"""Indexação e busca por similaridade das reviews da Olist via ChromaDB.

Escolha de tecnologia: ChromaDB em vez de FAISS puro porque precisamos de
filtragem nativa por metadados (score, data, categoria, status de entrega)
junto da busca vetorial, além de persistência em disco sem servidor externo
(ver skill `olist-vectorstore`).
"""

from pathlib import Path

import chromadb
import pandas as pd

from src.embeddings.embedder import gerar_embeddings

PERSIST_DIR = Path(__file__).resolve().parents[2] / "data" / "vectorstore" / "chroma"
COLLECTION_NAME = "olist_reviews"

COLUNAS_METADADOS = [
    "order_id",
    "review_score",
    "review_creation_date",
    "order_status",
    "product_category_name_english",
]

TAMANHO_LOTE = 1000


def _obter_cliente() -> chromadb.ClientAPI:
    try:
        PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        return chromadb.PersistentClient(path=str(PERSIST_DIR))
    except Exception as erro:
        raise RuntimeError(
            f"Falha ao conectar/criar o banco vetorial em '{PERSIST_DIR}'."
        ) from erro


def obter_colecao():
    """Recupera (ou cria) a coleção configurada para similaridade de cosseno."""
    cliente = _obter_cliente()
    return cliente.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _montar_metadados(linha: pd.Series) -> dict:
    """Converte uma linha do DataFrame em metadados aceitos pelo ChromaDB.

    O ChromaDB não aceita NaN/None como valor de metadado, então campos
    ausentes são preenchidos com um marcador explícito ("desconhecido").
    """
    metadados = {}
    for coluna in COLUNAS_METADADOS:
        valor = linha[coluna]
        if pd.isna(valor):
            metadados[coluna] = "desconhecido"
        elif coluna == "review_score":
            metadados[coluna] = int(valor)
        else:
            metadados[coluna] = str(valor)
    return metadados


def indexar_reviews(df: pd.DataFrame, recriar: bool = False) -> int:
    """Gera embeddings para `df` e indexa no ChromaDB em lotes.

    `df` deve conter as colunas produzidas por `src/data/preprocess.py`
    (review_id, review_comment_message + metadados).
    """
    cliente = _obter_cliente()

    if recriar:
        try:
            cliente.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # coleção pode não existir ainda

    colecao = cliente.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total_indexado = 0
    for inicio in range(0, len(df), TAMANHO_LOTE):
        lote = df.iloc[inicio : inicio + TAMANHO_LOTE]

        textos = lote["review_comment_message"].tolist()
        embeddings = gerar_embeddings(textos).tolist()
        ids = lote["review_id"].astype(str).tolist()
        metadatas = [_montar_metadados(linha) for _, linha in lote.iterrows()]

        colecao.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=textos,
            metadatas=metadatas,
        )
        total_indexado += len(lote)
        print(f"Indexadas {total_indexado}/{len(df)} reviews...")

    return total_indexado


def buscar_similares(pergunta: str, k: int = 5, filtros: dict | None = None) -> pd.DataFrame:
    """Busca as `k` reviews mais similares à `pergunta`, com filtros opcionais.

    `filtros` segue a sintaxe de `where` do ChromaDB, ex:
    {"review_score": {"$lte": 2}} ou {"order_status": "delivered"}.
    """
    colecao = obter_colecao()

    vetor_pergunta = gerar_embeddings([pergunta]).tolist()

    resultado = colecao.query(
        query_embeddings=vetor_pergunta,
        n_results=k,
        where=filtros,
    )

    if not resultado["ids"][0]:
        return pd.DataFrame(
            columns=["review_id", "similaridade", "review_comment_message", *COLUNAS_METADADOS]
        )

    linhas = []
    for review_id, documento, metadados, distancia in zip(
        resultado["ids"][0],
        resultado["documents"][0],
        resultado["metadatas"][0],
        resultado["distances"][0],
    ):
        similaridade = 1 - distancia  # espaço "cosine": distância = 1 - similaridade
        linhas.append(
            {
                "review_id": review_id,
                "similaridade": round(similaridade, 4),
                "review_comment_message": documento,
                **metadados,
            }
        )

    return pd.DataFrame(linhas)


def main() -> None:
    from src.data.preprocess import ARQUIVO_SAIDA

    if not ARQUIVO_SAIDA.exists():
        raise FileNotFoundError(
            f"'{ARQUIVO_SAIDA}' não encontrado. Execute 'src/data/preprocess.py' antes."
        )

    df = pd.read_csv(ARQUIVO_SAIDA)
    total = indexar_reviews(df, recriar=True)
    print(f"Indexação concluída: {total} reviews em '{PERSIST_DIR}'.")


if __name__ == "__main__":
    main()
