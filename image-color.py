"""
https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen?rq=3
"""

import sys
import pygame as pg


def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pg.Color(r, g, b, a))


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()

    # Uncomment this for a non-translucent surface.
    # surface = pg.Surface((100, 150), pg.SRCALPHA)
    # pg.draw.circle(surface, pg.Color(40, 240, 120), (50, 50), 50)
    surface = pg.image.load("assets/bullet2.png").convert_alpha()
    surface = pg.transform.rotozoom(surface, 0, 2)

    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_f:
                    fill(surface, pg.Color(240, 200, 40))
                if event.key == pg.K_g:
                    fill(surface, pg.Color(250, 10, 40))
                if event.key == pg.K_h:
                    fill(surface, pg.Color(40, 240, 120))

        screen.fill(pg.Color("lightskyblue4"))
        pg.draw.rect(screen, pg.Color(40, 50, 50), (210, 210, 50, 90))
        screen.blit(surface, (200, 200))

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
