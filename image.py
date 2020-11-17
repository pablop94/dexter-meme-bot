import sys
import requests

from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from settings import BASE_PATH, IMAGES_FOLDER, FONT_PATH


FONT = ImageFont.truetype(FONT_PATH, 20)

def crear_meme_desde_url(url):
    response = requests.get(url)
    return crear_meme(BytesIO(response.content))

def crear_meme_desde_archivo(path):
    return crear_meme(path)


def crear_meme(foreground_image_path):
    background = Image.open(BASE_PATH).copy()
    foreground = Image.open(foreground_image_path)
    foreground = foreground.convert("RGBA")

    foreground = foreground.resize((240, 240), Image.LANCZOS)
    width, height = foreground.size

    deltaX = 153
    deltaY = 100
    foreground = foreground.transform((width, height), Image.QUAD,
            (-deltaX, -deltaY, -deltaX+5, height+deltaY-5, width, height, width, 0), Image.BICUBIC)

    background.paste(foreground, (165, 20), foreground)

    return background

def agregar_texto(texto, imagen):
    TEXT_LINE_LENGTH = 38
    WHITE_SPACE_HEIGHT = 75
    TEXT_MARGIN = (20, 5)

    newimage = imagen.copy()
    white_image = Image.new('RGB', (imagen.size[0], imagen.size[1]+WHITE_SPACE_HEIGHT), (255,255,255))
    draw = ImageDraw.Draw(white_image)

    new_text = _break_by_text_length(texto, TEXT_LINE_LENGTH)
    #text begins at top left
    draw.multiline_text(TEXT_MARGIN, new_text, (0, 0, 0), font=FONT)
    white_image.paste(newimage, (0, WHITE_SPACE_HEIGHT))
    
    return white_image

def _break_by_text_length(texto, length):
    import textwrap
    """Converts a long string into a string with the specified length, inserting line breaks between the chunks"""
    return '\n'.join(textwrap.wrap(texto, length))

