"""Avaliação do pipeline RAG com um conjunto fixo de perguntas.

Roda perguntas dentro e fora do escopo, registra se houve evidência, quantas
reviews foram usadas, a maior similaridade e a resposta do Gemini, e salva
tudo em `docs/avaliacao_rag.md` (ver skill `olist-evaluator`).

A avaliação é retomável: o resultado de cada pergunta fica guardado em
`docs/avaliacao_cache.json`. Nas próximas execuções, as perguntas que já deram
OK são reaproveitadas e só as que falharam (ou ainda não rodaram) chamam o
Gemini de novo. Se a cota diária acabar no meio, as restantes ficam como
PENDENTE e é só rodar de novo no dia seguinte: o relatório final sai completo.

Uso:
    python -m src.pipeline.avaliar             # retoma de onde parou
    python -m src.pipeline.avaliar --refazer   # ignora o cache e roda tudo de novo
    python -m src.pipeline.avaliar _teste      # grava em docs/avaliacao_rag_teste.md
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

from src.pipeline.rag import SIMILARIDADE_MINIMA, montar_filtros, responder

PASTA_DOCS = Path(__file__).resolve().parents[2] / "docs"
ARQUIVO_CACHE = PASTA_DOCS / "avaliacao_cache.json"

# (pergunta, filtros, escopo esperado)
# Perguntas 1 a 13: exemplos do enunciado do Tech Challenge (páginas 4, 5, 8 e 9).
CASOS_DE_TESTE = [
    ("Quais são os principais problemas relatados pelos clientes?", None, "dentro"),
    ("Quais são os principais problemas relatados pelos clientes em suas avaliações?", None, "dentro"),
    ("Quais reclamações relacionadas à entrega aparecem com maior frequência?", None, "dentro"),
    ("O que os clientes mais elogiam em suas experiências de compra?", None, "dentro"),
    ("Quais problemas são relatados por clientes insatisfeitos?", None, "dentro"),
    ("Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?", None, "dentro"),
    ("O que os clientes relatam sobre problemas relacionados à entrega?", None, "dentro"),
    ("Quais aspectos da experiência de compra são mais elogiados pelos clientes?", None, "dentro"),
    ("Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?", None, "dentro"),
    ("Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?", None, "dentro"),
    ("Quais são os principais problemas relatados nas avaliações com nota baixa?", montar_filtros(nota_maxima=2), "dentro"),
    ("O que os clientes mais elogiam em determinadas categorias de produtos?", montar_filtros(categoria="health_beauty"), "dentro"),
    ("Quais temas aparecem nas avaliações relacionadas a experiências de entrega insatisfatórias?", montar_filtros(nota_maxima=2), "dentro"),
    ("o produto chegou quebrado ou com defeito?", montar_filtros(nota_maxima=2, categoria="furniture_decor"), "dentro"),
    ("qual a capital da França?", None, "fora"),
    ("como está o preço do dólar hoje?", None, "fora"),
    ("qual o melhor celular para comprar este ano?", None, "fora"),
]


def chave_do_caso(pergunta: str, filtros: dict | None) -> str:
    """Identifica um caso no cache. Inclui o mínimo de similaridade: se ele mudar,
    os resultados antigos deixam de valer e a pergunta roda de novo."""
    return f"{pergunta} | {filtros} | min={SIMILARIDADE_MINIMA}"


def carregar_cache() -> dict:
    if ARQUIVO_CACHE.exists():
        return json.loads(ARQUIVO_CACHE.read_text(encoding="utf-8"))
    return {}


def salvar_cache(cache: dict) -> None:
    ARQUIVO_CACHE.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def rodar_caso(pergunta: str, filtros: dict | None, escopo: str) -> dict:
    """Executa uma pergunta no pipeline e devolve o resultado resumido."""
    resultado = responder(pergunta, filtros=filtros)

    respondeu = resultado.tem_evidencia
    erro_llm = resultado.resposta.startswith("Não foi possível consultar")
    maior = max((ev["similaridade"] for ev in resultado.evidencias), default=None)
    correto = respondeu if escopo == "dentro" else not respondeu

    return {
        "respondeu": respondeu,
        "reviews": len(resultado.evidencias),
        "maior": maior,
        "resposta": resultado.resposta,
        "status": "ERRO NO LLM" if erro_llm else ("OK" if correto else "REVISAR"),
        "cota_esgotada": "RESOURCE_EXHAUSTED" in resultado.resposta,
        "data": f"{datetime.now():%d/%m/%Y %H:%M}",
    }


def avaliar(sufixo: str = "", refazer: bool = False) -> None:
    arquivo_relatorio = PASTA_DOCS / f"avaliacao_rag{sufixo}.md"
    cache = {} if refazer else carregar_cache()
    cota_esgotada = False

    linhas = [
        "# Avaliação do pipeline RAG",
        "",
        f"Gerado em {datetime.now():%d/%m/%Y %H:%M} | similaridade mínima: {SIMILARIDADE_MINIMA}",
        "",
        "| # | Pergunta | Filtros | Escopo esperado | Respondeu? | Reviews usadas | Maior similaridade | Resultado |",
        "|---|---|---|---|---|---|---|---|",
    ]
    detalhes = ["", "## Respostas completas", ""]
    contagem = {}

    for numero, (pergunta, filtros, escopo) in enumerate(CASOS_DE_TESTE, start=1):
        chave = chave_do_caso(pergunta, filtros)
        anterior = cache.get(chave)

        if anterior and anterior["status"] == "OK":
            print(f"[{numero}/{len(CASOS_DE_TESTE)}] (já OK em {anterior['data']}) {pergunta}")
            caso = anterior
        elif cota_esgotada:
            print(f"[{numero}/{len(CASOS_DE_TESTE)}] (pendente: cota esgotada) {pergunta}")
            caso = None
        else:
            print(f"[{numero}/{len(CASOS_DE_TESTE)}] {pergunta}")
            caso = rodar_caso(pergunta, filtros, escopo)
            cache[chave] = caso
            salvar_cache(cache)  # salva a cada pergunta: se o script parar, nada se perde
            if caso["cota_esgotada"]:
                cota_esgotada = True
                print("    Cota diária do Gemini esgotada: as próximas ficam pendentes.")
            elif caso["respondeu"]:
                time.sleep(5)  # evita estourar o limite de chamadas por minuto do nível gratuito

        if caso is None:
            status = "PENDENTE"
            linhas.append(f"| {numero} | {pergunta} | {filtros or '-'} | {escopo} | - | - | - | {status} |")
            resposta = "Ainda não executada (cota diária do Gemini esgotada). Rode a avaliação de novo."
        else:
            status = caso["status"]
            maior = caso["maior"]
            linhas.append(
                f"| {numero} | {pergunta} | {filtros or '-'} | {escopo} | "
                f"{'sim' if caso['respondeu'] else 'não'} | {caso['reviews']} | "
                f"{f'{maior:.2f}' if maior is not None else '-'} | {status} |"
            )
            resposta = caso["resposta"]

        contagem[status] = contagem.get(status, 0) + 1
        detalhes += [f"### {numero}. {pergunta}", "", f"Filtros: {filtros or 'nenhum'}", "", resposta, ""]

    arquivo_relatorio.parent.mkdir(parents=True, exist_ok=True)
    arquivo_relatorio.write_text("\n".join(linhas + detalhes), encoding="utf-8")

    resumo = ", ".join(f"{qtd} {status}" for status, qtd in contagem.items())
    print(f"\nResumo: {resumo}")
    print(f"Relatório salvo em: {arquivo_relatorio}")
    if contagem.get("OK", 0) < len(CASOS_DE_TESTE):
        print("Ainda há perguntas sem OK. Rode de novo mais tarde: as que já deram OK não serão refeitas.")


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    refazer = "--refazer" in argumentos
    sufixos = [a for a in argumentos if not a.startswith("--")]
    # Ex.: python -m src.pipeline.avaliar _antes  ->  docs/avaliacao_rag_antes.md
    avaliar(sufixos[0] if sufixos else "", refazer=refazer)
