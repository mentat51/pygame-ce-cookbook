from itertools import repeat
from random import randint

import pygame as pg


def shake():
    """
    this function creates our shake-generator
    it "moves" the screen to the left and right
    three times by yielding (-5, 0), (-10, 0),
    ... (-20, 0), (-15, 0) ... (20, 0) three times,
    then keeps yieling (0, 0)
    """
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x * s, 0)
        for x in range(20, 0, 5):
            yield (x * s, 0)
        s *= -1
    while True:
        yield (0, 0)


def get_rock():
    return pg.Rect(randint(0, 340), 0, 60, 60)


def main():
    org_screen = pg.display.set_mode((400, 400))
    screen = org_screen.copy()
    screen_rect = screen.get_rect()
    player = pg.Rect(180, 180, 20, 20)

    falling = get_rock()
    clock = pg.time.Clock()

    # 'offset' will be our generator that produces the offset
    # in the beginning, we start with a generator that
    # yields (0, 0) forever
    offset = repeat((0, 0))

    while True:
        if pg.event.get(pg.QUIT):
            break
        pg.event.pump()

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player.move_ip(0, -2)
        if keys[pg.K_a]:
            player.move_ip(-2, 0)
        if keys[pg.K_s]:
            player.move_ip(0, 2)
        if keys[pg.K_d]:
            player.move_ip(2, 0)
        player.clamp_ip(screen_rect)

        falling.move_ip(0, 4)

        if player.colliderect(falling):
            # if the player is hit by the rock,
            # we create a new shake-generator
            offset = shake()
            falling = get_rock()

        if not screen_rect.contains(falling):
            falling = get_rock()

        org_screen.fill((0, 0, 0))
        screen.fill((255, 255, 255))
        pg.draw.rect(screen, (0, 0, 0), player)
        pg.draw.rect(screen, (255, 0, 0), falling)

        # here we draw our temporary surface to the
        # screen using the offsets created by the
        # generators.
        org_screen.blit(screen, next(offset))
        pg.display.flip()

        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
