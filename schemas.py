from pydantic import BaseModel

class ImageData(BaseModel):
    name: str
    type: str
    b64Image: str
