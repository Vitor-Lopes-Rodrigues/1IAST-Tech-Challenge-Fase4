"""Avaliação do pipeline RAG com um conjunto fixo de perguntas.

Roda perguntas dentro e fora do escopo, registra se houve evidência, quantas
reviews foram usadas, a maior similaridade e a resposta do Gemini, e salva
tudo em `docs/avaliacao_rag.md` (ver skill `olist-evaluator`).

Uso: python -m src.pipeline.avaliar
"""

import time
from datetime import datetime
from pathlib import Path

from src.pipeline.rag import SIMILARIDADE_MINIMA, montar_filtros, responder

ARQUIVO_RELATORIO = Path(__file__).resolve().parents[2] / "docs" / "avaliacao_rag.md"

# (pergunta, filtros, escopo esperado)
CASOS_DE_TESTE = [
    ("quais as principais reclamações sobre a entrega?", None, "dentro"),
    ("quais as reclamações de entrega mais frequentes?", None, "dentro"),
    ("o produto chegou quebrado ou com defeito?", None, "dentro"),
    ("os clientes recebem produto diferente do que compraram?", None, "dentro"),
    ("o que os clientes elogiam na entrega?", None, "dentro"),
    ("o produto chegou quebrado ou com defeito?", montar_filtros(nota_maxima=2, categoria="furniture_decor"), "dentro"),
    ("qual a capital da França?", None, "fora"),
    ("como está o preço do dólar hoje?", None, "fora"),
    ("qual o melhor celular para comprar este ano?", None, "fora"),
]


def avaliar() -> None:
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
        maior = max((ev["similaridade"] for ev in resultado.evidencias), default=None)
        correto = respondeu if escopo == "dentro" else not respondeu

        linhas.append(
            f"| {numero} | {pergunta} | {filtros or '-'} | {escopo} | "
            f"{'sim' if respondeu else 'não'} | {len(resultado.evidencias)} | "
            f"{f'{maior:.2f}' if maior is not None else '-'} | {'OK' if correto else 'REVISAR'} |"
        )
        detalhes += [f"### {numero}. {pergunta}", "", f"Filtros: {filtros or 'nenhum'}", "", resultado.resposta, ""]

        if respondeu:
            time.sleep(2)  # evita estourar o limite de chamadas por minuto do nível gratuito

    ARQUIVO_RELATORIO.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_RELATORIO.write_text("\n".join(linhas + detalhes), encoding="utf-8")
    print(f"\nRelatório salvo em: {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    avaliar()
