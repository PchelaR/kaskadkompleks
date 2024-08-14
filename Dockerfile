FROM python:3.12.4

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt