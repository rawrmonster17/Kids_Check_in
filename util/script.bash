#!/bin/bash

# Define container and database variables
CONTAINER_NAME="postgres"
DB_USER="postgres"
DB_NAME="kids"

# Execute SQL queries inside the PostgreSQL container
sudo docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "SELECT * FROM kids;"
sudo docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "SELECT * FROM parents;"
sudo docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "SELECT * FROM parent_kid;"
