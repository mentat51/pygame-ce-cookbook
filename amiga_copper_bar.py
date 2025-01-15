from dataclasses import dataclass, field

import pygame as pg

@dataclass(slots=True)
class CopperBar:
    height:int
    red:int=0
    green:int=0
    blue:int=0
    direction:int=1
    y:int=0
    lines:list=field(default_factory=list)

    def __post_init__(self):
        height = self.height // 2
        for i in range(1, height):
            self.lines.append((i * self.red, i * self.green, i * self.blue))
        for i in range(1, height):
            red = 255 - i * self.red if self.red else 0
            green = 255 - i * self.green if self.green else 0
            blue = 255 - i * self.blue if self.blue else 0
            self.lines.append((red, green, blue))

    def update(self):
        screen_height = pg.display.get_window_size()[1]
        self.y += self.direction
        if self.y + self.height > screen_height or self.y < 0:
            self.direction *= -1

    def render(self, screen):
        screen_width = screen.get_width()
        y = self.y

        for i, line in enumerate(self.lines):
            pg.draw.line(screen, line, (0, y + i), (screen_width, y + i))


def main():
    screen = pg.display.set_mode((800,600))
    pg.display.set_caption('Copper Bar')
    clock = pg.Clock()

    blue_bar = CopperBar(124, blue=4)
    red_bar = CopperBar(124, red=4, y=80)
    green_bar = CopperBar(124, green=4, y=280)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        blue_bar.update()
        red_bar.update()
        green_bar.update()

        screen.fill((0, 0, 0))
        blue_bar.render(screen)
        red_bar.render(screen)
        green_bar.render(screen)

        pg.display.flip()

        clock.tick()

if __name__ == '__main__':
    try:
        pg.init()
        main()
    finally:
        pg.quit()