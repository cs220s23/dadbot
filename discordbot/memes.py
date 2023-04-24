from PIL import Image, ImageDraw, ImageFont

import requests
import textwrap
import os


templates = {
    "winning": "pic/are_ya_winning.png"
}

try:
    defaultFont = ImageFont.truetype("pic/ComicNeueAngular-Regular.ttf", 50)
except IOError:
    with requests.Session() as s:
        r = s.get("https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue-Angular/ComicNeueAngular-Regular.ttf")
        with open("pic/ComicNeueAngular-Regular.ttf", 'wb') as f:
            f.write(r.content)
        defaultFont = ImageFont.truetype("pic/ComicNeueAngular-Regular.ttf", 50)


def compose_image(base: Image, top: Image, pos: (int, int)) -> Image:
    result = Image.new("RGBA", (base.size[0], base.size[1]))
    result.paste(base)
    result.paste(top, pos)
    return result


def winning(avatar: Image, text: str, name: str = None) -> Image:
    with Image.open(templates["winning"]) as base:
        text = textwrap.fill(text, 17)
        avatar_resize = avatar.resize((200, 200))
        result = compose_image(base, avatar_resize, (520, 130))
        draw = ImageDraw.Draw(result)
        draw.text((610, 380), text, font=defaultFont, fill="black", anchor="mm")
        if name and len(name) < 11:
            draw.rectangle([(140, 60),(225, 80)], fill="white")
            name_font = ImageFont.truetype(defaultFont.path, 25)
            draw.text((140, 60), name, font=name_font, fill="black")

    return result
