# builder
FROM python:3.11.1-alpine3.17 as builder

WORKDIR /workdir/src
RUN pip install --upgrade pip && pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt > requirements.txt

# runtime
FROM python:3.11.1-alpine3.17 as runtime
WORKDIR /workdir/src
COPY --from=builder /workdir/src/requirements.txt ./
RUN pip install -r ./requirements.txt
COPY src/python/main ./src/python/main

CMD ["python", "src/python/main/main.py"]
