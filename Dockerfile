# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc libpq-dev \
    libcairo2 libcairo2-dev libpangocairo-1.0-0 weasyprint \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only poetry files to install deps first (to leverage Docker cache)
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]

