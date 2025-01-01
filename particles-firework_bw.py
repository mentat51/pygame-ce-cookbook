"""
https://pythonprogramming.altervista.org/a-screensaver-with-fireworks-in-pygame/
"""

from dataclasses import dataclass
import random

import pygame as pg


def mouse_simulator():
    width = pg.display.get_window_size()[0]
    if random.random() < 0.05:
        clicking = True
    else:
        clicking = False
    mx = random.randrange(0, width)
    my = random.randrange(0, width)
    return clicking, mx, my


@dataclass(slots=True)
class Particle:
    location: list[int, int]
    velocity: list[int, int]
    timer: float


class FireWork:
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
            pg.draw.circle(
                screen,
                (255, 255, 255),
                [int(location[0]), int(location[1])],
                int(particle.timer),
            )


def main():
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1376, 900), 0, 32)
    pg.display.set_caption("Firework demo")

    firework = FireWork()
    clicking = False
    pg.mouse.set_visible(False)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_f:
                    pg.display.toggle_fullscreen()

        clicking, mx, my = mouse_simulator()
        if clicking:
            for i in range(10):
                firework.emit(mx, my)

        firework.update()

        screen.fill((0, 0, 0))
        firework.render(screen)
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
