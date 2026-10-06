---
name: olist-evaluator
description: Use ao validar respostas do RAG Olist contra as evidências recuperadas, para evitar alucinação, ou ao avaliar a qualidade do pipeline (precisão da busca, cobertura, casos sem resposta). Acionar antes de finalizar respostas no pipeline e ao escrever testes/avaliações do sistema.
---

# Olist Evaluator

Esta skill cobre o pilar **Tratamento de Falta de Evidências (Prevenção de Alucinação)** e dá suporte à validação de qualidade geral do RAG (ver `CLAUDE.md`).

## Quando usar
- Antes de uma resposta do pipeline ser enviada ao usuário: verificar se há evidências suficientes e relevantes.
- Ao escrever testes/avaliações do sistema RAG (precisão da busca semântica, taxa de alucinação, cobertura de perguntas fora do escopo).
- Ao definir thresholds de similaridade mínima para considerar uma evidência "relevante".

## Diretrizes

1. **Regra de ouro**: se a busca semântica não retornar reviews com similaridade acima de um threshold mínimo (definir e documentar o valor, ex: calibrado empiricamente), ou se as evidências forem insuficientes/contraditórias, a resposta final **deve** declarar explicitamente que não há informações suficientes na base — nunca inventar ou extrapolar.
2. **Fora do escopo**: perguntas que não se referem a avaliações de clientes da Olist (ex: perguntas gerais, sobre outras empresas) devem ser identificadas e respondidas com uma recusa clara, não uma tentativa de resposta genérica.
3. **Checagem de citação**: toda resposta gerada pelo pipeline (`olist-rag-pipeline`) deve ser validada quanto a conter pelo menos uma citação de evidência (`review_id`/trecho) por afirmação relevante. Se não houver, rejeitar/reformular antes de entregar ao usuário.
4. **Métricas de avaliação sugeridas**:
   - Precisão@k da busca semântica em um conjunto de perguntas de teste com resposta esperada conhecida.
   - Taxa de respostas que corretamente declaram "sem evidência suficiente" quando a pergunta é fora do escopo (testar com perguntas propositalmente fora do dataset).
   - Revisão manual de amostra de respostas vs. evidências citadas (checar se o trecho citado realmente sustenta a afirmação).
5. **Local do código**: validadores e scripts de avaliação ficam em `src/pipeline/` (validação em tempo de execução) e podem ter um script/notebook de avaliação dedicado em `notebooks/` para rodar a avaliação em lote — mas a lógica de validação usada em produção deve estar em `src/`, não só no notebook.
6. **Documentar limitações conhecidas** (ex: dataset desbalanceado por score, amostragem usada) no README, para transparência sobre quando o sistema pode falhar.

## Saída esperada
Função de validação (ex: `validar_evidencias(resposta, evidencias, threshold) -> bool`) usada pelo pipeline antes de retornar a resposta final, mais um conjunto de casos de teste (perguntas dentro e fora do escopo) para avaliação contínua.
