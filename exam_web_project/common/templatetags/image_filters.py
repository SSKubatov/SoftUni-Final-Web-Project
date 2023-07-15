from django import template
from PIL import Image

register = template.Library()


@register.filter()
def resize_image(image_url, size):
    image_path = image_url.path
    image = Image.open(image_path)
    image.thumbnail(size, Image.ANTIALIAS)
    resized_image_path = f"{image_path}_resized.png"
    image.save(resized_image_path)
    return resized_image_path
