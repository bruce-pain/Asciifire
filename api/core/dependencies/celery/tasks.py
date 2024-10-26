from typing import List

from api.core.dependencies.celery.celery_app import worker
from api.v1.services import converter
from api.utils import image_utils


@worker.task(name="ascii_generator_task")
def ascii_generator_task(
    file_bytes: bytes,
    ramp_choice: str,
    image_width: int,
):
    source_image = image_utils.decode_to_matlike(file_bytes)

    result_buffer: List[List[str]] = converter.generate_ascii(
        source_image, ramp_choice, image_width
    )

    return converter.ascii_raw_string(result_buffer)
