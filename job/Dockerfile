FROM python:3.8.8-slim

RUN set -xe \
    && pip install google-cloud-bigquery requests pendulum terminaltables

WORKDIR /app
COPY ./ ./

CMD ["python", "main.py"]
