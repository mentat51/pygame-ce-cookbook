from dataclasses import dataclass
from pathlib import Path

import pygame as pg


@dataclass(slots=True)
class Text:
    font:pg.Font
    text:str
    texture_path:Path
    surface:pg.Surface=None

    def __post_init__(self):
        text_surface = self.font.render(self.text, True, 'white') #, None, wraplength:int=0)
        texture = pg.image.load(self.texture_path)
        i = 0
        while i < text_surface.get_width():
            text_surface.blit(texture, (i, 0), special_flags=pg.BLEND_RGB_MULT)
            i += texture.get_width()
        self.surface = text_surface

    def render(self, screen:pg.Surface, pos:pg.typing.Point):
        screen.blit(self.surface, pos)


def main():
    size = (960, 720)
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Textured text')

    BG_COLOR = pg.Color("gray32")

    texture = Path("assets/textures/nick-fewings-unsplash.jpg")
    font = pg.Font(None, 295)
    text = Text(font, "Textured", texture)
    text2 = Text(font, "text", texture)

    print(text.font.get_point_size())

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        screen.fill(BG_COLOR)
        text.render(screen, (50, 170))
        text2.render(screen, (240, 370))
        pg.display.flip()


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
