---
name: olist-rag-pipeline
description: Use ao construir ou alterar o pipeline RAG do projeto Olist — orquestração entre busca semântica, construção de prompt contextual e geração de resposta pelo LLM, com citação obrigatória de evidências. Acionar para tarefas em src/pipeline/ e src/app/.
---

# Olist RAG Pipeline

Esta skill cobre o pilar **Pipeline RAG Robusto** e **Respostas Fundamentadas em Evidências** (ver `CLAUDE.md`).

## Quando usar
- Orquestrar o fluxo: pergunta do usuário → busca semântica (`olist-vectorstore`) → construção de prompt → chamada ao LLM → resposta formatada.
- Definir e ajustar o template de prompt contextual.
- Implementar suporte a filtros por metadados (score, data, categoria, status de entrega) na busca antes de montar o contexto.
- Formatar a resposta final citando explicitamente as evidências usadas.

## Diretrizes

1. **Prompt contextual rigoroso**: o prompt enviado ao LLM deve instruir explicitamente a responder **apenas** com base nas reviews recuperadas, sem usar conhecimento externo sobre a Olist ou inventar fatos.
2. **Rastreabilidade obrigatória**: toda resposta deve listar as evidências usadas — `review_id`, `review_score` e um trecho direto da review. Nunca gerar uma afirmação sem apontar a evidência correspondente.
3. **Metadados como contexto**: quando a pergunta do usuário mencionar (explícita ou implicitamente) período, categoria de produto ou status de entrega, aplicar filtros na busca (`olist-vectorstore`) antes de montar o prompt — não confiar só na similaridade semântica pura.
4. **Modularização**: lógica de pipeline em `src/pipeline/` (ex: `montar_prompt()`, `gerar_resposta()`, `formatar_evidencias()`); interface de usuário (Streamlit/Chainlit/API) em `src/app/`, consumindo o pipeline — nunca duplicar lógica de negócio na camada de UI.
5. **Tratamento de exceções**: falhas na chamada ao LLM (timeout, rate limit, erro de API) devem ser capturadas e retornar uma mensagem de erro amigável ao usuário, nunca um stack trace.
6. **Chaves de API**: ler sempre via `.env`/`python-dotenv`; nunca hardcode nem logar chaves.
7. **Delegar a decisão de "sem evidência suficiente"** para a skill `olist-evaluator` — este pipeline deve chamar essa validação antes de gerar a resposta final.

## Saída esperada
Função/pipeline único (ex: `responder(pergunta: str) -> RespostaRAG`) que retorna texto da resposta + lista estruturada de evidências (review_id, score, trecho), pronta para ser exibida na UI.
