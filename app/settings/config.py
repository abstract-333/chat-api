from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    mongodb_connection_uri: str = Field(alias='MONGO_DB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGO_DB_CHAT_DATABASE')
    mongodb_chat_collection: str = Field(
        default='chat', alias='MONGO_DB_CHAT_COLLECTION'
    )
    mongodb_message_collection: str = Field(
        default='messages', alias='MONGO_DB_MESSAGE_COLLECTION'
    )

    debug: bool = Field(alias='DEBUG', default=True)
