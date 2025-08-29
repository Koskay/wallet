FROM python:3.12.2-alpine



ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap


RUN pip install --upgrade pip

ADD requirements.txt /app
ADD pyproject.toml /app

RUN pip install -r requirements.txt

COPY . /app/
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh