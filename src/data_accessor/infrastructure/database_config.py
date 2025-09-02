import os
import toml
from typing import Optional
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

class DatabaseConfig:
    def __init__(self, secrets_path: Optional[str] = None):
        """Initialize database configuration with secure handling of credentials.
        
        Args:
            secrets_path: Optional path to secrets file. If None, will search in parent directories.
        """
        self._secrets = self._load_secrets(secrets_path)
        self._initialize_config()

    def _load_secrets(self, secrets_path: Optional[str]) -> dict:
        """Securely load secrets from file or environment variables."""
        if secrets_path is None:
            secrets_path = self._find_secrets_file()
        
        try:
            if not secrets_path or not os.path.exists(secrets_path):
                logger.warning("Secrets file not found, falling back to environment variables")
                return {}
            
            with open(secrets_path, 'r') as f:
                file_content = f.read()
                if len(file_content.strip()) == 0:
                    raise ValueError("Secrets file is empty")
                return toml.loads(file_content)["database"]
        except Exception as e:
            logger.warning("Error loading secrets file, falling back to environment variables")
            return {}

    def _find_secrets_file(self) -> Optional[str]:
        """Safely locate the secrets file in parent directories."""
        current_dir = os.path.dirname(__file__)
        root_dir = os.path.abspath(os.sep)
        
        while current_dir != root_dir:
            potential_path = os.path.join(current_dir, "secrets.toml")
            if os.path.exists(potential_path):
                return potential_path
            current_dir = os.path.dirname(current_dir)
        return None

    def _initialize_config(self) -> None:
        """Initialize configuration with secure defaults."""
        # Use a separate method to validate and store credentials
        self._set_credentials()
        
        # Store non-sensitive configuration
        self._host = self._secrets.get("host", os.getenv("DB_HOST", "localhost"))
        self._port = self._validate_port(
            self._secrets.get("port", os.getenv("DB_PORT", "5432"))
        )
        self._db_name = self._secrets.get("db_name", os.getenv("DB_NAME", "postgres"))

    def _set_credentials(self) -> None:
        """Securely store credentials."""
        self._user = self._secrets.get("user", os.getenv("DB_USER"))
        if not self._user:
            raise ValueError("Database user must be provided")
            
        self._password = self._secrets.get("password", os.getenv("DB_PASSWORD"))
        if not self._password:
            raise ValueError("Database password must be provided")

    @staticmethod
    def _validate_port(port: str) -> int:
        """Validate and convert port number."""
        try:
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                raise ValueError
            return port_num
        except (TypeError, ValueError):
            raise ValueError("Port must be a number between 1 and 65535")

    @property
    def connection_string(self) -> str:
        """Generate a secure connection string with escaped special characters."""
        return (
            f"postgresql+asyncpg://{quote_plus(self._user)}:{quote_plus(self._password)}"
            f"@{self._host}:{self._port}/{self._db_name}"
        )

    def __repr__(self) -> str:
        """Secure string representation that doesn't expose sensitive data."""
        return f"DatabaseConfig(host='{self._host}', port={self._port}, db_name='{self._db_name}')"

    def __str__(self) -> str:
        """Secure string representation that doesn't expose sensitive data."""
        return self.__repr__()
