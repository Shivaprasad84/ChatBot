import base64
import uuid
from pathlib import Path

def save_image(file_name: str, file_type: str, b64image: str):
    image_bytes = base64.b64decode(b64image.encode("ascii"))
    image_path: Path = Path('images') / Path(f'{file_name}.{file_type}') # image.bmp
    image_path.write_bytes(image_bytes)
    return uuid.uuid4().hex


def get_b64_image(image_name: str):
    data = Path(f'images/{image_name}').read_bytes()
    b64data = base64.b64encode(data).decode('ascii')
    return b64data
