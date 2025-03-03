# Using a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app #inside the container

# Copy project files (only what's needed)
COPY etl/	/app/etl/
COPY tests/	/app/tests/
COPY config/	/app/config/
COPY data/	/app/data/
COPY dags/	/app/dags/
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y
RUN pip install --no-cache -r requirements.txt

# Set to run DAG Script
#CMD ["python", "/app/dags/***.py"]