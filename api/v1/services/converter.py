import cv2

from cv2.typing import MatLike
from typing import List, Union


def downscale(image: MatLike, new_width: int) -> MatLike:
    """Reduce image size so pixels match required number of characters

    Args:
        image (MatLike): source image
        new_width (int): required number of chars

    Returns:
        MatLike: Reduced image
    """
    new_width = new_width // 2
    old_height, old_width, _ = image.shape

    aspect_ratio = old_height / old_width

    new_height = int(aspect_ratio * new_width)
    new_width = int(new_width * 2)

    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def get_ascii_from_pixel_intensity(pixel_intensity: int, ramp_choice: str) -> str:
    """Pick ascii character from a character ramp using pixel intensity

    Args:
        pixel_intensity (int): Pixel intensity value
        ramp_choice (str): Ramp to pick chars from

    Returns:
        str: selected char
    """
    RAMPS = {
        "block": " ░▒▓█",
        "smooth": "▁▂▃▄▅▆▇█",
        "basic": " .:-=+*#%@",
    }

    selected_ramp = RAMPS[ramp_choice]

    map_length = len(selected_ramp)

    # Normalize pixel_intensity to 0-1 range, then scale to map_length
    map_index = int((pixel_intensity / 255.0) * (map_length - 1))

    return selected_ramp[map_index]


def ascii_html_string(buffer: List[List[dict]]) -> str:
    rows = []
    for row in buffer:
        row_chars = "".join(
            f"<span style='color: {pixel['color']};'>{pixel['char']}</span>"
            for pixel in row
        )
        rows.append(row_chars)
    return "<br>".join(rows)


def ascii_raw_string(buffer: List[List[str]]) -> str:
    """convert 2D string buffer into one newline seperated string

    Args:
        buffer (List[List[str]]): 2D string buffer
    Returns:
        str: Result string
    """
    return "\n".join("".join(row) for row in buffer)


def generate_ascii(
    source_image: MatLike,
    ramp_choice: str,
    image_width: int,
    colored: bool,
) -> List[List[Union[str, dict]]]:
    """Generate ascii art from an image

    Args:
        source_image (MatLike): Image to convert
        ramp_choice (str): Ascii character ramp
        image_width (int): number of characters per line

    Returns:
        List[List[str]]: 2D buffer containing generated ascii art
    """
    source_image_width = source_image.shape[1]

    if source_image_width > image_width:
        source_image = downscale(image=source_image, new_width=image_width)

    grayscale_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

    # 2D buffer
    result_buffer: List[List[Union[str, dict]]] = []

    for y, grayscale_row in enumerate(grayscale_image):
        row = []
        for x, pixel_intensity in enumerate(grayscale_row):
            ascii_char = get_ascii_from_pixel_intensity(pixel_intensity, ramp_choice)

            if colored:
                # Get the original BGR values from the source image
                blue, green, red = source_image[y, x]
                pixel_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
                pixel_data = {"char": ascii_char, "color": pixel_hex}
            else:
                pixel_data = ascii_char

            row.append(pixel_data)
        result_buffer.append(row)

    return result_buffer
