"""
"Parallax Scrolling Example 2" by David Olofson
"""

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Self

import pygame as pg

# ----------------------------------------------------------
# Definitions...
# ----------------------------------------------------------
# foreground and background velocities in pixels/sec */
FOREGROUND_VEL_X = 100.0
FOREGROUND_VEL_Y = 50.0

# Size of the screen in pixels
SCREEN_W = 320
SCREEN_H = 240

# Size of one background tile in pixels
TILE_W = TILE_H = 48

# The maps are 16 by 16 squares, and hold one character per square.
# The characters determine which tiles are to be drawn in the corresponding
# squares on the screen. Space (" ") means that no tile will be drawn.
MAP_W = MAP_H = 16

# *----------------------------------------------------------
#   ...some globals...
# ---------------------------------------------------------*/

foreground_map = (
    # 0123456789ABCDEF
    "3333333333333333",
    "3   2   3      3",
    "3   222 3  222 3",
    "3333 22     22 3",
    "3       222    3",
    "3   222 2 2  333",
    "3   2 2 222    3",
    "3   222      223",
    "3        333   3",
    "3  22 23 323  23",
    "3  22 32 333  23",
    "3            333",
    "3 3  22 33     3",
    "3    222  2  3 3",
    "3  3     3   3 3",
    "3333333333333333",
)

# Middle level map where the planets are.
middle_map = (
    # 0123456789ABCDEF
    "   1    1       ",
    "           1   1",
    "  1             ",
    "     1  1    1  ",
    "   1            ",
    "         1      ",
    " 1            1 ",
    "    1   1       ",
    "          1     ",
    "   1            ",
    "        1    1  ",
    " 1          1   ",
    "     1          ",
    "        1       ",
    "  1        1    ",
    "                ",
)

background_map = (
    # 0123456789ABCDEF
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
)

"""---------------------------------------------------------
    ...and some code. :-)
---------------------------------------------------------"""


@dataclass(slots=True)
class Tiles:
    filename: InitVar[str]
    colorkey: InitVar[pg.typing.ColorLike]
    surface: pg.Surface = None

    def __post_init__(self, filename: str, colorkey: pg.typing.ColorLike):
        image_path = Path("assets") / filename
        if not image_path.exists():
            raise FileNotFoundError(f"File {image_path} not found !")

        surface = pg.image.load(image_path).convert()
        surface.set_colorkey(colorkey)
        self.surface = surface

    def draw(self, screen: pg.Surface, tile: int, pos: pg.typing.Point) -> None:
        # Study the following expression. Typo trap! :-)
        tile = int(tile)
        source_rect = pg.Rect(
            0,  # Only one column, so we never change this.
            tile * TILE_H,  # Select tile from image!
            TILE_W,
            TILE_H,
        )

        dest_rect = pg.Rect(*pos, TILE_W, TILE_H)

        screen.blit(self.surface, dest_rect, source_rect)


@dataclass(slots=True)
class Layer:
    map: tuple[str]
    tiles: Tiles  # pg.Surface
    pos: pg.Vector2 = field(default_factory=pg.Vector2)
    velocity: pg.Vector2 = field(default_factory=pg.Vector2)

    def set_velocity(self, x: float, y: float) -> None:
        self.velocity = pg.Vector2(x, y)

    def animate(self, dt: int) -> None:
        """Update animation (apply the velocity, that is)"""
        self.pos += self.velocity * dt

    def limit_bounce(self):
        """Bounce at map limits"""
        maxx = MAP_W * TILE_W - SCREEN_W
        maxy = MAP_H * TILE_H - SCREEN_H

        if self.pos.x >= maxx:
            self.velocity.x = -self.velocity.x
            # Mirror over right limit. We need to do this
            # to be totally accurate, as we're in a time
            # discreet system! Ain't that obvious...? ;-)
            self.pos.x = maxx * 2 - self.pos.x
        elif self.pos.x <= 0:
            # Basic physics again...
            self.velocity.x = -self.velocity.x
            # Mirror over left limit
            self.pos.x = -self.pos.x

        if self.pos.y >= maxy:
            self.velocity.y = -self.velocity.y
            self.pos.y = maxy * 2 - self.pos.y
        elif self.pos.y <= 0:
            self.velocity.y = -self.velocity.y
            self.pos.y = -self.pos.y

    def link(self, layer: Self, ratio) -> None:
        """
        Link the position of this layer to another layer, w/ scale ratio

        BTW, it would be kind of neat implementing the link in a more
        automatic fashion - link() one layer to another an init time,
        and then forget about it! Oh well, that's another tutorial. :-)
        """
        self.pos = layer.pos * ratio

    def render(self, screen: pg.Surface) -> None:
        """Render layer to the specified surface"""
        # Calculate which part of the map to draw
        map_x = int(self.pos.x / TILE_W)
        map_y = int(self.pos.y / TILE_H)

        """
        Calculate where the screen is, with pixel accuracy.
        (This gets "negated" later, as it's a screen
        coordinate rather than a map coordinate.)
        """
        fine_x = int(self.pos.x % TILE_W)
        fine_y = int(self.pos.y % TILE_H)

        """
        Draw all visible tiles.

        Note that this means that we need to draw the size
        of one tile outside the screen on each side! (The
        parts that are outside aren't actually rendered, of
        course - SDL clips them away.)
        """
        for y in range(-fine_y, SCREEN_H, TILE_H):
            map_x_loop = map_x
            for x in range(-fine_x, SCREEN_W, TILE_W):
                tile = self.map[map_y][map_x_loop]
                if tile != " ":
                    self.tiles.draw(screen, tile, (x, y))
                map_x_loop += 1
            map_y += 1


class Demo:
    title = "Parallax Scrolling"
    width = 320
    height = 240

    def __init__(self):
        screen = pg.display.set_mode(
            (self.width, self.height), pg.DOUBLEBUF | pg.FULLSCREEN | pg.SCALED
        )
        pg.display.set_caption(self.title)
        pg.mouse.set_visible(False)
        self.tiles = Tiles("parallax-tiles.bmp", (255, 0, 255))

        self.foreground_layer = Layer(foreground_map, self.tiles)
        self.middle_layer = Layer(middle_map, self.tiles)
        self.background_layer = Layer(background_map, self.tiles)

        self.foreground_layer.set_velocity(FOREGROUND_VEL_X, FOREGROUND_VEL_Y)

        self.main(screen)

    def main(self, screen: pg.Surface) -> None:
        clock = pg.Clock()
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    run = False
            dt = clock.tick()
            self.update(dt)

            screen.fill("black")
            self.render(screen)
            pg.display.flip()

    def render(self, screen: pg.Surface) -> None:
        # Render layers
        for layer in (self.background_layer, self.middle_layer, self.foreground_layer):
            layer.render(screen)

        # draw "title" tile in upper left corner
        self.tiles.draw(screen, "4", (0, 0))

    def update(self, delta_time: int):
        # calculate time since last update
        dt = delta_time * 0.001

        # Update foreground position
        self.foreground_layer.animate(dt)
        self.foreground_layer.limit_bounce()

        # Link the middle and background levels
        # to the foreground level
        self.middle_layer.link(self.foreground_layer, 0.5)
        self.background_layer.link(self.foreground_layer, 0.25)


if __name__ == "__main__":
    try:
        pg.init()
        Demo()
    finally:
        pg.quit()
