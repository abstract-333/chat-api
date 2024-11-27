from dataclasses import dataclass

from domain.entities.messages import Chat
from infra.repositories.chats.base import BaseChatsRepository
from infra.repositories.chats.convertors import convert_chat_to_document
from infra.repositories.mongo_base import BaseMongoDBRepository


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: Chat) -> None:
        collection = self._collection()

        await collection.insert_one(convert_chat_to_document(chat))
