from dataclasses import dataclass
import math

import pygame as pg


@dataclass(slots=True)
class SinusText(object):
    """Sinus wave scroll text"""

    text: str
    y: int
    amplitude: int  # amplitude of sinus wave
    frequency: int  # frequency of sinus wave
    font_color: pg.Color
    font_size: int = 30
    _text_surface: pg.Surface = None
    _factor: float = 1.0
    _position: int = 0  # position in rendered string

    def __post_init__(self):
        # prepend an append some spaces
        width = pg.display.get_window_size()[0]
        appendix = " " * (width // self.font_size)
        self.text = appendix + self.text + appendix
        # radian to degree
        self._factor = 2 * math.pi / width

        font = pg.font.SysFont("mono", self.font_size, bold=True)
        self._text_surface = font.render(self.text, True, self.font_color)

    def render(self, screen: pg.Surface):
        for offset in range(self._text_surface.get_width()):
            screen.blit(
                self._text_surface,
                (
                    0 + offset,
                    self.y
                    + math.sin(offset * self.frequency * self._factor) * self.amplitude,
                ),
                (self._position + offset, 0, 1, self.font_size),
            )

    def update(self):
        if self._position < self._text_surface.get_width():
            self._position += 1
        else:
            self._position = 0


def main():
    fps = 50
    screen = pg.display.set_mode((600, 600))
    pg.display.set_caption("text sinus scrolling")
    text = SinusText("Dolor Ipsum Dolor uswef", 200, 30, 2, pg.Color(0, 255, 255))
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                run = False
        keyinput = pg.key.get_pressed()
        if keyinput is not None:
            if keyinput[pg.K_ESCAPE]:
                run = False

        text.update()

        screen.fill((0, 0, 0, 255))
        text.render(screen)
        pg.display.flip()


if __name__ == "__main__":
    try:
        pg.init()
        main()
    finally:
        pg.quit()
