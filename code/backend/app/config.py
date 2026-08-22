from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"

settings = Settings()
