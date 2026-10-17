# Avaliação do pipeline RAG

Gerado em 17/10/2026 15:00 | similaridade mínima: 0.57

| # | Pergunta | Filtros | Escopo esperado | Respondeu? | Reviews usadas | Maior similaridade | Resultado |
|---|---|---|---|---|---|---|---|
| 1 | quais as principais reclamações sobre a entrega? | - | dentro | sim | 20 | 0.73 | OK |
| 2 | quais as reclamações de entrega mais frequentes? | - | dentro | sim | 19 | 0.62 | OK |
| 3 | o produto chegou quebrado ou com defeito? | - | dentro | sim | 23 | 0.81 | OK |
| 4 | os clientes recebem produto diferente do que compraram? | - | dentro | sim | 30 | 0.80 | OK |
| 5 | o que os clientes elogiam na entrega? | - | dentro | sim | 30 | 0.81 | OK |
| 6 | o produto chegou quebrado ou com defeito? | {'$and': [{'review_score': {'$lte': 2}}, {'product_category_name_english': 'furniture_decor'}]} | dentro | sim | 30 | 0.80 | OK |
| 7 | qual a capital da França? | - | fora | não | 0 | - | OK |
| 8 | como está o preço do dólar hoje? | - | fora | não | 0 | - | OK |
| 9 | qual o melhor celular para comprar este ano? | - | fora | não | 0 | - | OK |

## Respostas completas

### 1. quais as principais reclamações sobre a entrega?

Filtros: nenhum

Com base nas avaliações dos clientes, as principais reclamações sobre a entrega estão divididas e ordenadas por frequência (do problema mais mencionado para o menos mencionado):

1. **Demora, atrasos e descumprimento do prazo de entrega (17 clientes)**
   - "DEmora na entrega" (9 clientes) [f065fc6c8703c41424e316207f5261af]
   - "Atraso na entrega" (2 clientes) [a1074ef6728469383f2a8bf58fd98e51]
   - "Demora de entrega" (1 cliente) [7d8d252cc0ae002b13db033ec1cd9dcb]
   - "Demora a entrega" (1 cliente) [ef3905df6593f5fa7faebc82fb85e2e6]
   - "Demora entrega" (1 cliente) [f09b051abf307c8693ad220930fd39cd]
   - "Atrasou a entrega" (1 cliente) [adc92c58a60ad8ab3a9bb76476dc320d]
   - "DEMOROU MUITO A ENTREGA" (1 cliente) [6c05e9a8437ceaf85a6da5f02729fecf]
   - Prazo de entrega não cumprido (1 cliente) [db398c0ddf7b63f9ec7e07a246940d4b]

2. **Qualidade geral insatisfatória, desencontros e problemas com a política de entrega (6 clientes)**
   - "péssima entrega" (2 clientes) [5e728b72bbe8e793ad1c12e93a9fe9aa]
   - "entrega deficiente" (1 cliente) [8390e4ee7ef8df007b81040926af7213]
   - Muitos desencontros nas entregas dos produtos (1 cliente) [949eca021ed60d00a2d2bda3cc686d4d]
   - Problemas com a entrega realizada pelos Correios (1 cliente) [e06d9a717c61331208eabed007431c41]
   - Necessidade de rever a política de entrega (1 cliente) [a6d8671d04e0055b62713f3bfe2c05cd]

3. **Falta de comunicação, informações confusas e ausência de esclarecimentos (4 clientes)**
   - Informações muito confusas sobre a entrega (1 cliente) [256e445ddba830565ad576854f406761]
   - Falta de esclarecimento sobre o atraso da entrega (1 cliente) [8f3d0a9a8a2f00b6363350eaea165c50]
   - Falta de aviso sobre a entrega acompanhada de problemas no processo (1 cliente) [c82e20ab06764504caa5a5754ba2050a]
   - Notificação de problemas na entrega sem detalhamento do ocorrido ou de como resolver, gerando frustração (1 cliente) [57d720a4164ce4e420c120398045fbd0]

4. **Não entrega em domicílio e necessidade de retirada em agência dos Correios mesmo com frete pago (2 clientes)**
   - Pagamento do frete realizado, mas necessidade de ir buscar o produto nos Correios e pagar transporte para isso (1 cliente) [dd6e9d8ecbe106b6eddc67776eae3f5a]
   - Correios não entregaram na residência apesar da taxa paga; ao tentar retirar na agência central, o produto já havia sido devolvido (1 cliente) [0a6843048d2229baf1201b4783d38df3]

