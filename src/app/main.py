"""Interface Streamlit do RAG de Voz do Cliente (Olist).

Executar a partir da raiz do projeto:
    streamlit run src/app/main.py
"""

import sys
from pathlib import Path

# O Streamlit adiciona src/app ao sys.path, não a raiz; sem isso `from src...` quebra.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import streamlit as st

from src.pipeline.rag import (
    K_PADRAO,
    SIMILARIDADE_MINIMA,
    RespostaRAG,
    montar_filtros,
    responder,
)
from src.vectorstore.chroma_store import obter_colecao

PREFIXO_ERRO_LLM = "Não foi possível consultar"
TAMANHO_LOTE_CATEGORIAS = 5000

PERGUNTAS_EXEMPLO = [
    "Quais reclamações relacionadas à entrega aparecem com maior frequência?",
    "O que os clientes mais elogiam em suas experiências de compra?",
    "Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?",
    "qual a capital da França?",
]

st.set_page_config(page_title="Voz do Cliente - Olist", page_icon="💬", layout="wide")


@st.cache_data(show_spinner=False)
def listar_categorias() -> list[str]:
    """Categorias de produto presentes no banco vetorial (para o filtro)."""
    colecao = obter_colecao()
    categorias = set()
    # Em lotes: um único get() sobre a coleção inteira estoura o limite de
    # variáveis do SQLite ("too many SQL variables").
    for inicio in range(0, colecao.count(), TAMANHO_LOTE_CATEGORIAS):
        lote = colecao.get(
            include=["metadatas"], limit=TAMANHO_LOTE_CATEGORIAS, offset=inicio
        )
        categorias.update(m["product_category_name_english"] for m in lote["metadatas"])
    categorias.discard("desconhecido")
    return sorted(categorias)


def consultar(pergunta: str, k: int, filtros: dict | None) -> RespostaRAG:
    """Chama o pipeline com cache por sessão para poupar a cota do Gemini.

    Respostas com erro do LLM não são guardadas, para permitir nova tentativa.
    """
    cache = st.session_state.setdefault("cache_respostas", {})
    chave = (pergunta, k, str(filtros))
    if chave in cache:
        return cache[chave]

    resultado = responder(pergunta, k=k, filtros=filtros)
    if not resultado.resposta.startswith(PREFIXO_ERRO_LLM):
        cache[chave] = resultado
    return resultado


def mostrar_evidencias(resultado: RespostaRAG) -> None:
    st.subheader(f"Evidências ({len(resultado.evidencias)})")
    tabela = pd.DataFrame(resultado.evidencias).rename(
        columns={
            "review_id": "ID da avaliação",
            "review_score": "Nota",
            "similaridade": "Similaridade",
            "ocorrencias": "Clientes com o mesmo texto",
            "review_comment_message": "Comentário",
        }
    )
    st.dataframe(tabela, use_container_width=True, hide_index=True)


with st.sidebar:
    st.header("Filtros")
    usar_nota = st.checkbox("Limitar pela nota")
    nota_maxima = st.slider("Nota máxima", 1, 5, 2, disabled=not usar_nota)

    try:
        categorias = listar_categorias()
    except Exception as erro:
        categorias = []
        st.warning(f"Não foi possível carregar as categorias: {erro}")
    categoria = st.selectbox("Categoria do produto", ["Todas", *categorias])

    st.header("Busca")
    k = st.slider("Reviews recuperadas (k)", 5, 50, K_PADRAO)
    st.caption(f"Similaridade mínima: {SIMILARIDADE_MINIMA}")

    st.header("Exemplos")
    for exemplo in PERGUNTAS_EXEMPLO:
        if st.button(exemplo, use_container_width=True):
            st.session_state["pergunta_pendente"] = exemplo

st.title("💬 Voz do Cliente - Olist")
st.write(
    "Pergunte em linguagem natural sobre as avaliações dos clientes. "
    "As respostas usam apenas as avaliações recuperadas e citam os IDs que as sustentam."
)

pergunta = st.chat_input("Digite sua pergunta") or st.session_state.pop("pergunta_pendente", None)

if pergunta:
    filtros = montar_filtros(
        nota_maxima=nota_maxima if usar_nota else None,
        categoria=None if categoria == "Todas" else categoria,
    )

    st.chat_message("user").write(pergunta)
    if filtros:
        st.caption(f"Filtros aplicados: {filtros}")

    with st.chat_message("assistant"):
        try:
            with st.spinner("Buscando avaliações e gerando resposta..."):
                resultado = consultar(pergunta, k, filtros)
        except Exception as erro:
            st.error(f"Erro ao executar o pipeline: {erro}")
            st.stop()

        if not resultado.tem_evidencia:
            st.warning(resultado.resposta)
        elif resultado.resposta.startswith(PREFIXO_ERRO_LLM):
            st.error(resultado.resposta)
        else:
            st.markdown(resultado.resposta)

    if resultado.evidencias:
        mostrar_evidencias(resultado)
