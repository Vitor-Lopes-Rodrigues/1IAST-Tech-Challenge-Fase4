# Pipeline RAG – geração de respostas (`src/pipeline/`)

Esta etapa usa o banco vetorial (ChromaDB) para responder perguntas em linguagem natural sobre as avaliações da Olist, sempre citando as evidências e recusando quando não há base suficiente.

## Fluxo

```
Pergunta do gestor
   ↓
1. Busca semântica: as 30 reviews mais parecidas (buscar_similares, com filtros opcionais)
   ↓
2. Threshold: descarta reviews com similaridade < 0,57
   → se não sobrar nenhuma: responde "não encontrei" SEM chamar o LLM
   ↓
3. Agrupa reviews com texto idêntico e conta quantos clientes escreveram cada uma
   ↓
4. Monta o prompt (regras + reviews com nota, categoria e contagem)
   ↓
5. Gemini gera a resposta citando os [review_id]
   ↓
6. Retorna a resposta + lista de evidências (review_id, nota, similaridade, ocorrências, trecho)
```

## Como executar

```powershell
# 1. Preparar a base (uma vez)
python -m src.data.download_data
python -m src.data.preprocess
python -m src.vectorstore.chroma_store

# 2. Configurar a chave: copiar .env.example para .env e preencher GOOGLE_API_KEY

# 3. Fazer perguntas
python -m src.pipeline.rag

# 4. Rodar a avaliação (gera docs/avaliacao_rag.md)
python -m src.pipeline.avaliar
```

## Decisões técnicas

| Decisão | Valor | Justificativa |
|---|---|---|
| LLM | `gemini-3.7-flash` | Rápido e com cota gratuita. O `gemini-2.5-flash` não está mais disponível para contas novas, e o `gemini-3.8-flash` (primeira escolha) esgotou a cota diária do nível gratuito durante os testes. Configurável via `GEMINI_MODEL` no `.env`, sem alterar o código. |
| Temperatura | 0 | Respostas mais determinísticas e factuais, menos "criatividade". |
| Reviews buscadas (k) | 30 | Com k = 8 a resposta trazia só "atraso"; com mais reviews aparecem outros tipos de problema. Como textos idênticos são agrupados, buscamos mais para sobrar variedade. |
| Similaridade mínima | 0,57 | Calibrada com testes. Pior caso dentro do escopo: 0,616 ("quais as reclamações de entrega mais frequentes?"). Pior caso fora do escopo: 0,558 ("como está o preço do dólar hoje?"). O valor inicial de 0,62 gerou falsos negativos e foi recalibrado. |
| Agrupamento de repetidas | texto normalizado (minúsculas, sem pontuação) | Muitos clientes escrevem a mesma frase curta ("Demora na entrega" aparece 8x). Agrupar libera espaço no prompt e a contagem permite ordenar os problemas por frequência. |
| Filtros por metadados | nota máxima e categoria | Sintaxe `where` do ChromaDB (ex.: `{"review_score": {"$lte": 2}}`), combinados com `$and`. |

## Prevenção de alucinação (duas camadas)

1. **Threshold de similaridade:** perguntas fora do escopo (ex.: "qual a capital da França?") não encontram reviews acima de 0,57 e são recusadas antes de chamar o Gemini.
2. **Regras no prompt:** o modelo deve usar apenas as reviews fornecidas, citar o `[review_id]` de cada afirmação e responder com a frase padrão de recusa quando as reviews não forem suficientes. Isso cobre casos que passam pelo threshold mas não respondem à pergunta (ex.: uma review elogiando a entrega numa pergunta sobre reclamações é ignorada).

## Limitações conhecidas

- **Margem pequena no threshold:** a diferença entre o pior caso dentro (0,616) e fora (0,558) do escopo é de só 0,06. O threshold sozinho não separa perfeitamente; por isso existe a segunda camada.
- **Viés em perguntas genéricas:** em "Quais são os principais problemas relatados pelos clientes?", as reviews mais parecidas são as que contêm a palavra "cliente" (ex.: "falta de respeito com o cliente"), e esse tema aparece como o mais frequente, embora atraso na entrega seja mais comum na base. A busca mede semelhança de texto, não frequência real. Melhoria futura: reescrever a pergunta em várias buscas concretas (multi-query) antes de recuperar.
- **Filtros reduzem o universo de busca:** com nota ≤ 2, a pergunta 9 da avaliação recuperou só 3 reviews acima do threshold, e a resposta ficou rasa.
- **A forma de perguntar influencia a busca:** "reclamações sobre a entrega" (0,73) e "reclamações de entrega mais frequentes" (0,62) trazem similaridades diferentes.
- **O agrupamento só junta textos idênticos:** "Demora na entrega" e "Demorou muito a entrega" continuam separados. Agrupar por sentido exigiria comparar embeddings.
- **Sem filtro por data:** a data está gravada como texto no ChromaDB, que só compara números. Exigiria reindexar com a data numérica.
- **Uma review pode cair em mais de um tópico** da resposta, então os totais por tópico não somam o total de clientes.
- **Cota do nível gratuito do Gemini:** cerca de 20 chamadas por dia por modelo. Uma rodada completa de `avaliar.py` usa 12. Ao atingir o limite, a API retorna erro 429 (`RESOURCE_EXHAUSTED`); o pipeline mostra a mensagem do erro e mantém as evidências. Cada integrante deve usar a própria chave.
- **A nota nem sempre bate com o texto:** há reviews nota 5 com reclamação, o que reforça o valor de analisar o texto.

## Resultados

Ver `docs/avaliacao_rag.md`, gerado por `python -m src.pipeline.avaliar`: 15 perguntas (11 exemplos do enunciado, 1 teste com filtro combinado e 3 fora do escopo), todas com o resultado esperado.
