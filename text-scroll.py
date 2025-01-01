from dataclasses import dataclass

import pygame as pg


@dataclass(slots=True)
class ScrollText(object):
    """Simple 2d Scrolling Text"""

    text: str
    pos: pg.Vector2
    color: pg.typing.ColorLike
    speed: int = 1
    size: int = 30
    font: pg.Font = None
    surface: pg.Surface = None

    def __post_init__(self):
        screen_width = pg.display.get_surface().width
        self.pos = pg.Vector2(self.pos)
        self.pos.x = screen_width
        # initialize
        self.font = pg.font.SysFont("mono", self.size, bold=True)
        self.surface = self.font.render(self.text, True, self.color)

    def render(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.pos)

    def update(self):
        """update every frame"""
        if self.pos.x + self.surface.get_width() > 1:
            self.pos.x -= self.speed
        else:
            self.pos.x = pg.display.get_surface().width


def test():
    fps = 25
    screen = pg.display.set_mode((600, 600))
    pg.display.set_caption("Text scroll example")
    text = ScrollText("Dolor Ipsum Dolor uswef", (0, 400), pg.Color(255, 255, 0))
    text2 = ScrollText(
        "Simple Scrolling text example", (0, 200), pg.Color(255, 0, 0), 2
    )
    clock = pg.time.Clock()

    run = True
    while run:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False

        for item in (text, text2):
            item.update()

        screen.fill((0, 0, 0, 255))
        for item in (text, text2):
            item.render(screen)
        pg.display.flip()


if __name__ == "__main__":
    try:
        pg.init()
        test()
    finally:
        pg.quit()
