import cv2
import base64
import numpy as np

from typing import Optional, Union

from cv2.typing import MatLike
from fastapi import UploadFile

VALID_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def file_validation(file: UploadFile) -> Union[UploadFile, None]:
    filename: Optional[str] = file.filename
    if filename:
        ext = filename.split(".")[-1]

        if ext.lower() not in VALID_EXTENSIONS:
            return None
        return file
    return None


def decode_to_matlike(file_bytes: bytes) -> MatLike:
    """Convert uploaded image to opencv matlike object

    Args:
        file (UploadFile): Uploaded image

    Returns:
        MatLike: Opencv Matlike Image (Matrix of uint8)
    """
    numpy_array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    return image
