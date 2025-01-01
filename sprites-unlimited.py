"""
Name    :    unlimited 'bobs' - korruptor, http://www.korruptor.demon.co.uk
Desc    :

I first saw this in the Dragons MegaDemo on the A500 back in '89 and it blew me away.
How gutted I was when Wayne "tripix" Keenan told me how easy it was and knocked up an
an example demo a couple of years later.

For those of you that didn't know how it was done, here's a pygame example. It's
basically a flick-book effect; you draw the same sprite in different positions on
25 different 'screens' and flick between them. When you've drawn on all 25 you loop
back to the beginning and keep on blitting.

Sprite offsets make it look like you're adding sprites. Simple.
"""

from math import cos, sin

import pygame as pg


class Bobs:
    PI = 3.14159
    DEG2RAD = PI / 180

    __slots__ = ("surfaces", "bob", "x_angle", "y_angle", "index")

    def __init__(self, screen: pg.Surface) -> None:
        self.surfaces: list[pg.Surface] = []
        # load a sprite and set the palette
        self.bob = pg.image.load("assets/bob.gif")
        self.bob.set_colorkey((255, 255, 255))

        # Create 25 blank surfaces to draw on.
        for i in range(0, 25):
            self.surfaces.append(pg.Surface(screen.size))

        self.x_angle: float = 0.0
        self.y_angle: float = 0.0
        self.index: int = 0

    def update(self):
        width, height = pg.display.get_window_size()
        # Get some x/y positions
        x = (width / 2) * sin((self.x_angle * Bobs.DEG2RAD) * 0.75)
        y = (height / 2) * cos((self.y_angle * Bobs.DEG2RAD) * 0.67)

        # Inc the angle of the sine
        self.x_angle += 1.17
        self.y_angle += 1.39

        # blit our 'bob' on the 'active' surface
        self.surfaces[self.index].blit(
            self.bob, (x + (width / 2) - 32, y + (height / 2) - 32)
        )

    @property
    def surface(self):
        _surface = self.surfaces[self.index]
        # inc the active surface number
        self.index = (self.index + 1) % 25
        return _surface


def main():
    RES = (480, 400)

    screen = pg.display.set_mode(RES, 0)

    clock = pg.time.Clock()

    bobs = Bobs(screen)

    run = True
    while run:
        # Have we received an event to quit the program?
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_f:
                    pg.display.toggle_fullscreen()

        bobs.update()

        # blit the active surface to the screen
        screen.blit(bobs.surface, (0, 0))

        # display the results
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
