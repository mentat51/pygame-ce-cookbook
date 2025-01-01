"""
https://stackoverflow.com/questions/56209634/is-it-possible-to-change-sprite-colours-in-pygame
"""

import pygame as pg


def changColor(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)

    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pg.BLEND_MULT)
    return finalImage


def main():
    window = pg.display.set_mode((300, 160))

    image = pg.image.load("assets/CarWhiteDragon256.png").convert_alpha()
    hue = 0

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False

        color = pg.Color(0)
        color.hsla = (hue, 100, 50, 100)
        hue = hue + 1 if hue < 360 else 0

        color_image = changColor(image, color)

        window.fill((96, 96, 64))
        window.blit(color_image, color_image.get_rect(center=window.get_rect().center))
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
