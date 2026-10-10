---
name: olist-data-prep
description: Use para ingestão (kagglehub) e pré-processamento dos dados da Olist — download do dataset, limpeza de review_comment_message, tratamento de nulos e join com metadados de pedidos/produtos. Acionar para tarefas em src/data/ e src/embeddings/.
---

# Olist Data Prep

Esta skill cobre o primeiro pilar do projeto (ver `CLAUDE.md`): **Construção da Base de Conhecimento**.

## Quando usar
- Ingestão do dataset `olistbr/brazilian-ecommerce` via `kagglehub` (`src/data/download_data.py`).
- Limpeza de `olist_order_reviews_dataset.csv`: nulos, texto vazio, encoding, ruído (`src/data/preprocess.py`).
- Join com metadados relevantes de outros CSVs do dataset (pedidos, produtos, clientes — score, datas, categoria do produto, status de entrega).
- Chunking de texto (se necessário) e geração de embeddings (`src/embeddings/`).

## Diretrizes

1. **Ingestão via kagglehub**: baixar com `kagglehub.dataset_download("olistbr/brazilian-ecommerce")` (ou `KaggleDatasetAdapter`) e persistir/ler os CSVs a partir de `data/raw/` — nunca apontar código de produção direto para o cache do kagglehub.
2. **Nunca** processar dados diretamente em notebooks para produção — notebooks são só para EDA/prototipação (`notebooks/`). Código final vai em `src/data/` (ingestão/limpeza/chunking) e `src/embeddings/` (geração/gerenciamento de vetores).
3. **Tratamento de nulos**: descartar ou sinalizar explicitamente reviews sem `review_comment_message`; nunca inventar texto. Documentar a decisão no código.
4. **Modelo de embedding**: priorizar modelos otimizados para português (ex: `paraphrase-multilingual-MiniLM-L12-v2`, `text-embedding-3-small`). Normalizar os vetores (`normalize_embeddings=True`) quando a métrica for similaridade de cosseno.
5. **Metadados**: preservar `review_id`, `order_id`, `review_score`, `review_creation_date`, categoria do produto e status de entrega junto de cada chunk/vetor — são necessários para rastreabilidade e filtragem no pipeline RAG.
6. **Tratamento de exceções**: envolver download/leitura de CSV e chamadas a APIs de embedding (se usar API externa) em try/except com mensagens claras; nunca falhar silenciosamente.
7. **Reprodutibilidade**: usar `random_state` fixo em amostragens; documentar o tamanho do dataset usado (amostra vs. completo) e checar duplicatas de `review_id` (conhecidas no dataset original).

## Saída esperada
Funções/módulos reutilizáveis em `src/data/` (ex: `baixar_dataset()`, `pre_processar()`) e `src/embeddings/` (ex: `gerar_embeddings()`), com checagens básicas de sanidade (shape dos embeddings, contagem de nulos/duplicatas antes e depois).
