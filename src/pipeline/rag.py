"""Pipeline RAG: pergunta -> busca semântica -> prompt -> Gemini -> resposta com evidências.

Fluxo (ver skill `olist-rag-pipeline`):
1. Busca as reviews mais parecidas com a pergunta (`buscar_similares`, do vectorstore).
2. Descarta as reviews com similaridade abaixo do mínimo (prevenção de alucinação).
3. Se não sobrar nenhuma, responde que não há evidências, SEM chamar o LLM.
4. Monta o prompt com as reviews relevantes e envia ao Gemini.
5. Devolve o texto da resposta + a lista de evidências usadas.
"""

import os
from dataclasses import dataclass, field

import pandas as pd
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.vectorstore.chroma_store import buscar_similares

# Carrega o GOOGLE_API_KEY (e opcionalmente GEMINI_MODEL) do arquivo .env
load_dotenv()

MODELO_LLM = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Calibrado empiricamente (17/10): perguntas dentro do escopo ficaram entre
# 0,71 e 0,99; perguntas fora do escopo ("capital da França", "preço do dólar")
# ficaram entre 0,50 e 0,56. O mínimo fica no meio dessa faixa.
SIMILARIDADE_MINIMA = 0.62

K_PADRAO = 20

MENSAGEM_SEM_EVIDENCIA = (
    "Não encontrei avaliações de clientes suficientes na base da Olist "
    "para responder a essa pergunta."
)

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um analista de Voz do Cliente da Olist. Responda à pergunta "
            "usando EXCLUSIVAMENTE as avaliações de clientes fornecidas no contexto.\n"
            "Regras:\n"
            "1. Não use conhecimento externo nem invente informações.\n"
            "2. Toda afirmação deve citar o review_id da avaliação que a sustenta, "
            "no formato [review_id].\n"
            "3. Se as avaliações não forem suficientes para responder, diga "
            "exatamente: \"" + MENSAGEM_SEM_EVIDENCIA + "\"\n"
            "4. Responda em português, de forma objetiva, em tópicos quando fizer sentido.",
        ),
        (
            "human",
            "Avaliações de clientes (contexto):\n{contexto}\n\nPergunta: {pergunta}",
        ),
    ]
)


@dataclass
class RespostaRAG:
    """Resultado do pipeline: texto da resposta + evidências que a sustentam."""

    resposta: str
    evidencias: list[dict] = field(default_factory=list)
    tem_evidencia: bool = False


def filtrar_relevantes(resultados: pd.DataFrame, minimo: float = SIMILARIDADE_MINIMA) -> pd.DataFrame:
    """Mantém só as reviews com similaridade igual ou acima do mínimo."""
    return resultados[resultados["similaridade"] >= minimo]


def formatar_contexto(reviews: pd.DataFrame) -> str:
    """Transforma as reviews em texto para o prompt, uma por linha, com metadados."""
    linhas = []
    for _, review in reviews.iterrows():
        linhas.append(
            f"[{review['review_id']}] (nota {review['review_score']}, "
            f"categoria {review['product_category_name_english']}): "
            f"{review['review_comment_message']}"
        )
    return "\n".join(linhas)


def extrair_evidencias(reviews: pd.DataFrame) -> list[dict]:
    """Lista estruturada das evidências: review_id, nota, similaridade e trecho."""
    colunas = ["review_id", "review_score", "similaridade", "review_comment_message"]
    return reviews[colunas].to_dict(orient="records")


def responder(pergunta: str, k: int = K_PADRAO, filtros: dict | None = None) -> RespostaRAG:
    """Executa o pipeline RAG completo para uma pergunta."""
    resultados = buscar_similares(pergunta, k=k, filtros=filtros)
    relevantes = filtrar_relevantes(resultados)

    # Regra de ouro: sem evidência relevante, não chama o LLM (evita alucinação).
    if relevantes.empty:
        return RespostaRAG(resposta=MENSAGEM_SEM_EVIDENCIA)

    evidencias = extrair_evidencias(relevantes)

    try:
        llm = ChatGoogleGenerativeAI(model=MODELO_LLM, temperature=0)
        cadeia = PROMPT | llm | StrOutputParser()
        texto = cadeia.invoke(
            {"contexto": formatar_contexto(relevantes), "pergunta": pergunta}
        )
    except Exception as erro:
        return RespostaRAG(
            resposta=f"Não foi possível consultar o modelo de linguagem agora: {erro}",            evidencias=evidencias,
            tem_evidencia=True,
        )

    return RespostaRAG(resposta=texto, evidencias=evidencias, tem_evidencia=True)


def imprimir(resultado: RespostaRAG) -> None:
    """Exibe a resposta e as evidências no terminal."""
    print("\n=== RESPOSTA ===")
    print(resultado.resposta)
    if resultado.evidencias:
        print("\n=== EVIDÊNCIAS ===")
        for ev in resultado.evidencias:
            print(
                f"- [{ev['review_id']}] nota {ev['review_score']} | "
                f"similaridade {ev['similaridade']:.2f} | {ev['review_comment_message']}"
            )


if __name__ == "__main__":
    pergunta = input("Pergunta: ")
    imprimir(responder(pergunta))