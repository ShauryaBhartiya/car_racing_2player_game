import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def control_of_player1(player_car1):
    moved = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moved = True
        player_car1.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car1.move_backword()
    if keys[pygame.K_a]:
        player_car1.rotate(left=True)
    if keys[pygame.K_d]:
        player_car1.rotate(right = True)

    if not moved:
        player_car1.reduce_speed()

def control_of_player2(player_car2):
    moved = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        moved = True
        player_car2.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car2.move_backword()
    if keys[pygame.K_LEFT]:
        player_car2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car2.rotate(right = True)

    if not moved:
        player_car2.reduce_speed()

def blit_text_center(win, font, text):
    render = font.render(text, 50, (255, 0, 0))
    win.blit(render,(win.get_width()/2- render.get_width()/2, win.get_height()/2- render.get_height()/2))