5. **Produto avariado/mal embalado na entrega e dificuldades com devolução (1 cliente)**
   - Produto mal embalado, frascos de vidro sem lacre vazando, falta de autorização de devolução solicitada no dia da entrega e transtorno de ter que levar a encomenda aos Correios (1 cliente) [6d096d02c248a56919a9a5a2b1c54e50]

### 2. quais as reclamações de entrega mais frequentes?

Filtros: nenhum

Com base nas avaliações fornecidas, as reclamações relacionadas à entrega, ordenadas da mais frequente para a menos frequente, são:

1. **Demora e atraso na entrega** (mencionado por **21 clientes** no total):
   - "Demora na entrega": **8 clientes** [7ba96f95841f5317463f8a4bba91a879].
   - "Muita demora na entrega": **4 clientes** [72926e5236768ffc912764ca429d0e00].
   - "Atraso na entrega": **2 clientes** [a1074ef6728469383f2a8bf58fd98e51].
   - "DEMOROU MUITO A ENTREGA": **1 cliente** [6c05e9a8437ceaf85a6da5f02729fecf].
   - "Demorando muito a entrega": **1 cliente** [fbd9cc5a7770c84243e9701ac9ac2309].
   - "Demora de entrega": **1 cliente** [7d8d252cc0ae002b13db033ec1cd9dcb].
   - "Demora a entrega": **1 cliente** [ef3905df6593f5fa7faebc82fb85e2e6].
   - "Pessimo muita demora na entrega": **1 cliente** [f02d4978f58368f3346d8450d52f0ba2].
   - Demora de 30 dias com recebimento de e-mails automáticos pedindo mais prazos: **1 cliente** [a7da193f53a190326b28ed511bbf2ad6].
   - Demora na entrega somada à cobrança de frete tendo que retirar nos Correios: **1 cliente** [e71a72bcfcdb675001de2017908c3824].

2. **Problemas com entrega dividida / envio fracionado** (mencionado por **2 clientes** no total):
   - Produtos entregues em dias diferentes gerando dúvidas e reclamações: **1 cliente** [b24256a5bc7d16294b6b9f1965702418].
   - Entrega dividida com nota fiscal no valor total sem aviso prévio ao cliente: **1 cliente** [a8b2ebaa07aacce35cdf3c6e49283a49].

3. **Informações confusas, desatualizadas ou ausentes sobre o status da entrega** (mencionado por **3 clientes** no total com relatos distintos):
   - Status da entrega desatualizado, com indicação de erro e alteração de prazos: **1 cliente** [18fd8314a11f9a00cb85e8ef9aa70042].
   - Informação sobre a entrega considerada muito confusa: **1 cliente** [256e445ddba830565ad576854f406761].
   - Ausência de esclarecimentos sobre o atraso da entrega: **1 cliente** [8f3d0a9a8a2f00b6363350eaea165c50].

4. **Desencontros nas entregas**:
   - Reclamação de muitos desencontros ao entregar os produtos: **1 cliente** [949eca021ed60d00a2d2bda3cc686d4d].

5. **Qualidade geral do serviço de entrega**:
   - Apontada genericamente como "entrega deficiente": **1 cliente** [8390e4ee7ef8df007b81040926af7213].

### 3. o produto chegou quebrado ou com defeito?

Filtros: nenhum

Sim, de acordo com as avaliações dos clientes, os produtos chegaram **tanto com defeito quanto quebrados**. 

Abaixo estão os relatos detalhados, ordenados dos problemas mais frequentes para os menos frequentes:

### 1. Produto com defeito (relatado por 16 clientes no total)
* **4 clientes:** relataram que "O produto veio com defeito" [6d3d6c30e8318a946c8c1f89e577cd7f].
* **3 clientes:** relataram que o "produto veio com defeito" [ea0036b547cb7e145507d50c4d64ce2a].
* **2 clientes:** mencionaram "produto com defeito" [eeafacf5860957c8c7f64dd182586816].
* **1 cliente:** informou que "Infelizmente o produto veio com defeito" [461092fffb45dbaaa8ee1dc23f330d1c].
* **1 cliente:** apontou que "o produto veio com defeito, aparência de usado!" [cc5b0a4875e99b76b467223755d062fd].
* **1 cliente:** relatou que "o produto veio certo mais com defeito" [a645617468c029bce21266286217f6e3].
* **1 cliente:** afirmou que "O produto veio com defeito . Amassado." [2968e46e7843c288808aec153f47c708].
* **1 cliente:** escreveu que "O produto veio co defeito" [13ad6bda4fff6a2c7a90bd1b90a40e65].
* **1 cliente:** relatou que o produto deu defeito e precisou ser encaminhado para a autorizada [00ebb33f82d352f07f0b19e8c6970036].
* **1 cliente:** afirmou que o "produto deu defeito na 1 vez de uso." [8b4c14417bccab81710772ecb8b23fd6].

