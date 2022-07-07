import uvicorn

from color_deconvolution import eosin_channel, hematoxylin_channel
from core import create_app
from schemas import ImageData
from utils import get_b64_image, save_image

app = create_app()
images = dict()


@app.get('/HematoxylinImage')
def get_hematoxylin_image(image_id: str):
    image_name, image_type = images.get(image_id)
    image = hematoxylin_channel(image_name, image_type)
    b64Image = get_b64_image(image)
    return {'b64Image': b64Image}


@app.get('/EosinImage')
def get_eosin_image(image_id):
    image_name, image_type = images.get(image_id)
    image = eosin_channel(image_name, image_type)
    b64Image = get_b64_image(image)
    return {'b64Image': b64Image}


@app.post('/upload')
async def upload(data: ImageData):
    name = data.name
    type = data.type.split('/')[1]
    image_id = save_image(name, type, data.b64Image)
    images[image_id] = (name, type)
    return {
        "message": "Successfully uploaded image",
        "imageId": image_id
    }


def main():
    uvicorn.run('app:app', host='localhost', port=5010, reload=True)


if __name__ == '__main__':
    main()
