FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN ["pip", "install", "--requirement", "requirements.txt"]
