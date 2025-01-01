"""
https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
"""

import pygame as pg
from pygame.typing import ColorLike

white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)


class MySysFont:
    def __init__(self, name: str, size: int):
        self.font = pg.font.SysFont(name, size)

    def render(
        self, text: str, color: ColorLike, bgcolor: ColorLike = None
    ) -> pg.Surface:
        surface = self.font.render(text, True, color, bgcolor)
        return surface

    def render_outline(
        self,
        text: str,
        color: ColorLike,
        outline_color: ColorLike,
        bgcolor: ColorLike = None,
        thickness: int = 2,
    ) -> pg.Surface:
        surf1 = self.render(text, outline_color, bgcolor)
        rect1 = surf1.get_rect()
        surf2 = self.render(text, color, bgcolor)
        surface = pg.Surface((surf1.width + 2, surf1.height + 2), pg.SRCALPHA)

        x, y = surface.get_rect().center
        for dx, dy in (
            (-thickness, -thickness),
            (+thickness, -thickness),
            (-thickness, +thickness),
            (+thickness, +thickness),
        ):
            rect1.center = (x + dx, y + dy)
            surface.blit(surf1, rect1)
        rect = surface.get_rect()
        rect.center = (x, y)
        surface.blit(surf2, rect)
        return surface

    def render_outline2(
        self,
        text: str,
        color: ColorLike,
        outline_color: ColorLike,
        bgcolor: ColorLike = None,
        thickness: int = 2,
    ) -> pg.Surface:
        surface = self.font.render(text, True, color).convert_alpha()
        mask = pg.mask.from_surface(surface)
        mask_surf = mask.to_surface(setcolor=outline_color)
        mask_surf.set_colorkey((0, 0, 0))

        new_img = pg.Surface(
            (surface.get_width() + thickness, surface.get_height() + thickness)
        )
        color_key = (255, 0, 255)
        new_img.fill(color_key)
        new_img.set_colorkey(color_key)

        for i in range(-thickness, thickness):
            new_img.blit(mask_surf, (i + thickness, thickness))
            new_img.blit(mask_surf, (thickness, i + thickness))
        new_img.blit(surface, (thickness, thickness))

        return new_img


def main():
    win = pg.display.set_mode((800, 600))
    pg.display.set_caption("font outline demo")

    font = MySysFont("Impact", 80)
    text = font.render_outline("World", "red", "yellow", thickness=4)
    text2 = font.render_outline2("Other method", "yellow", "blue", thickness=4)

    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False

        win.fill("lightblue")
        win.blit(text, (200, 150))
        win.blit(text2, (200, 250))
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
