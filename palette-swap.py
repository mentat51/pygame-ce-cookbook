"""
https://pythonprogramming.altervista.org/swap-color-palette-in-pygame-dafluffypotato/?doing_wp_cron=1614111833.7463190555572509765625

Change the colors of an original image to get a new picture derived from the original.
"""

import pygame as pg

from pygame.typing import ColorLike


def palette_swap(surf: pg.Surface, old_color: ColorLike, new_color: ColorLike):
    img_copy = pg.Surface(surf.get_size())
    img_copy.fill(new_color)
    surf.set_colorkey(old_color)
    img_copy.blit(surf, (0, 0))
    return img_copy


def main():
    pg.display.set_caption("game base")
    screen = pg.display.set_mode((1000, 500), 0, 32)
    clock = pg.time.Clock()

    tree_original = pg.image.load("assets/tree.png").convert()
    tree_img = palette_swap(tree_original, (11, 70, 97), (17, 11, 96))
    tree_img = palette_swap(tree_img, (15, 106, 99), (83, 32, 145))
    tree_img = palette_swap(tree_img, (35, 152, 77), (167, 65, 131))
    tree_img = palette_swap(tree_img, (154, 209, 59), (205, 124, 97))
    tree_img.set_colorkey((0, 0, 0))

    # scale x3 the two images
    tree_original = pg.transform.scale_by(tree_original, (3, 3))
    tree = pg.transform.scale_by(tree_img, (3, 3))

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        screen.fill((0, 0, 0))
        screen.blit(tree_original, (50, 50))
        screen.blit(tree, (500, 50))
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    try:
        main()
    finally:
        pg.quit()
