# Jogo da Forca - Aplicação Web

Este projeto é uma aplicação web desenvolvida em Django, com o objetivo de criar um "Jogo da Forca" interativo, onde professores podem cadastrar temas e palavras, e alunos podem jogar de acordo com essas definições.

## Funcionalidades

### Para Professores
- Cadastro e autenticação na aplicação.
- Inserção de novas palavras e temas para serem usados no jogo.
- Possibilidade de adicionar texto e dicas opcionais para cada palavra.
- Geração de relatórios sobre quais alunos jogaram, filtrando por tema e período de tempo.
- Geração de PDF das atividades para impressão.

### Para Alunos
- Jogar sem precisar se cadastrar ou logar no sistema.
- Possibilidade de cadastro caso seja exigido pelo professor.
- Escolher jogos filtrando por tema ou professor.

## Tecnologias Utilizadas
- **Python 3.12**: Linguagem principal utilizada no backend.
- **Django**: Framework web para desenvolvimento rápido e seguro.
- **HTML/CSS/JavaScript**: Para a construção do frontend e interação com o jogo.
- **MySQL**: Banco de dados utilizado no desenvolvimento local.

## Instalação e Execução

### Pré-requisitos

Antes de iniciar, certifique-se de ter o Python 3.12 instalado em sua máquina. Você pode baixar o Python [aqui](https://www.python.org/downloads/).

### Passo a Passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/wand-CE/jogo_da_forca.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd jogo_da_forca
   ```

   Este projeto utiliza um arquivo `.env` para armazenar variáveis de ambiente sensíveis. Para configurá-lo:
   1. Copie o arquivo `.envbase` para `.env`:

      ```bash
      cp ./jogo_da_forca/.envbase ./jogo_da_forca/.env
      ```
   2. Preencha os campos no arquivo .env com suas configurações.
   3. Se precisar de uma nova SECRET_KEY, gere uma usando o shell do Django:
      ```bash
      python manage.py shell
      ```
      Após abrir o shell execute:
      ```bash
      from django.core.management.utils import get_random_secret_key
      print(get_random_secret_key())
      ```
      Após isso copie a chave gerada e cole no arquivo .env.

4. Crie e ative um ambiente virtual com o Python:

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows use: venv\Scripts\activate
   ```

5. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```
   
6. Execute as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

7. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

8. Acesse a aplicação em `http://127.0.0.1:8000`.

9. Aproveite!!!

## Interface do Aplicativo

![image](https://github.com/user-attachments/assets/b1574ebf-315e-4333-bcb4-5cad09c308b9)

