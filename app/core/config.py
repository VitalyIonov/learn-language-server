from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import model_validator


def _build_database_uri(scheme: str, user: str, password: str, host: str, port: int, db: str) -> str:
    return str(
        MultiHostUrl.build(
            scheme=scheme,
            username=user,
            password=password,
            host=host,
            port=port,
            path=db,
        )
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    LOGIN_REDIRECT_URL: str
    LOGOUT_REDIRECT_URL: str

    OPENAI_API_KEY: str
    SECRET_KEY: str

    database_uri: str = ""
    sync_database_uri: str = ""

    @model_validator(mode="after")
    def _set_database_uris(self) -> "Settings":
        self.database_uri = _build_database_uri(
            scheme="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            db=self.POSTGRES_DB,
        )
        self.sync_database_uri = _build_database_uri(
            scheme="postgresql+psycopg2",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            db=self.POSTGRES_DB,
        )
        return self

    SESSION_SECRET_KEY: str
    DEEPL_API_KEY: str
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET: str
    R2_PUBLIC_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str


settings = Settings()
