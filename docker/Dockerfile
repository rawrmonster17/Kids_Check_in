FROM python:3.11

WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the contents of the app directory directly into /app
COPY app/ /app/

# Copy SQL script to the appropriate directory
COPY docker/server.sql /docker-entrypoint-initdb.d/

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
