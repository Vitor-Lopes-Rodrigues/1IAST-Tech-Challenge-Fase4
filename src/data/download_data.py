"""Download do dataset Olist (Brazilian E-Commerce) via kagglehub.

Baixa `olistbr/brazilian-ecommerce` e copia os CSVs para `data/raw/`,
local esperado pelo restante do pipeline (ver CLAUDE.md).
"""

import shutil
from pathlib import Path

import kagglehub

DATASET_SLUG = "olistbr/brazilian-ecommerce"
RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def baixar_dataset() -> Path:
    """Baixa o dataset do Kaggle e retorna o diretório local do cache do kagglehub."""
    try:
        caminho_cache = kagglehub.dataset_download(DATASET_SLUG)
    except Exception as erro:
        raise RuntimeError(
            f"Falha ao baixar o dataset '{DATASET_SLUG}' via kagglehub. "
            "Verifique sua autenticação do Kaggle (kaggle.json ou "
            "variáveis KAGGLE_USERNAME/KAGGLE_KEY)."
        ) from erro

    return Path(caminho_cache)


def copiar_para_data_raw(caminho_cache: Path) -> list[Path]:
    """Copia todos os CSVs do cache do kagglehub para data/raw/."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    arquivos_copiados = []
    for csv in caminho_cache.glob("*.csv"):
        destino = RAW_DATA_DIR / csv.name
        shutil.copy2(csv, destino)
        arquivos_copiados.append(destino)

    if not arquivos_copiados:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em '{caminho_cache}' após o download do dataset."
        )

    return arquivos_copiados


def main() -> None:
    print(f"Baixando dataset '{DATASET_SLUG}' via kagglehub...")
    caminho_cache = baixar_dataset()
    print(f"Dataset disponível em: {caminho_cache}")

    arquivos = copiar_para_data_raw(caminho_cache)
    print(f"{len(arquivos)} arquivo(s) copiado(s) para {RAW_DATA_DIR}:")
    for arquivo in arquivos:
        print(f"  - {arquivo.name}")


if __name__ == "__main__":
    main()
