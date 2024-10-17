from pydantic import BaseModel

from domain.entities.messages import Chat


class CreateChatInSchema(BaseModel):
    title: str


class CreateChatOutSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatOutSchema":
        return CreateChatOutSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )
