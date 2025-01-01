import math
import random

import pygame as pg


RES = WIDTH, HEIGHT = 1600, 900
ALPHA = 30


class Star:
    CENTER = pg.Vector2(WIDTH // 2, HEIGHT // 2)
    COLORS = "blue cyan skyblue purple magenta".split()
    Z_DISTANCE = 140

    __slots__ = ("position", "velocity", "color", "screen_pos", "size")

    def __init__(self):
        self.position: pg.Vector3 = self.get_position()
        self.velocity: float = random.uniform(0.45, 0.95)
        self.color: pg.typing.ColorLike = random.choice(self.COLORS)
        self.screen_pos: pg.Vector2 = pg.Vector2(0, 0)
        self.size: int = 10

    def get_position(self, scale_pos=35) -> pg.Vector3:
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return pg.Vector3(x, y, self.Z_DISTANCE)

    def update(self):
        self.position.z -= self.velocity
        self.position = self.get_position() if self.position.z < 1 else self.position

        self.screen_pos = (
            pg.Vector2(self.position.x, self.position.y) / self.position.z + self.CENTER
        )
        self.size = (self.Z_DISTANCE - self.position.z) / (0.2 * self.position.z)
        # rotate xy
        self.position.xy = self.position.xy.rotate(0.2)
        # mouse
        # mouse_pos = self.CENTER - vec2(pg.mouse.get_pos())
        # self.screen_pos += mouse_pos

    def draw(self, screen: pg.Surface) -> None:
        size = self.size
        position = self.screen_pos
        if (-size < position.x < WIDTH + size) and (-size < position.y < HEIGHT + size):
            pg.draw.rect(screen, self.color, (*position, size, size))


class Starfield:
    NUM_STARS = 1500

    def __init__(self):
        self.stars = [Star() for i in range(self.NUM_STARS)]

    def render(self, screen: pg.Surface) -> None:
        for star in self.stars:
            star.draw(screen)

    def update(self) -> None:
        for star in self.stars:
            star.update()
        self.stars.sort(key=lambda star: star.position.z, reverse=True)


def main():
    clock = pg.time.Clock()
    screen = pg.display.set_mode(RES)
    pg.display.set_caption("Starfield Voxel Tunnel")
    alpha_surface = pg.Surface(RES)
    alpha_surface.set_alpha(ALPHA)
    starfield = Starfield()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_f:
                    pg.display.toggle_fullscreen()

        starfield.update()

        # self.screen.fill('black')
        starfield.render(screen)
        screen.blit(alpha_surface)

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