---

### 2. Produto quebrado ou com partes quebradas (relatado por 9 clientes no total)
* **2 clientes:** relataram que "O produto chegou quebrado" [43bf7d48ee35e1ef767b97badbbe7cd7].
* **1 cliente:** informou que "O produto chegou com uns parte quebrada" [c8b00b8c7a3d22c6e66417bdc3aac0e8].
* **1 cliente:** mencionou que o produto veio correto e no prazo, mas com uma peça quebrada [f6d2fac188b274803aead02ba49f4bfe].
* **1 cliente:** relatou que "o produto veio quebrado" [1f9abf59f4b7b1ccfcb945f669ffad9a].
* **1 cliente:** registrou que "O produto está quebrado" [cb3ac9ac65081886c88485829c53c90b].
* **1 cliente:** declarou que não pôde opinar pois o produto veio quebrado [bb62ebe8f7eaad6812b528ee1f37ef6a].
* **1 cliente:** mencionou que o produto chegou no prazo, porém veio quebrado [9b7f186bdb84e90acc8ac7af8a67016c].
* **1 cliente:** relatou que "O produto estava quebrado." [29978e0295beaafa1d774ee406272040].

### 4. os clientes recebem produto diferente do que compraram?

Filtros: nenhum

Sim, as avaliações confirmam que os clientes frequentemente recebem produtos diferentes dos que compraram. 

Abaixo estão os relatos categorizados e ordenados do mais frequente para o menos frequente:

* **Produto entregue diferente ou divergente do anunciado/comprado (sem detalhamento adicional):** 14 clientes relataram ter recebido um item diferente do que foi solicitado ou apresentado no anúncio [8f451e1cf55dd3f4a5c6e9607a07c561], [c94fe7161f7932281babee672d4b4248], [6651d31e8f40b2444a4601ca46433649], [014552bc1539eed96d4937a07ef1ba03], [0e0b79d9fc0ee15927ba7dc8d4f3918c], [4e7db7d9bdafdd99952285cc366d108a], [6137736e63c63b146f3012dd3419e657], [6f97d8b5afaf78f8658cfc0634840b40], [007f155f02008dd28da584c210767024], [41d35526d3891eb684c6690aa1c85484], [9a9162d4873a41a1b7a4a2ff2e548ba2], [f85ae141a0d912defb1c690f27ce57ce], [e6990ae4b0dbd9d5fab435ebb6aa08c7], [09e543d8be5911076628e46bcf674dfb].
* **Produto entregue diferente e de qualidade inferior:** 3 clientes apontaram que o produto recebido era diferente e de qualidade menor ou baixíssima [c099aafb6db35704451859b711b53425], [a07589e145a10b7428786ce94186b128], [31e60ea253684567293ba02673d47914].
* **Produto entregue com divergência em atributos específicos (cor ou sabor/preço):** 2 clientes indicaram que receberam produtos com variações indevidas, como cor diferente da solicitada [374ff0f46ff482b92a8794eda1c7c47f] ou sabor divergente acompanhado de um produto mais barato [1094606b4d6ef97ac40a3878bc96e609].
* **Divergência que altera o funcionamento do item:** 1 cliente relatou que a diferença entre o item anunciado e o entregue altera o seu funcionamento [4481b7d6375b34d2d6f82151f77c5526].
* **Envio de mercadoria trocada com outro cliente:** 1 cliente informou ter recebido o pedido de outro cliente totalmente diferente do que havia comprado [d08cc40f9017263837bd0e77799d066a].

### 5. o que os clientes elogiam na entrega?

Filtros: nenhum

Com base nas avaliações fornecidas, os clientes elogiam os seguintes aspectos sobre a entrega, ordenados do mais frequente para o menos frequente:

