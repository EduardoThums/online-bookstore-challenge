# Online Bookstore Challenge

RESTful API developed as a solution for the [challenge](https://github.com/bravosul/back-end-challenge) proposed by [Bravosul](https://bravosul.com.br/) company.

## Technologies
- Python
- Flask
- MongoDB
- Docker


## Requirements
- [Python](https://www.python.org/)
- [PIP (Python package manager)](https://pypi.org/project/pip/)
- [Virtualenv](https://packaging.python.org/key_projects/#virtualenv)
- [Docker](https://docs.docker.com/desktop/) and [Docker Compose](https://docs.docker.com/compose/install/)


## How to use
1. Create a file named ```.env``` in the root project directory and add these variables on it:
```
MONGODB_HOST=localhost
SECRET_KEY=YOUR-SECRET-KEY
```

2. Create a virtual environment and install the project dependencies:
```
python -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```

3. In the root project directory run the underneath command to start the API and database locally:
```
make run-api
```

## Documentation
An example of all available routes is located in the ```resources/``` directory as an [Insomnia](https://insomnia.rest/) JSON file.
