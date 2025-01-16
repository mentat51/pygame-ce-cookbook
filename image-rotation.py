import pygame as pg

def main():
    screen = pg.display.set_mode((700, 700))
    pg.display.set_caption("Re-centering is OFF, press the C key to switch.")
    clock = pg.Clock()

    car = pg.image.load("assets/racing-car.png").convert_alpha()
    car_img = pg.transform.scale_by(car, 0.5)
    car_rect = car_img.get_rect(center=screen.get_rect().center)

    angle = 0
    rotation_speed = 10
    re_centering = False

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    re_centering = not re_centering
                    pg.display.set_caption(
                        f"Re-centering is {'OFF' if not re_centering else 'ON'}, press the C key to switch."
                    )
                elif event.key == pg.K_ESCAPE:
                    run = False

        angle = (angle + 1) % 360
        rotated_car_img = pg.transform.rotate(car_img, -angle)
        if re_centering:
            rotated_car_rect = rotated_car_img.get_rect(center=car_rect.center)
        else:
            rotated_car_rect = rotated_car_img.get_rect(topleft=car_rect.topleft)


        screen.fill("black")
        pg.draw.rect(screen, "red", rotated_car_rect, 3)
        pg.draw.rect(screen, "blue", car_rect, 3)
        screen.blit(rotated_car_img, rotated_car_rect)
        pg.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    try:
        pg.init()
        main()
    finally:
        pg.quit()
