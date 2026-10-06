---
name: olist-data-prep
description: Ingestão automática via kagglehub e pré-processamento dos dados da Olist.
---

# Skill: Ingestão e Preparação de Dados Olist

Quando acionado para carregar ou processar os dados:

1. **Ingestão (kagglehub)**:
   - Baixar o dataset `olistbr/brazilian-ecommerce` usando `kagglehub.dataset_download` ou `KaggleDatasetAdapter`[cite: 15].
   - Garantir a persistência ou leitura direta a partir da pasta `data/raw/`[cite: 13].

2. **Limpeza e Filtragem**:
   - Carregar `olist_order_reviews_dataset.csv` e realizar o merge com metadados de pedidos/produtos caso necessário[cite: 4, 8].
   - Remover registros com `review_comment_message` nulo ou vazio[cite: 4, 6].
   - Preservar metadados: `review_score`, `review_creation_date`, `order_id`[cite: 4, 8].

3. **Saída**:
   - Manter os módulos em `src/data/download_data.py` e `src/data/preprocess.py`.

   
# Olist Data Prep

Esta skill cobre o primeiro pilar do projeto (ver `CLAUDE.md`): **Construção da Base de Conhecimento**.

## Quando usar
- Ingestão do `olist_order_reviews_dataset.csv` (e datasets relacionados: orders, products, customers) a partir de `data/raw/`.
- Limpeza de `review_comment_message` (nulos, texto vazio, encoding, ruído).
- Join com metadados relevantes (score, datas, categoria do produto, status de entrega).
- Chunking de texto (se necessário) e geração de embeddings.

## Diretrizes

1. **Nunca** processar dados diretamente em notebooks para produção — notebooks são só para EDA/prototipação (`notebooks/`). Código final vai em `src/data/` (ingestão/limpeza/chunking) e `src/embeddings/` (geração/gerenciamento de vetores).
2. **Tratamento de nulos**: descartar ou sinalizar explicitamente reviews sem `review_comment_message`; nunca inventar texto. Documentar a decisão no código.
3. **Modelo de embedding**: priorizar modelos otimizados para português (ex: `paraphrase-multilingual-MiniLM-L12-v2`, `text-embedding-3-small`). Normalizar os vetores (`normalize_embeddings=True`) quando a métrica for similaridade de cosseno.
4. **Metadados**: preservar `review_id`, `order_id`, `review_score`, `review_creation_date`, categoria do produto e status de entrega junto de cada chunk/vetor — são necessários para rastreabilidade e filtragem no pipeline RAG.
5. **Tratamento de exceções**: envolver leitura de CSV e chamadas a APIs de embedding (se usar API externa) em try/except com mensagens claras; nunca falhar silenciosamente.
6. **Reprodutibilidade**: usar `random_state` fixo em amostragens; documentar o tamanho do dataset usado (amostra vs. completo).

## Saída esperada
Funções/módulos reutilizáveis em `src/data/` e `src/embeddings/` (ex: `carregar_reviews()`, `limpar_texto()`, `gerar_embeddings()`), com testes básicos de sanidade (shape dos embeddings, contagem de nulos antes/depois).
