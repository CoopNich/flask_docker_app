## About This App
This is a CRUD application created with Python/Flask and wrapped in a Docker container. It was created to test and learn Docker containerization. 

### Technologies Used
    Python
    PyTest
    Flask
    SQLAlchemy
    Postgress
    Docker

## Instructions for Installation and Testing

Be sure that you have [Docker](https://www.docker.com) installed and running

Clone this repo on your personal machine using the following command in your terminal

```sh
    git clone git@github.com:coopnich/flask_docker_app.git
```

cd into the root folder of the project, then build your container and run it on your localserver with the following command

```sh
    docker-compose up -d --build
```
### Flask Admin
Once the container is spun up, you can visit http://localhost:5001/admin/budgetitem/ to interact with the Flask Admin GUI to interact with the database and use CRUD functionality. 

### PyTest
PyTest is also available for running tests on the project/tests/test_budget_item.py file

```sh
    docker-compose exec budget_items python -m pytest "project/tests"
```
