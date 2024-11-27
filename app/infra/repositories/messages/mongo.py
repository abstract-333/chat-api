from dataclasses import dataclass

from domain.entities.messages import Message
from infra.repositories.messages.base import BaseMessagesRepository
from infra.repositories.messages.convertors import convert_message_to_document
from infra.repositories.mongo_base import BaseMongoDBRepository


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={
                "$push": {
                    "messages": convert_message_to_document(message=message),
                },
            },
        )
