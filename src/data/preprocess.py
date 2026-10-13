"""Pré-processamento das reviews da Olist.

Carrega `olist_order_reviews_dataset.csv`, remove registros sem texto,
enriquece com metadados (status do pedido e categoria do produto) e
gera um dataset limpo pronto para a geração de embeddings
(ver skill `olist-data-prep` e `olist-embeddings`).
"""

from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

ARQUIVO_REVIEWS = "olist_order_reviews_dataset.csv"
ARQUIVO_ORDERS = "olist_orders_dataset.csv"
ARQUIVO_ORDER_ITEMS = "olist_order_items_dataset.csv"
ARQUIVO_PRODUTOS = "olist_products_dataset.csv"
ARQUIVO_TRADUCAO_CATEGORIA = "product_category_name_translation.csv"

ARQUIVO_SAIDA = RAW_DATA_DIR / "olist_reviews_clean.csv"

COLUNAS_FINAIS = [
    "review_id",
    "order_id",
    "review_score",
    "review_comment_message",
    "review_creation_date",
    "order_status",
    "product_category_name_english",
]


def _ler_csv(nome_arquivo: str) -> pd.DataFrame:
    caminho = RAW_DATA_DIR / nome_arquivo
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError as erro:
        raise FileNotFoundError(
            f"Arquivo '{nome_arquivo}' não encontrado em '{RAW_DATA_DIR}'. "
            "Execute 'src/data/download_data.py' antes do pré-processamento."
        ) from erro


def carregar_reviews_com_texto() -> pd.DataFrame:
    """Carrega as reviews e descarta as que não têm comentário escrito."""
    reviews = _ler_csv(ARQUIVO_REVIEWS)

    total = len(reviews)
    reviews = reviews.dropna(subset=["review_comment_message"])
    reviews = reviews[reviews["review_comment_message"].str.strip() != ""]

    # review_id tem duplicatas no dataset original da Olist (mesma review
    # associada a mais de um pedido); mantemos a primeira ocorrência para
    # garantir unicidade na indexação do vectorstore.
    reviews = reviews.drop_duplicates(subset="review_id", keep="first")

    print(f"Reviews totais: {total} | Reviews com texto (únicas): {len(reviews)}")

    return reviews


def _limpar_texto(serie: pd.Series) -> pd.Series:
    """Normaliza espaços em branco; preserva o conteúdo original para o embedding."""
    return serie.str.replace(r"\s+", " ", regex=True).str.strip()


def enriquecer_com_metadados(reviews: pd.DataFrame) -> pd.DataFrame:
    """Adiciona status do pedido e categoria (em inglês) do produto."""
    orders = _ler_csv(ARQUIVO_ORDERS)[["order_id", "order_status"]]

    order_items = _ler_csv(ARQUIVO_ORDER_ITEMS)[["order_id", "product_id"]]
    order_items = order_items.drop_duplicates(subset="order_id", keep="first")

    produtos = _ler_csv(ARQUIVO_PRODUTOS)[["product_id", "product_category_name"]]
    traducao = _ler_csv(ARQUIVO_TRADUCAO_CATEGORIA)

    produto_categoria = order_items.merge(produtos, on="product_id", how="left")
    produto_categoria = produto_categoria.merge(
        traducao, on="product_category_name", how="left"
    )
    produto_categoria = produto_categoria[
        ["order_id", "product_category_name_english"]
    ]

    enriquecido = reviews.merge(orders, on="order_id", how="left")
    enriquecido = enriquecido.merge(produto_categoria, on="order_id", how="left")

    return enriquecido


def pre_processar() -> pd.DataFrame:
    """Pipeline completo: carregar, limpar texto e enriquecer com metadados."""
    reviews = carregar_reviews_com_texto()
    reviews["review_comment_message"] = _limpar_texto(reviews["review_comment_message"])

    enriquecido = enriquecer_com_metadados(reviews)

    faltantes_categoria = enriquecido["product_category_name_english"].isna().sum()
    if faltantes_categoria:
        print(
            f"Aviso: {faltantes_categoria} review(s) sem categoria de produto "
            "identificada (mantidas, sem exclusão)."
        )

    return enriquecido[COLUNAS_FINAIS].reset_index(drop=True)


def main() -> None:
    dados_limpos = pre_processar()

    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    dados_limpos.to_csv(ARQUIVO_SAIDA, index=False)
    print(f"Dataset limpo salvo em: {ARQUIVO_SAIDA} ({len(dados_limpos)} linhas)")


if __name__ == "__main__":
    main()
