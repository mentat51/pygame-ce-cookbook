from dataclasses import dataclass, field
import os
import random

import pygame as pg


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 650

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (150, 50)


@dataclass(slots=True)
class Spark:
    x: int
    y: int
    radius: int = 5
    original_radius: int = 5
    alpha_layers: int = 2
    alpha_glow: int = 2
    burn_rate: float = 0.0

    def __post_init__(self):
        self.original_radius = self.radius
        self.burn_rate = 0.1 * random.randint(1, 4)

    def update(self):
        self.y -= 7 - self.radius
        self.x += random.randint(-self.radius, self.radius)
        self.original_radius -= self.burn_rate
        self.radius = int(self.original_radius)
        if self.radius <= 0:
            self.radius = 1

    def draw(self, screen: pg.Surface) -> None:
        max_surf_size = (
            2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
        )
        surf = pg.Surface((max_surf_size, max_surf_size), pg.SRCALPHA)
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.radius * i * i * self.alpha_glow
            if self.radius in (3, 4):
                r, g, b = (255, 0, 0)
            elif self.radius == 2:
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (50, 50, 50)
            # r, g, b = (0, 0, 255)  # uncomment this to make the flame blue
            color = (r, g, b, alpha)
            pg.draw.circle(
                surf,
                color,
                (surf.get_width() // 2, surf.get_height() // 2),
                radius,
            )
        screen.blit(surf, surf.get_rect(center=(self.x, self.y)))


@dataclass(slots=True)
class Flame:
    x: int
    y: int
    flame_intensity: int = 2
    particles: list[Spark] = field(default_factory=list)

    def __post_init__(self):
        for i in range(self.flame_intensity * 25):
            self.particles.append(
                Spark(self.x + random.randint(-5, 5), self.y, random.randint(1, 5))
            )

    def draw(self, screen: pg.Surface) -> None:
        for spark in self.particles:
            spark.draw(screen)

    def update(self):
        for spark in self.particles:
            if spark.original_radius <= 0:
                self.particles.remove(spark)
                self.particles.append(
                    Spark(self.x + random.randint(-5, 5), self.y, random.randint(1, 5))
                )
                del spark
                continue
            spark.update()


def main_window():
    clock = pg.time.Clock()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Flame Particles using pygame")

    FPS = 60

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    flames = [
        Flame(center_x, center_y),
        Flame(center_x - 50, center_y),
        Flame(center_x + 50, center_y),
    ]

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        for flame in flames:
            flame.update()

        screen.fill((0, 0, 0))
        for flame in flames:
            flame.draw(screen)
        pg.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    try:
        pg.init()
        main_window()
    finally:
        pg.quit()
