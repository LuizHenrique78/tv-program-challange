# tv-program-challange

A arquitetura do projeto está divididas em camadas, 
- application -> onde fica os endpoints / cronjob / outras entradas
- cross -> dependencias gerais 
- domain -> interfaçe / serviços / entidades
- infra -> implementação das interfaces

obs. Toda estrutura está preparada para injeção de dependencias. Mas não implementei essa feature por conta de tempo.

Isso da a possibilidade de utilizarmos n connexçoes com o banco ou outras formas de importar os arquivos CSV.

Nessa implementação estou utilizando redis como banco temporario e a amazon s3 para buscar o CSV que será carregado, mas há possibiliidade de ter varias outras implementaçoes.

# Ambiente

Dentro de um cluster kubernetes a ideia é ter um cronjob configurado para rodar todo dia em uma data especifica, Assim como ter o server do fast api rodandno como micro-serviço.

