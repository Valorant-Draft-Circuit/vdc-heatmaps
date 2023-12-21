from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MODEL_")

    # endpoint: str
    # region: str
    # aws_access_key_id: str
    # aws_secret_access_key: str
    # s3_bucket: str
    environment: str = "testing"

    @property
    def is_testing(self) -> bool:
        return self.environment == "testing"

    @property
    def is_dev(self) -> bool:
        return self.environment == "development"

    @property
    def is_prod(self) -> bool:
        return self.environment == "production"
