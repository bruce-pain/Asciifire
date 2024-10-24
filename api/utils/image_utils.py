import cv2
import numpy as np

from typing import Union

from cv2.typing import MatLike
from fastapi import UploadFile, HTTPException

VALID_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def file_validation(file: UploadFile) -> Union[UploadFile, None]:
    filename = file.filename
    ext = filename.split(".")[-1]

    if ext.lower() not in VALID_EXTENSIONS:
        return None
    return file


async def decode_to_matlike(file: UploadFile) -> MatLike:
    """Convert uploaded image to opencv matlike object

    Args:
        file (UploadFile): Uploaded image

    Returns:
        MatLike: Opencv Matlike Image (Matrix of uint8)
    """
    contents = await file.read()
    numpy_array = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    return image
