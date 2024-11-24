from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    KAFKA_BROKER: str = "kafka:9092"
    KAFKA_TOPIC: str = "insurance_logs"

    class Config:
        env_file = ".env"


settings = Settings()
