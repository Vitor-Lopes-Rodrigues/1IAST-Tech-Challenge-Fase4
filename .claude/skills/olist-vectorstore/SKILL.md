---
name: olist-vectorstore
description: Use ao conectar, indexar ou consultar o banco vetorial do projeto Olist RAG (FAISS, ChromaDB, Qdrant ou similar). Acionar para tarefas em src/vectorstore/, criação de índices, busca por similaridade, ou armazenamento de metadados junto dos vetores.
---

# Olist Vectorstore

Esta skill cobre a parte de indexação do pilar **Construção da Base de Conhecimento** e dá suporte à **Busca Semântica** do pipeline RAG (ver `CLAUDE.md`).

## Quando usar
- Criar/atualizar índices vetoriais a partir dos embeddings gerados em `src/embeddings/`.
- Implementar busca por similaridade (cosseno ou produto interno, conforme normalização).
- Persistir e carregar o índice em disco (evitar reprocessar embeddings a cada execução).
- Expor filtragem por metadados (score, data, categoria, status de entrega) junto da busca vetorial.

## Diretrizes

1. **Escolha de tecnologia**: FAISS para prototipação local rápida e simples; ChromaDB ou Qdrant quando precisar de filtragem por metadados nativa e persistência mais robusta. Justificar a escolha no README.
2. **Consistência de métrica**: se os embeddings foram normalizados (`normalize_embeddings=True`), o índice deve usar similaridade de cosseno (ou produto interno, que é equivalente após normalização) — não misturar métricas.
3. **Metadados obrigatórios**: cada vetor indexado deve manter o vínculo com `review_id`, `review_score`, data e demais metadados definidos em `olist-data-prep`, para permitir rastreabilidade das respostas e filtragem.
4. **Código em `src/vectorstore/`**: funções como `criar_indice()`, `buscar_similares(query, k, filtros=None)`, `salvar_indice()`, `carregar_indice()`. Nunca deixar essa lógica presa em notebook.
5. **Tratamento de exceções**: falhas de conexão com o banco vetorial (quando remoto, ex: Qdrant) devem ser capturadas e relatadas com mensagem clara, nunca travar a aplicação sem explicação.
6. **Performance**: para datasets grandes (~40 mil reviews), evitar recomputar embeddings/índice a cada execução — cachear em disco e documentar o processo de atualização incremental, se houver.

## Saída esperada
Módulo em `src/vectorstore/` que recebe embeddings + metadados e expõe uma função de busca por similaridade com filtros opcionais, usada pelo pipeline RAG (`olist-rag-pipeline`).
