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

MODELO_LLM = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

# Quantas vezes a biblioteca tenta de novo quando o Gemini falha (ex.: 503).
# Cada tentativa conta na cota diária do nível gratuito, então mantemos baixo.
MAX_TENTATIVAS_LLM = int(os.getenv("GEMINI_MAX_RETRIES", "1"))

# Calibrado empiricamente (17/10): perguntas dentro do escopo ficaram entre
# 0,71 e 0,99; perguntas fora do escopo ("capital da França", "preço do dólar")
# ficaram entre 0,50 e 0,56. O mínimo fica no meio dessa faixa.
SIMILARIDADE_MINIMA = 0.57

K_PADRAO = 30

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
            "4. Responda em português, de forma objetiva, em tópicos quando fizer sentido.\n"
            "5. Cada avaliação indica quantos clientes escreveram o mesmo texto. Use essa "
            "contagem para ordenar os tópicos do mais frequente para o menos frequente e "
            "informe quantos clientes mencionaram cada problema.",
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

def agrupar_repetidas(reviews: pd.DataFrame) -> pd.DataFrame:
    """Agrupa reviews com o mesmo texto (ignorando maiúsculas e pontuação).

    Mantém a primeira de cada grupo e adiciona a coluna `ocorrencias`,
    com quantos clientes escreveram aquele mesmo texto.
    """
    chave = (
        reviews["review_comment_message"]
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.strip()
    )
    agrupadas = reviews.assign(_chave=chave)
    agrupadas["ocorrencias"] = agrupadas.groupby("_chave")["_chave"].transform("size")
    return agrupadas.drop_duplicates("_chave").drop(columns="_chave")

def formatar_contexto(reviews: pd.DataFrame) -> str:
    """Transforma as reviews em texto para o prompt, uma por linha, com metadados."""
    linhas = []
    for _, review in reviews.iterrows():
        linhas.append(
            f"[{review['review_id']}] (nota {review['review_score']}, "
            f"categoria {review['product_category_name_english']}, "
            f"{review['ocorrencias']} cliente(s) escreveram o mesmo): "
            f"{review['review_comment_message']}"
        )
    return "\n".join(linhas)


def extrair_evidencias(reviews: pd.DataFrame) -> list[dict]:
    """Lista estruturada das evidências: review_id, nota, similaridade, ocorrências e trecho."""
    colunas = ["review_id", "review_score", "similaridade", "ocorrencias", "review_comment_message"]
    return reviews[colunas].to_dict(orient="records")

def montar_filtros(nota_maxima: int | None = None, categoria: str | None = None) -> dict | None:
    """Monta o filtro de metadados no formato `where` do ChromaDB.

    Exemplos:
        montar_filtros(nota_maxima=2) -> {"review_score": {"$lte": 2}}
        montar_filtros(categoria="furniture_decor") -> {"product_category_name_english": "furniture_decor"}
    """
    condicoes = []
    if nota_maxima is not None:
        condicoes.append({"review_score": {"$lte": nota_maxima}})
    if categoria:
        condicoes.append({"product_category_name_english": categoria})

    if not condicoes:
        return None
    if len(condicoes) == 1:
        return condicoes[0]
    return {"$and": condicoes}

def responder(pergunta: str, k: int = K_PADRAO, filtros: dict | None = None) -> RespostaRAG:
    """Executa o pipeline RAG completo para uma pergunta."""
    resultados = buscar_similares(pergunta, k=k, filtros=filtros)
    relevantes = filtrar_relevantes(resultados)

    # Regra de ouro: sem evidência relevante, não chama o LLM (evita alucinação).
    if relevantes.empty:
        return RespostaRAG(resposta=MENSAGEM_SEM_EVIDENCIA)

    relevantes = agrupar_repetidas(relevantes)
    evidencias = extrair_evidencias(relevantes)

    try:
        llm = ChatGoogleGenerativeAI(
            model=MODELO_LLM, temperature=0, max_retries=MAX_TENTATIVAS_LLM
        )
        cadeia = PROMPT | llm | StrOutputParser()
        texto = cadeia.invoke(
            {"contexto": formatar_contexto(relevantes), "pergunta": pergunta}
        )
    except Exception as erro:
        return RespostaRAG(
            resposta=f"Não foi possível consultar o modelo de linguagem agora: {erro}",
            evidencias=evidencias,
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
                f"similaridade {ev['similaridade']:.2f} | "
                f"{ev['ocorrencias']}x | {ev['review_comment_message']}"
            )


if __name__ == "__main__":
    pergunta = input("Pergunta: ")
    nota = input("Nota máxima (1 a 5, Enter para todas): ").strip()
    categoria = input("Categoria em inglês (Enter para todas): ").strip()

    filtros = montar_filtros(
        nota_maxima=int(nota) if nota else None,
        categoria=categoria or None,
    )
    imprimir(responder(pergunta, filtros=filtros))