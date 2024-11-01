FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "/app/src/main.py"]