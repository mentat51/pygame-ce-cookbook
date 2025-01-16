"""
This example shows a simple wireframe rotating cube.

Written by Gustavo Niemeyer <niemeyer@conectiva.com>.
"""
from dataclasses import dataclass
from math import sin, cos

import pygame as pg

ORIGINX = 0
ORIGINY = 0

@dataclass(slots=True)
class Point:
    x:float
    y:float
    z:float

    def rotate(self, angle:float, axis:'self')->None:
        """Rotate a 3D point around given axis."""
        point = Point(0, 0, 0)
        cosang = cos(angle)
        sinang = sin(angle)
        point.x += (cosang+(1-cosang) * axis.x * axis.x) * self.x
        point.x += ((1-cosang) * axis.x * axis.y - axis.z * sinang) * self.y
        point.x += ((1-cosang) * axis.x * axis.z + axis.y *sinang) * self.z
        point.y += ((1-cosang) * axis.x * axis.y + axis.z * sinang) * self.x
        point.y += (cosang+(1-cosang) * axis.y * axis.y) * self.y
        point.y += ((1-cosang) * axis.y * axis.z - axis.x * sinang) * self.z
        point.z += ((1-cosang) * axis.x * axis.z - axis.y * sinang) * self.x
        point.z += ((1-cosang) * axis.y * axis.z + axis.x * sinang) * self.y
        point.z += (cosang+(1-cosang) * axis.z * axis.z) * self.z

        self.x = point.x
        self.y = point.y
        self.z = point.z

def draw_3dline(surface:pg.Surface, color:pg.typing.ColorLike, a:Point, b:Point):
    """Convert 3D coordinates to 2D and draw line."""
    ax, ay = a.x+(a.z*0.3)+ORIGINX, a.y+(a.z*0.3)+ORIGINY
    bx, by = b.x+(b.z*0.3)+ORIGINX, b.y+(b.z*0.3)+ORIGINY
    pg.draw.line(surface, color, (ax, ay), (bx, by))


class Cube:
    def __init__(self, size:int)->None:
        self.points = [Point(-size,size,size),  Point(size,size,size),  Point(size,-size,size),  Point(-size,-size,size),
            Point(-size,size,-size), Point(size,size,-size), Point(size,-size,-size), Point(-size,-size,-size)]

    def rotate(self, angle:float, axis:Point)->None:
        """Rotate an object around given axis."""
        for point in self.points:
            point.rotate(angle, axis)

    def draw(self, surface:pg.Surface, color:pg.typing.ColorLike)->None:
        """Draw 3D cube."""
        a, b, c, d, e, f, g, h = self.points
        draw_3dline(surface, color, a, b)
        draw_3dline(surface, color, b, c)
        draw_3dline(surface, color, c, d)
        draw_3dline(surface, color, d, a)

        draw_3dline(surface, color, e, f)
        draw_3dline(surface, color, f, g)
        draw_3dline(surface, color, g, h)
        draw_3dline(surface, color, h, e)

        draw_3dline(surface, color, a, e)
        draw_3dline(surface, color, b, f)
        draw_3dline(surface, color, c, g)
        draw_3dline(surface, color, d, h)

def main():
    BLACK = (0,0,0)
    global ORIGINX, ORIGINY

    screen = pg.display.set_mode((640,400))
    pg.display.set_caption('3D Cube wireframe')

    clock = pg.Clock()
    # Move origin to center of screen
    ORIGINX = screen.get_width()/2
    ORIGINY = screen.get_height()/2
    cube = Cube(100)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

        cube.rotate(0.1,  Point(0, 1, 0))
        cube.rotate(0.01, Point(0, 0, 1))
        cube.rotate(0.01, Point(1, 0, 0))

        screen.fill(BLACK)
        cube.draw(screen, (204,255,0))
        pg.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()