* **Satisfação geral com o processo de entrega (16 clientes):** Clientes declararam estar plenamente satisfeitos ou teceram elogios diretos à entrega e ao recebimento dos pedidos [37c35442208c3077f15ff19e742e0c3e], [715d3f3f7ef4c0d9dc0e8fc2b7d64d3c], [caf2d73f07a603dae1236185169ca715], [e75e500cbc0c72b7630e533d0b548483], [1623821d572c0de4740be6b27aaf0396], [554085c752f6fc356ec5ccddb4e23b29], [b6325f75b3d0eb876d609bb69a56e69d], [8c693221cf18f71764f09a52d2fa529f], [a807ea65e5f33c7fdc436a6e95676660], [f11ce2a6624ecde4d87464b5208ea5c0], [73f8c9bce7d4179b0cd3490d9aaaa61c], [4be01979725f06dfb2de7b1f8a372c01], [2190e26e87feab595fb9a8ef532b5d2e], [cbd645c58b462377d3d6fc829d2bff7b], [7e2ca26a179ce3ffa1b36621a74fd1aa], [eee85a5e7b2b68f4f0d2ded32588dacf].
* **Qualidade, excelência e coerência do serviço de entrega (4 clientes):** Clientes destacaram um serviço de entrega "ótimo", "perfeito" ou coerente com a proposta da empresa [6a817364a1bb1e3a0f509ad6ee9259e5], [bf56c9b8f0664fb20069f5a19a01fab0], [5f99a02c2816238d916b7d4e40bae62c], [1ccbfabdc33d85d527e65a80a68ff4b2].
* **Pontualidade e cumprimento de prazos (2 clientes):** Elogiaram especificamente a entrega dentro do prazo prometido e a pontualidade [6c612bde41f4ce34be1b41efb17aa695], [f2443dba3712367285105aeab6c2d89f].
* **Agilidade na entrega (1 cliente):** Foi elogiada a rapidez e agilidade com que a mercadoria chegou ao consumidor [8c53c47cb8b315b9bf4ec1f704040b05].

### 6. o produto chegou quebrado ou com defeito?

Filtros: {'$and': [{'review_score': {'$lte': 2}}, {'product_category_name_english': 'furniture_decor'}]}

Sim, diversas avaliações confirmam que produtos chegaram quebrados, com defeito ou com avarias. 

Abaixo estão os problemas relatados, ordenados do mais frequente para o menos frequente:

* **Produto quebrado ou com partes quebradas/rachadas (6 clientes):**
  * Produto chegou quebrado [714b8f899b9e039e4fb59ff083935f67], [ea13f408f9f91e78274f1caa2c9663d2] (2 clientes).
  * Produto entregue com uma peça quebrada [f6d2fac188b274803aead02ba49f4bfe] (1 cliente).
  * Produto recebido com a tampa quebrada [b19b3da265d2e2d3f4f18fd77bbba111] (1 cliente).
  * Tampa com rachado e corpo cheio de arranhões [5f3724298f6245ce0866b61e0b403032] (1 cliente).
  * Produto descartável que quebrou no mesmo dia em que foi montado [0edf4a7e5a01cd378c390fc012ee9b98] (1 cliente).

* **Produto com defeito de fábrica ou acabamento (4 clientes):**
  * Produto recebido com defeito / necessitando de troca [eada60766110d984171b1a231c1e3600], [ab2a7a5b86afdac6192523b81cf562b6] (2 clientes).
  * Produto com defeito de fornecedor, apresentando pintura lateral descascada [c3542714507b3198ccc76a6627523dff] (1 cliente).
  * Defeito de acabamento com laterais desfiando e desmanchando [85107a1dcf6d0ecc4e46eba9f50a8efa] (1 cliente).

* **Produto avariado ou amassado (2 clientes):**
  * Produto entregue avariado e com dimensões incorretas [95d9b32ceb14e27ec00467d1792b457e] (1 cliente).
  * Embalagem frágil que veio aberta e causou amassado no produto [aea723bee8f35a61b8738007d38010a0] (1 cliente).

### 7. qual a capital da França?

Filtros: nenhum

Não encontrei avaliações de clientes suficientes na base da Olist para responder a essa pergunta.

### 8. como está o preço do dólar hoje?

Filtros: nenhum

Não encontrei avaliações de clientes suficientes na base da Olist para responder a essa pergunta.

### 9. qual o melhor celular para comprar este ano?

Filtros: nenhum

Não encontrei avaliações de clientes suficientes na base da Olist para responder a essa pergunta.
