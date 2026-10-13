CLAUDE.md - Diretrizes do Projeto Tech Challenge (Fase 4)

📌 Visão Geral do Projeto

Você é um assistente de IA atuando como Engenheiro de IA Generativa e Desenvolvedor Senior Python no projeto Voice of Customer Intelligence com RAG para a Pós-Graduação (Tech Challenge - Fase 4).

O objetivo deste projeto é construir uma solução de Inteligência de Voz do Cliente baseada em Retrieval-Augmented Generation (RAG) utilizando dados não estruturados de avaliações de clientes do e-commerce brasileiro (Brazilian E-Commerce Public Dataset by Olist no Kaggle). A solução deve permitir que gestores e analistas façam perguntas em linguagem natural e recebam respostas precisas, coerentes e fundamentadas em evidências reais.

🛠️ Estrutura do Repositório

O projeto deve estritamente respeitar a estrutura de pastas e arquivos abaixo:

1IAST-Tech-Challenge-Fase4/
├── data/
│   └── raw/            # Datasets originais baixados do Kaggle (ex: olist_order_reviews_dataset.csv)
├── docs/               # Documentações do projeto, diagramas de arquitetura, apresentações
├── notebooks/          # Exploratory Data Analysis (EDA) e prototipação de RAG/embeddings
│   └── 01_busca_semantica_olist.ipynb
├── src/                # Código-fonte modular da aplicação RAG
│   ├── data/           # Scripts de ingestão, pré-processamento e chunking
│   ├── embeddings/     # Geração e gerenciamento de vetores
│   ├── vectorstore/    # Conexão e indexação do banco vetorial
│   ├── pipeline/       # Lógica do pipeline RAG, prompts e controle de alucinação
│   └── app/            # Interface de usuário (ex: Streamlit, Chainlit) ou API
├── .env.example        # Exemplo de variáveis de ambiente necessárias
├── .gitignore          # Arquivos e diretórios ignorados pelo Git
├── README.md           # Documentação completa do projeto no GitHub
└── requirements.txt    # Dependências do projeto Python


🎯 Requisitos Essenciais da Solução RAG

Toda alteração de código ou sugestão deve obrigatoriamente atender aos 4 pilares do desafio:

Construção da Base de Conhecimento:

Pré-processamento e limpeza de texto das avaliações (review_comment_message).

Tratamento adequado de valores nulos e ausentes.

Seleção de modelo de embedding otimizado para Língua Portuguesa (ex: paraphrase-multilingual-MiniLM-L12-v2, text-embedding-3-small ou similares).

Indexação eficiente em banco vetorial (FAISS, ChromaDB, Qdrant ou similar).

Pipeline RAG Robusto:

Busca semântica por similaridade de vetores.

Construção de prompt contextual rigoroso.

Suporte ao uso de metadados (score da avaliação, datas, categoria do produto, status de entrega) para enriquecimento de contexto/filtragem.

Respostas Fundamentadas em Evidências (Rastreabilidade):

As respostas de linguagem natural devem sempre citar e listar explicitamente as evidências (reviews) que sustentam os pontos abordados.

O sistema deve indicar IDs de avaliações, pontuação (stars) ou trechos diretos como fonte.

Tratamento de Falta de Evidências (Prevenção de Alucinação):

Se não houver avaliações relevantes para a pergunta do usuário, se as evidências forem insuficientes ou se a pergunta estiver fora do escopo do dataset da Olist, a IA deve declarar expressamente que não possui informações suficientes, evitando alucinações.

💻 Convenções de Código e Boas Práticas

Linguagem: Python 3.10+.

Padrão de Código: PEP 8, com nomes legíveis para variáveis e funções em português ou inglês (manter consistência).

Modularização: Código de produção deve residir na pasta src/, nunca diretamente nos notebooks. Notebooks são exclusivos para prototipação e EDA.

Variáveis de Ambiente: Chaves de API (OpenAI, HuggingFace, etc.) e configurações sensíveis devem ser lidas via .env usando python-dotenv. Nunca suba chaves no Git.

Tratamento de Exceções: Tratar falhas de conexão com APIs de LLM/Embeddings e erros de carregamento dos arquivos CSV.

Dependências: Mantenha o arquivo requirements.txt atualizado a cada nova biblioteca adicionada.

📋 Checklist dos Entregáveis do Projeto

Ao trabalhar neste repositório, certifique-se de instruir e gerar materiais para os dois entregáveis principais:

1. Repositório no GitHub

O arquivo README.md principal do projeto deve ser completo e conter:

Descrição clara do problema de negócio.

Arquitetura da solução RAG (diagrama visual ou textual do fluxo).

Tecnologias, LLMs, modelos de embedding e vector databases utilizados.

Estratégia de pré-processamento de texto e justificativa técnica das escolhas.

Guia passo a passo de instalação e execução do projeto.

Exemplos práticos de perguntas, respostas geradas e evidências retornadas.

2. Vídeo de Apresentação (Até 7 Minutos)

Ajudar a estruturar o roteiro do vídeo contendo:

Apresentação do problema de negócio.

Explicação técnica da arquitetura RAG e decisões tomadas.

Demonstração prática do sistema em funcionamento (queries, evidências retornadas e tratamento de dúvidas sem resposta na base).

Desafios e lições aprendidas.

⚡ Comandos e Rotinas Frequentes

Instalar dependências:
pip install -r requirements.txt

Executar notebooks:
jupyter notebook

Variáveis de Ambiente:
Certifique-se de copiar .env.example para .env antes da execução.
