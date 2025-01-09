# Usar a imagem oficial do Python como base
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app
COPY teste.py /app
COPY .envtest /app
COPY client.json /app

COPY /src /app/src

RUN pip install -r requirements.txt

CMD ["python", "teste.py"]
