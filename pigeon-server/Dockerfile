FROM --platform=linux/amd64 python:3.10

ENV SQLALCHEMY_DATABASE_URI=postgresql://administrator:verySecretPassword@database:5432/server 

RUN pip3 install poetry

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-root

COPY bin bin
COPY server server

ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["serve"]