from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from application.api.messages.schemas import (
    CreateChatInSchema,
    CreateChatOutSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from logic.exceptions.messages import ChatNotFoundException
from logic.init import init_container
from logic.mediator import Mediator
from utils.uuid_4 import get_uuid4


router = APIRouter(tags=["Chat"], prefix="/chat")


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    description="Create new chat, if chat with current name exists, it will raise 400 status code",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatOutSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatInSchema,
    container: Container = Depends(dependency=init_container),
) -> CreateChatOutSchema:
    """Create New Chat"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(
            command=CreateChatCommand(title=schema.title),
        )

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return CreateChatOutSchema.from_entity(chat=chat)


@router.post(
    path="/{chat_oid}/message",
    status_code=status.HTTP_201_CREATED,
    description="Add new message to chat, if chat not exists, it will raise 404 status code",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateMessageSchema,
            "content": {
                "application/json": {
                    "example": {"id": get_uuid4(), "title": "Message Example"},
                },
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "error": f"Chat with this oid {get_uuid4()} not found",
                        },
                    },
                },
            },
        },
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Create New Message"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid),
        )
    except ChatNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": exception.message},
        ) from exception
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception
    return CreateMessageResponseSchema.from_entity(message=message)
