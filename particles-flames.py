# program by: tank king
# demonstration of flame particles
from dataclasses import dataclass, field
import math
from random import randint
from typing import ClassVar

# requires pg 2.0.0 for pg.SCALED flag
# to use pg 1.9.x remove the SCALED flag when initializing the display

import pygame as pg


# resolution is high for demonstration purposes
# FPS can be highly improved at lower resolutions
screen_width = 1280
screen_height = 720


@dataclass(slots=True)
class FlameParticle:
    x: int = 50
    y: int = 50
    radius: int = 5
    original_radius: int = 5
    surf: pg.Surface = None
    burn_rate: float = 0.0

    alpha_layers: ClassVar[int] = 2
    alpha_glow: ClassVar[float] = 0.75

    def __post_init__(self):
        # self.x = x
        # self.y = y
        # self.r = r
        self.original_radius = self.radius
        max_surf_size = (
            2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
        )
        self.surf = pg.Surface((max_surf_size, max_surf_size), pg.SRCALPHA)
        self.burn_rate = 0.05 * randint(1, 8)

    def update(self, dt):
        self.y -= (7 - self.radius) * dt / 4
        self.x += randint(-self.radius, self.radius) * dt * 0.33
        self.original_radius -= self.burn_rate * dt
        self.radius = int(self.original_radius)
        if self.radius <= 0:
            self.radius = 1

    def draw(self, screen: pg.Surface) -> None:
        max_surf_size = (
            2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
        )
        self.surf = pg.Surface((max_surf_size, max_surf_size), pg.SRCALPHA)
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.radius * i * i * self.alpha_glow
            if self.radius in (3, 4):
                r, g, b = (255, 0, 0)
            elif self.radius in (1, 2):
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (75, 75, 75)
            # r, g, b = (0, 0, 255)  # uncomment this to make the flame blue
            color = (r, g, b, alpha)
            pg.draw.circle(
                self.surf,
                color,
                (self.surf.get_width() * 0.5, self.surf.get_height() * 0.5),
                radius,
            )
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))


@dataclass(slots=True)
class Flame:
    x: int = 50
    y: int = 50
    intensity: int = 1
    particles: list[FlameParticle] = field(default_factory=list)

    def __post_init__(self):
        self.emit_particles()

    def emit_particles(self) -> None:
        self.particles.clear()
        for _ in range(int(self.intensity) * 1):
            self.particles.append(
                FlameParticle(self.x + randint(-1, -1), self.y, randint(1, 5))
            )

    def draw(self, dt, screen: pg.Surface) -> None:
        for particle in self.particles:
            if particle.original_radius <= 0:
                self.particles.remove(particle)
                self.particles.append(
                    FlameParticle(self.x + randint(-1, -1), self.y, randint(1, 5))
                )
                del particle
                continue
            particle.update(dt)
            particle.draw(screen)


def check_color(color, condition: str):
    r, g, b = condition.split(",")
    r1, g1, b1 = color

    def compare(x, y, compare_type):
        x, y = int(x), int(y)
        if compare_type == ">":
            return x > y
        elif compare_type == "<":
            return x < y
        elif compare_type == "==":
            return x == y

    red_compare_results = compare(r1, r[1:], r[0])
    green_compare_results = compare(g1, g[1:], g[0])
    blue_compare_results = compare(b1, b[1:], b[0])

    if red_compare_results and green_compare_results and blue_compare_results:
        return True
    else:
        return False


def extract_points_from_img(
    image: pg.Surface, image_color_range: dict, allowed_colors=("black", "red")
):
    extracted_points = []
    image.lock()
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            pixel_color = image.get_at([x, y])
            r, g, b, alpha = pixel_color
            if alpha > 127:
                for color in list(image_color_range.keys()):
                    if color in allowed_colors:
                        if check_color((r, g, b), image_color_range[color]):
                            extracted_points.append([x, y])
    image.unlock()
    return extracted_points


def remove_point_cluttering(point_list):
    # basic function to reduce the number of points
    # only keeps points for every 4th point iterated
    point_list.sort(key=lambda a: a[1])
    point_list = [i for i in point_list if point_list.index(i) % 4 == 0]
    return point_list


def main():
    screen = pg.display.set_mode(
        (screen_width, screen_height), pg.SCALED | pg.FULLSCREEN
    )
    pg.display.set_caption("Flame Sparks Testing")

    clock = pg.time.Clock()
    FPS = 60

    TARGET_FPS = 60

    flames = []

    color_ranges = {
        "white": ">225,>225>225",
        "red": ">100,<50,<50",
        "yellow": ">200,>200,<50",
        "black": "<50,<50,<50",
    }

    img = pg.image.load("assets/durga1.png").convert()
    img = pg.transform.scale(img, (int(img.get_width() * 720 / img.get_height()), 720))
    print("Loading Points...")
    points = extract_points_from_img(img, color_ranges)
    print("Points Loaded")

    print("Removing Point Cluttering")
    points = remove_point_cluttering(point_list=points)
    print("Point Cluttering Reduced")

    # shifting all points to center of screen
    print("Shifting all points to center")
    for p in points:
        p[0] += screen_width // 2 - img.get_width() // 2
    print("All points shifted to center")

    # circular points
    points2 = [
        [
            screen_width // 2 + 25 + screen_height // 2 * math.cos(math.radians(i)),
            screen_height // 2 + screen_height // 2 * math.sin(math.radians(i)),
        ]
        for i in range(360)
    ]

    dt = 1
    surf = pg.Surface(screen.get_size())  # to make the background fade away
    surf.set_alpha(0)
    alpha = 0
    start = True  # set it to False if you want to manually trigger the animation after loading
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                # manually trigger the animation by pressing any key
                start = True
                if event.key == pg.K_ESCAPE:
                    run = False

        if start:
            if len(flames) < len(points):
                qty = 5 if len(points) - len(flames) > 5 else len(points) - len(flames)
                for _ in range(qty):
                    flames.append(Flame(*points[len(flames)]))
            else:
                alpha += 0.5
                if alpha > 255:
                    alpha = 255
                surf.set_alpha(int(alpha))
        if alpha >= 255:
            if len(flames) < len(points) + len(points2):
                temp = Flame(*points2[len(flames) - len(points)], 10)
                flames.append(temp)

        screen.fill((0, 0, 0))
        screen.blit(img, (screen_width // 2 - img.get_width() // 2, 0))
        # the fading effect can also be done by changing the alpha of the image directly (can be used to improve FPS)
        screen.blit(surf, (0, 0))
        for flame in flames:
            flame.draw(dt, screen)
        pg.display.flip()
        pg.display.set_caption(
            "Flame Particles Testing FPS = " + str(int(clock.get_fps()))
        )
        dt = TARGET_FPS * clock.tick(FPS) * 0.001


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
