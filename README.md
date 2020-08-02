# Online Bookstore Challenge

API RESTful criada como solução para o [desafio](https://github.com/bravosul/back-end-challenge) proposto pela empresa [Bravosul](https://bravosul.com.br/).

## Tecnologias
- Python
- Flask
- MongoDB
- Docker

---

## Requisitos
- [Python](https://www.python.org/)
- [PIP (Python package manager)](https://pypi.org/project/pip/)
- [Virtualenv](https://packaging.python.org/key_projects/#virtualenv)
- [Docker](https://docs.docker.com/desktop/) e [Docker Compose](https://docs.docker.com/compose/install/)

---

## Como usar
1. Na raiz do projeto crie um arquivo chamado ```.env``` e adicione as variavies abaixo:
```
MONGODB_HOST=localhost
SECRET_KEY=YOUR-SECRET-KEY
```
2. Crie um ambiente virtual e instale as depencias do projeto:

```
python -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```

3. Na raiz do projeto rode o comando abaixo para iniciar a API e o banco de dados localmente:
```
make run-api
```
---

# Documentação
Um exemplo com todas as rotas está disponivel no formato json para o [Insomnia](https://insomnia.rest/) no diretório ```resources/```.
