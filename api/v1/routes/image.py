from cv2.typing import MatLike
from fastapi import APIRouter, status, UploadFile, Query, HTTPException
from sse_starlette.sse import EventSourceResponse
from celery.result import AsyncResult
from typing import Optional
import asyncio

from api.utils import image_utils
from api.v1.schemas import image as image_schema
from api.core.dependencies.celery.tasks import ascii_generator_task
from api.core.dependencies.celery.celery_app import worker

image_router = APIRouter(prefix="/image", tags=["Ascii Generator"])


@image_router.post(
    path="/upload",
    status_code=status.HTTP_200_OK,
    response_model=image_schema.AsciiTaskStartResponse,
    summary="Generate ascii art from image",
    description="This endpoint takes a photo and some query parameters to generate an ascii representation of the image",
    tags=["Ascii Generator"],
)
async def upload(
    file: UploadFile,
    width: int = Query(default=150),
    character_set: str = Query(default="basic"),
    is_colored: bool = Query(default=False),
):
    image_file: Optional[UploadFile] = image_utils.file_validation(file)

    if not image_file:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Supported files include {', '.join(image_utils.VALID_EXTENSIONS)}",
        )

    file_bytes = await image_file.read()

    task: AsyncResult = ascii_generator_task.delay(
        file_bytes, character_set, width, is_colored
    )

    return image_schema.AsciiTaskStartResponse(
        task_id=str(task.id),
        message="ASCII art generation started!",
        status_code=status.HTTP_200_OK,
    )


@image_router.get(path="/tasks/{task_id}/stream")
async def stream_task_status(task_id: str):
    async def event_generator():
        while True:
            task_result = worker.AsyncResult(task_id)
            if task_result.ready():
                yield {"event": "complete", "data": str(task_result.result)}
                break
            else:
                yield {"event": "progress", "data": "Processing"}
            await asyncio.sleep(1.5)

    return EventSourceResponse(event_generator())
