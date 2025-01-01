from random import randrange

import pygame as pg

BLACK = pg.Color(0, 0, 0)
BLUE = pg.Color(0, 0, 255)
GREEN = pg.Color(0, 255, 0)
RED = pg.Color(255, 0, 0)
WHITE = pg.Color(255, 255, 255)


class Stars:
    MAX_STARS = 250
    STAR_SPEED = 2

    COLORS = (WHITE, WHITE, WHITE, BLUE, RED, GREEN)

    def __init__(self, width: int, height: int) -> None:
        """Create the starfield"""
        stars = []
        for i in range(Stars.MAX_STARS):
            # A star is represented as a list with this format: [X,Y]
            star = pg.Vector2(randrange(0, width - 1), randrange(0, height - 1))
            stars.append(star)
        self.stars = stars

    def render(self, screen: pg.Surface) -> None:
        """Move and draw the stars in the given screen"""
        # shortcuts to speed up access
        COLORS = self.COLORS
        NB = len(COLORS)
        for i, star in enumerate(self.stars):
            color = self.COLORS[i % NB]
            # pg.draw.circle(screen, color, (star[0], star[1]), 1)
            pg.draw.circle(screen, color, star, 1)

    def update(self, height: int) -> None:
        """Move and draw the stars in the given screen"""
        # shortcuts to speed up access
        velocity = self.STAR_SPEED
        for star in self.stars:
            star.y += velocity
            if star.y >= height:
                star.y = 0
                star.x = randrange(0, 639)  # respawn


def main():
    WIDTH, HEIGHT = 640, 480
    title = "Starfield Simulation"
    clock = pg.Clock()

    screen = pg.display.set_mode((WIDTH, HEIGHT))
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

        stars.update(HEIGHT)

        screen.fill(BLACK)
        stars.render(screen)
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
