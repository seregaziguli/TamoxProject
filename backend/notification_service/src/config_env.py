from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL") or "amqp://guest:guest_pass@rabbitmq:5672/"
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL") or "http://auth_service:8000"