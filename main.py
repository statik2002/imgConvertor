import io

import requests
from PIL import Image


def convert_image(unconverted_image: Image, fixed_image_size: int = 480) -> Image:
    width, height = unconverted_image.size
    new_image = Image.new('RGB', (fixed_image_size, fixed_image_size), (255, 255, 255))

    if width >= height:
        width_percent = (fixed_image_size / float(unconverted_image.size[0]))
        width_size = int((float(unconverted_image.size[0]) * float(width_percent)))
        height_size = int((float(unconverted_image.size[1]) * float(width_percent)))
        temp_image = unconverted_image.resize((width_size, height_size))
        new_image.paste(temp_image, (0, int(fixed_image_size / 2 - temp_image.size[1] / 2)))

    elif width < height:
        height_percent = (fixed_image_size / float(unconverted_image.size[1]))
        width_size = int((float(unconverted_image.size[0]) * float(height_percent)))
        height_size = int((float(unconverted_image.size[1]) * float(height_percent)))
        temp_image = unconverted_image.resize((width_size, height_size))
        new_image.paste(temp_image, (int(fixed_image_size / 2 - temp_image.size[0] / 2), 0))

    return new_image


def main() -> None:
    data = {
        "code1c": 19596
    }

    response = requests.get('https://neit.ru/api/v1/goods/get_good/', data=data, verify=False, timeout=6000)

    if response.status_code == 200:
        remote_product = response.json()
        if len(remote_product.get('images')) < 1:
            print(f'For product with code: {data.get("code1c")} have no images.')

        else:
            for image in remote_product.get('images'):
                img = requests.get(f'https://neit.ru{image.get("image")}', verify=False)
                image_name = image.get('image').split('/')[-1]
                if img.status_code == 200:
                    fetching_image = Image.open(io.BytesIO(img.content))
                    converted_image = convert_image(fetching_image)
                    converted_image.save(f'{image_name.split(".")[0]}.webp', 'webp')


if __name__ == '__main__':
    main()
