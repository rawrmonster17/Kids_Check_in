Kids Check-In System
Overview

The Kids Check-In System is a FastAPI-based application designed to manage the check-in and check-out of kids. It allows users to create records for kids and parents, link parents to kids, and retrieve lists of kids and parents. The application is built to be scalable and uses PostgreSQL as the database.
Table of Contents

    Features
    Installation
        Prerequisites
        Setup
    Running the Application
    API Endpoints
    Testing with Postman
    Database Initialization
    Docker Compose

Features

    Create records for kids and parents.
    Link parents to kids.
    Retrieve lists of kids and parents with pagination.
    Retrieve kids linked to a specific parent.

Installation
Prerequisites

    Docker
    Docker Compose
    Python 3.11
    PostgreSQL

Setup

    Clone the repository:

bash

git clone <repository-url>
cd KIDS_CHECK_IN

    Create a virtual environment and activate it:

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    Install the dependencies:

bash

pip install -r requirements.txt

Running the Application
Using Docker Compose

    Navigate to the docker directory:

bash

cd docker

    Build and start the Docker services:

bash

docker-compose up --build

    Access the application at http://localhost:8000.

Without Docker

    Set up and start PostgreSQL:

Ensure PostgreSQL is running and create a database named kids.

    Set the DATABASE_URL environment variable:

bash

export DATABASE_URL=postgresql://<username>:<password>@localhost/kids

    Initialize the database:

bash

python app/db.py

    Start the FastAPI application:

bash

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

API Endpoints
Create a New Kid

    URL: /kids/
    Method: POST
    Request Body:

    json

    {
      "first_name": "John",
      "last_name": "Doe",
      "allergies": "Peanuts",
      "checked_in": true
    }

    Response: Created kid record with ID

Create a New Parent

    URL: /parents/
    Method: POST
    Request Body:

    json

    {
      "first_name": "Jane",
      "last_name": "Doe",
      "phone_number": "123-456-7890",
      "email": "jane.doe@example.com"
    }

    Response: Created parent record with ID

Link Parent to Kid

    URL: /parent_kid/
    Method: POST
    Request Body:

    json

    {
      "parent_id": 1,
      "kid_id": 1
    }

    Response: Linked parent and kid

Get List of Kids

    URL: /kids/
    Method: GET
    Query Parameters:
        skip: (Optional) Number of records to skip for pagination.
        limit: (Optional) Maximum number of records to return.
    Response: List of kids

Get List of Parents

    URL: /parents/
    Method: GET
    Query Parameters:
        skip: (Optional) Number of records to skip for pagination.
        limit: (Optional) Maximum number of records to return.
    Response: List of parents

Get Kids Linked to a Parent

    URL: /parent_kids/{parent_id}
    Method: GET
    Path Parameters:
        parent_id: ID of the parent.
    Response: List of kids linked to the specified parent

Testing with Postman

    Create Environment:
        Create a new environment in Postman with a variable base_url set to http://localhost:8000.

    Create Requests:

        Create a New Kid:
            Method: POST
            URL: {{base_url}}/kids/
            Body: Raw JSON

        json

{
  "first_name": "John",
  "last_name": "Doe",
  "allergies": "Peanuts",
  "checked_in": true
}

Create a New Parent:

    Method: POST
    URL: {{base_url}}/parents/
    Body: Raw JSON

json

{
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "123-456-7890",
  "email": "jane.doe@example.com"
}

Link Parent to Kid:

    Method: POST
    URL: {{base_url}}/parent_kid/
    Body: Raw JSON

json

        {
          "parent_id": 1,
          "kid_id": 1
        }

        Get List of Kids:
            Method: GET
            URL: {{base_url}}/kids/

        Get List of Parents:
            Method: GET
            URL: {{base_url}}/parents/

        Get Kids Linked to a Parent:
            Method: GET
            URL: {{base_url}}/parent_kids/{parent_id}

    Execute Requests:
        Use the requests in Postman to interact with the FastAPI application and verify functionality.

Database Initialization

The database is initialized using the server.sql file located in the docker directory. This file is automatically executed when the PostgreSQL container starts.
Docker Compose

The docker-compose.yml file sets up the services required for the application:

    db: PostgreSQL database service
    web: FastAPI application service

Both services are connected to a custom network to facilitate communication.
Example docker-compose.yml

yaml

version: '3.9'

services:
  db:
    image: postgres:alpine3.20
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: kids
    volumes:
      - ../pgdata:/var/lib/postgresql/data
      - ./server.sql:/docker-entrypoint-initdb.d/server.sql
    ports:
      - "5432:5432"
    networks:
      - app-network

  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: fastapi_app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ../app:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - app-network

networks:
  app-network: