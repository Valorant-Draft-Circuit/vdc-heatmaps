FROM python:3.12.0-alpine AS development

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev
RUN apk update && \ 
    apk add git

# # Install missing packages
# RUN pip install pipx

# Set the necessary environment variables for poetry to work.
ENV POETRY_VERSION=1.6.0
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# WORKDIR ${PATH}/vdc-fastapi

# Install Poetry
# Use pip for the installation to avoid any virtual environment issues. Do not change to pipx unless a fix is found.
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

# Set the working directory
# Copy the application code
COPY . usr/local/vdc-fastapi

# Create a new project using Poetry
# RUN poetry new vdc-fastapi
 

# Uncomment once the project is being copied from github or the files below are currently present in the local directory.
# COPY pyproject.toml poetry.lock /vdc-fastapi/

# Install dependencies
# RUN poetry install


# Start the application
# After initial code is present for the fastapi to be able to properly run the app.
# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]