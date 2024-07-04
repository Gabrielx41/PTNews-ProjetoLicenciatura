# PTNews
## Visão geral
Este repositório contém o projeto PTNews desenvolvido como projeto final de Licenciatura de Engenharia Informática da UBI. O projeto tem como objetivo a extração de notícias de 11 fontes diferentes, disponibilização das notícias e estatísticas das mesmas.
## Inicialização da Extração dos Dados
* python3 -m PTNews_Script.iniciar
## Estrutura do Projeto
### PTNews_Script
* Dados: Contém os dados em ficheiros JSON.
* Ficheiros: Contém as operações de manipulação de ficheiros.
* GetDados: Contém as operações para extração de dados.
* Jornais: Contém as operações de gerenciamento de cada fonte de noticias.
* Redis: Contém as operações do redis.
* Request: Contém a função de request.
* Sentimentos: Contém as operações para análise de sentimentos.
* Token: Contém o ficheiro de inicialização/paragem do script.
* UltimosID: Contém os últimos id's das últimas notícias recolhidas.
* Uteis: Contém funções úteis para a extração dos dados.
* iniciar.py: Inicialização do script para incializar a extração de dados.
* main.py: Ficheiro main do script (operações de gerenciamento do script).

### PTNews
O website onde os utilizadores podem aceder ás notícias recolhidas e ás respetivas estatísticas.
* grafo: Contém a função para criar o grafo.
* redis_utils: Contém as operações do redis.
* static: Contém os dados estáticos: imagens, css, js.
* templates: Contém todos os ficheiros HTML utilizados na construção do website. 

## Fontes de Notícias Utilizadas
* ECO
* Público
* Observador
* Jornal i
* Jornal de Negócios
* Expresso
* Notícias ao Minuto
* Diário de Notícias
* Renascença
* Sapo24
* SIC Notícias
## Tecnologias Utilizadas
![Python](https://img.shields.io/badge/Python-42.9%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-30.3%25-yellow)
![CSS](https://img.shields.io/badge/CSS-14.9%25-purple)
![HTML](https://img.shields.io/badge/HTML-11.9%25-red)

## Clone o Repositório:
```bash
   git clone https://github.com/Gabrielx41/PTNews-ProjetoLicenciatura.git
```
## Contacto
Para quaisquer questões ou problemas, abra um 'issue' no repositório ou contacte gabriel.lazaro@ubi.pt.
