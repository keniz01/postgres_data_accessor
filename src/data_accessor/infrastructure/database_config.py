import os
import toml

class DatabaseConfig:
    def __init__(self, secrets_path=None):
        # Default path to secrets file
        if secrets_path is None:
            secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db_secrets.toml")
        try:
            secrets = toml.load(secrets_path)["database"]
        except Exception:
            secrets = {}
            
        self.user = secrets.get("user", os.getenv("DB_USER", "postgres"))
        self.password = secrets.get("password", os.getenv("DB_PASSWORD", "password"))
        self.host = secrets.get("host", os.getenv("DB_HOST", "localhost"))
        self.port = secrets.get("port", os.getenv("DB_PORT", "5432"))
        self.db_name = secrets.get("db_name", os.getenv("DB_NAME", "postgres"))

    @property
    def connection_string(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
