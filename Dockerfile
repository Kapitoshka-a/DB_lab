FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME

ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]