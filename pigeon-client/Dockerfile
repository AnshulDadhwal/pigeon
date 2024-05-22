FROM ubuntu:22.04
# Installing dependencies for running a python application
RUN apt-get update && apt-get install -y build-essential python3 python3-pip
# Install pipenv
RUN pip3 install poetry
# Setting the working directory
WORKDIR /app
# Install pipenv dependencies
COPY pyproject.toml ./
RUN poetry install --no-root
# Copying our application into the container
COPY pigeon-client pigeon-client

# Running our application
# TODO:
CMD ["bash", "-c", "sleep 10 && poetry run python pigeon-client/__init__.py"]

# FROM ubuntu:22.04
# # Installing dependencies for running a python application
# RUN apt-get update && apt-get install -y build-essential python3 python3-pip
# # Install pipenv
# RUN pip3 install poetry
# # Setting the working directory
# WORKDIR /app
# # Install pipenv dependencies
# COPY pyproject.toml ./
# RUN poetry install --no-root
# # Copying our application into the container
# COPY client client

# # Running our application
# # TODO:
# CMD ["bash", "-c", "sleep 10 && poetry run flask --app spamoverflow run --host 0.0.0.0 --port 8080"]
