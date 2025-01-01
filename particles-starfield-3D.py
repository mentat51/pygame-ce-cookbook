from dataclasses import dataclass
from random import randrange

import pygame as pg

BLACK = pg.Color(0, 0, 0)
BLUE = pg.Color(0, 0, 255)
GREEN = pg.Color(0, 255, 0)
RED = pg.Color(255, 0, 0)
WHITE = pg.Color(255, 255, 255)


@dataclass(slots=True)
class Star:
    x: int
    y: int
    z: int


class Stars:
    MAX_STARS = 250
    MAX_DEPTH = 32

    __slots__ = ("stars", "width", "height")

    def __init__(self, width: int, height: int) -> None:
        """Create the starfield"""
        stars = []
        MAX_DEPTH = self.MAX_DEPTH
        for i in range(Stars.MAX_STARS):
            # A star is represented as a list with this format: [X,Y,Z]
            star = Star(randrange(-25, 25), randrange(-25, 25), randrange(1, MAX_DEPTH))
            stars.append(star)
        self.stars: list[Star] = stars
        self.width: int = width
        self.height: int = height

    def render(self, screen: pg.Surface) -> None:
        """Move and draw the stars in the given screen"""
        origin_x = self.width / 2
        origin_y = self.height / 2
        MAX_DEPTH = self.MAX_DEPTH
        for star in self.stars:
            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star.z
            x = int(star.x * k + origin_x)
            y = int(star.y * k + origin_y)

            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.width and 0 <= y < self.height:
                size = int((1 - float(star.z) / MAX_DEPTH) * 5)
                shade = (1 - float(star.z) / MAX_DEPTH) * 255
                # self.screen.fill((shade,shade,shade),(x,y,size,size))
                pg.draw.rect(screen, (shade, shade, shade), (x, y, size, size))

    def update(self) -> None:
        """Move and draw the stars in the given screen"""
        MAX_DEPTH = self.MAX_DEPTH
        for star in self.stars:
            # the z component is decreased on each frame
            star.z -= 0.19

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star.z <= 0:
                star.x = randrange(-25, 25)
                star.y = randrange(-25, 25)
                star.z = MAX_DEPTH


def main():
    WIDTH, HEIGHT = 960, 540
    title = "3D Starfield Simulation"
    clock = pg.Clock()

    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED)
    pg.display.set_caption(title)

    stars = Stars(WIDTH, HEIGHT)

    run = True
    while run:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_f:
                    pg.display.toggle_fullscreen()

        stars.update()

        screen.fill(BLACK)
        stars.render(screen)
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
