# Usar a imagem oficial do Python como base
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app
COPY main.py /app
COPY .env /app
COPY client.json /app

COPY /source /app/source
COPY /exe /app/exe

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
