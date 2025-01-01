"""
https://pythonprogramming.altervista.org/a-screensaver-with-fireworks-in-pygame/
"""

from dataclasses import dataclass
import random

import pygame as pg


@dataclass(slots=True)
class Particle:
    location: list[int, int]
    velocity: list[int, int]
    timer: float


class Firework:
    def __init__(self):
        self.particles: list[Particle] = []

    def emit(self, x: int, y: int) -> None:
        particle = Particle(
            [x, y],
            [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
            random.randint(4, 6),
        )
        self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            location = particle.location
            velocity = particle.velocity
            location[0] += velocity[0]
            location[1] += velocity[1]
            particle.timer -= 0.035
            velocity[1] += 0.15
            if particle.timer <= 0:
                self.particles.remove(particle)

    def render(self, screen: pg.Surface) -> None:
        for particle in self.particles:
            location = particle.location
            xc1 = random.randrange(0, 255)
            xc2 = random.randrange(0, 255)
            xc3 = random.randrange(0, 255)
            pg.draw.circle(
                screen,
                (xc1, xc2, xc3),
                [int(location[0]), int(location[1])],
                int(particle.timer),
            )


def main():
    clok = pg.time.Clock()
    pg.display.set_caption("Fireworks")
    screen = pg.display.set_mode((1376, 900), 0, 32)
    pg.mouse.set_visible(False)
    firework = Firework()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        mx, my = pg.mouse.get_pos()

        for i in range(10):
            firework.emit(mx, my)
        firework.update()

        screen.fill((0, 0, 0))
        firework.render(screen)
        pg.display.flip()
        clok.tick(60)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
