from fastapi import APIRouter, status, UploadFile, Query, HTTPException

from api.utils import image_utils
from api.v1.services import converter
from api.v1.schemas import image as image_schema

image_router = APIRouter(prefix="/image", tags=["Ascii Generator"])


@image_router.post(
    path="/upload",
    status_code=status.HTTP_200_OK,
    response_model=image_schema.AsciiResultResponse,
    summary="Generate ascii art from image",
    description="This endpoint takes a photo and some query parameters to generate an ascii representation of the image",
    tags=["Ascii Generator"],
)
async def upload(
    image_file: UploadFile,
    width: int = Query(default=150),
    character_set: str = Query(default="basic"),
):
    image_file = image_utils.file_validation(image_file)

    if not image_file:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Supported files include {', '.join(image_utils.VALID_EXTENSIONS)}",
        )

    image_object = await image_utils.decode_to_matlike(file=image_file)

    result_buffer = converter.generate_ascii(
        source_image=image_object, ramp_choice=character_set, image_width=width
    )

    result_string = converter.ascii_raw_string(buffer=result_buffer)

    return image_schema.AsciiResultResponse(
        result=result_string,
        message="Ascii art generated successfully",
        status_code=status.HTTP_200_OK,
    )
