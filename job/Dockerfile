FROM python:3.8.8-slim

WORKDIR /app

COPY ./ ./

RUN set -xe \
    && pip install -r requirements.txt

CMD ["python", "main.py"]
