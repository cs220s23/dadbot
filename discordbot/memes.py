from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests
from io import BytesIO

templates = {
    "winning": "pic/are_ya_winning.png"
}

with requests.Session() as s:
    r = s.get("https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue-Angular/ComicNeueAngular-Regular.ttf")
    defaultFont = ImageFont.truetype(BytesIO(r.content), 65) if r.ok else None


def compose_image(base: Image, top: Image, pos: (int, int)) -> Image:
    result = Image.new("RGBA", (base.size[0], base.size[1]))
    result.paste(base)
    result.paste(top, pos)
    return result


def add_text(img: Image, text: str, pos: (int, int) = (0, 0), font=defaultFont,
             color: (int, int, int) = (0, 0, 0)) -> None:
    added_text = ImageDraw.Draw(img)
    added_text.text(pos, text, font=font, fill=color)


def winning(avatar: Image, text: str) -> Image:
    with Image.open(templates["winning"]) as base:
        avatar_resize = avatar.resize((200, 200))
        result = compose_image(base, avatar_resize, (520, 130))
        add_text(result, text, (420, 340))

    return result
