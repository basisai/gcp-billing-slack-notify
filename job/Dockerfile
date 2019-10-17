FROM python:3.7

RUN set -xe \
    && pip install google-cloud-bigquery requests pendulum terminaltables

WORKDIR /app
COPY ./ ./

CMD ["python", "main.py"]
