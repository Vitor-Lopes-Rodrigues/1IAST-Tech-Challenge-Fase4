"""Geração de embeddings das reviews da Olist.

Usa um modelo multilíngue (bom para português) e normaliza os vetores,
para que a similaridade de cosseno vire um produto interno simples
— consistente com o espaço de distância configurado no ChromaDB
(ver `src/vectorstore/chroma_store.py`).
"""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def carregar_modelo() -> SentenceTransformer:
    """Carrega o modelo de embeddings uma única vez por processo."""
    try:
        return SentenceTransformer(MODEL_NAME)
    except Exception as erro:
        raise RuntimeError(
            f"Falha ao carregar o modelo de embeddings '{MODEL_NAME}'. "
            "Verifique a conexão com a internet (download do modelo) ou "
            "se a biblioteca 'sentence-transformers' está instalada."
        ) from erro


def gerar_embeddings(textos: list[str], mostrar_progresso: bool = False) -> np.ndarray:
    """Converte uma lista de textos em vetores normalizados (norma 1)."""
    if not textos:
        return np.empty((0, 0), dtype="float32")

    modelo = carregar_modelo()
    return modelo.encode(
        textos,
        normalize_embeddings=True,
        show_progress_bar=mostrar_progresso,
    )
