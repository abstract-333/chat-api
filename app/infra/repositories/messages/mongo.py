from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatRepository


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def get_chats(self) -> list[Chat]:
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        pass

    async def add_chat(self, chat: Chat) -> None:
        pass
