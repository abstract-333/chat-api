from application.api.messages.schemas import (CreateChatInSchema,
                                              CreateChatOutSchema)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from logic.commands.messages import CreateChatCommand
from logic.init import init_container
from logic.mediator import Mediator

router = APIRouter(
    tags=["Chat"],
)


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
    container=Depends(dependency=init_container),
):
    """Create New Chat"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(
            command=CreateChatCommand(title=schema.title)
        )

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateChatOutSchema.from_entity(chat=chat)
