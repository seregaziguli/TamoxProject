FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env
COPY ./src /app/src

ENV PYTHONPATH=/app

CMD ["python", "-u", "-m", "src.main"]
