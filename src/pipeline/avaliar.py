"""Avaliação do pipeline RAG com um conjunto fixo de perguntas.

Roda perguntas dentro e fora do escopo, registra se houve evidência, quantas
reviews foram usadas, a maior similaridade e a resposta do Gemini, e salva
tudo em `docs/avaliacao_rag.md` (ver skill `olist-evaluator`).

Uso: python -m src.pipeline.avaliar [sufixo]
"""

import time
from datetime import datetime
from pathlib import Path

from src.pipeline.rag import SIMILARIDADE_MINIMA, montar_filtros, responder

PASTA_DOCS = Path(__file__).resolve().parents[2] / "docs"

# (pergunta, filtros, escopo esperado)
# Perguntas 1 a 11: exemplos do enunciado do Tech Challenge (páginas 4, 5, 8 e 9).
CASOS_DE_TESTE = [
    ("Quais são os principais problemas relatados pelos clientes?", None, "dentro"),
    ("Quais reclamações relacionadas à entrega aparecem com maior frequência?", None, "dentro"),
    ("O que os clientes mais elogiam em suas experiências de compra?", None, "dentro"),
    ("Quais problemas são relatados por clientes insatisfeitos?", None, "dentro"),
    ("Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?", None, "dentro"),
    ("O que os clientes relatam sobre problemas relacionados à entrega?", None, "dentro"),
    ("Quais aspectos da experiência de compra são mais elogiados pelos clientes?", None, "dentro"),
    ("Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?", None, "dentro"),
    ("Quais são os principais problemas relatados nas avaliações com nota baixa?", montar_filtros(nota_maxima=2), "dentro"),
    ("O que os clientes mais elogiam em determinadas categorias de produtos?", montar_filtros(categoria="health_beauty"), "dentro"),
    ("Quais temas aparecem nas avaliações relacionadas a experiências de entrega insatisfatórias?", montar_filtros(nota_maxima=2), "dentro"),
    ("o produto chegou quebrado ou com defeito?", montar_filtros(nota_maxima=2, categoria="furniture_decor"), "dentro"),
    ("qual a capital da França?", None, "fora"),
    ("como está o preço do dólar hoje?", None, "fora"),
    ("qual o melhor celular para comprar este ano?", None, "fora"),
]


def avaliar(sufixo: str = "") -> None:
    arquivo_relatorio = PASTA_DOCS / f"avaliacao_rag{sufixo}.md"
    linhas = [
        "# Avaliação do pipeline RAG",
        "",
        f"Gerado em {datetime.now():%d/%m/%Y %H:%M} | similaridade mínima: {SIMILARIDADE_MINIMA}",
        "",
        "| # | Pergunta | Filtros | Escopo esperado | Respondeu? | Reviews usadas | Maior similaridade | Resultado |",
        "|---|---|---|---|---|---|---|---|",
    ]
    detalhes = ["", "## Respostas completas", ""]

    for numero, (pergunta, filtros, escopo) in enumerate(CASOS_DE_TESTE, start=1):
        print(f"[{numero}/{len(CASOS_DE_TESTE)}] {pergunta}")
        resultado = responder(pergunta, filtros=filtros)

        respondeu = resultado.tem_evidencia
        erro_llm = resultado.resposta.startswith("Não foi possível consultar")
        maior = max((ev["similaridade"] for ev in resultado.evidencias), default=None)
        correto = respondeu if escopo == "dentro" else not respondeu
        status = "ERRO NO LLM" if erro_llm else ("OK" if correto else "REVISAR")

        linhas.append(
            f"| {numero} | {pergunta} | {filtros or '-'} | {escopo} | "
            f"{'sim' if respondeu else 'não'} | {len(resultado.evidencias)} | "
            f"{f'{maior:.2f}' if maior is not None else '-'} | {status} |"
        )
        detalhes += [f"### {numero}. {pergunta}", "", f"Filtros: {filtros or 'nenhum'}", "", resultado.resposta, ""]

        if respondeu:
            time.sleep(5)  # evita estourar o limite de chamadas por minuto do nível gratuito

    arquivo_relatorio.parent.mkdir(parents=True, exist_ok=True)
    arquivo_relatorio.write_text("\n".join(linhas + detalhes), encoding="utf-8")
    print(f"\nRelatório salvo em: {arquivo_relatorio}")


if __name__ == "__main__":
    import sys

    # Ex.: python -m src.pipeline.avaliar _antes  ->  docs/avaliacao_rag_antes.md
    avaliar(sys.argv[1] if len(sys.argv) > 1 else "")
