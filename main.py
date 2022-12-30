import os
#from time import sleep

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def main():
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Герой двигается!')

    # группа, содержащая все спрайты
    all_sprites = pygame.sprite.Group()

    # изображение должно лежать в папке data
    bowl_image = pygame.transform.scale(load_image("bowl.png"), (200, 100))
    bowl = pygame.sprite.Sprite(all_sprites)
    bowl.image = bowl_image
    bowl.rect = bowl.image.get_rect()
    bowl.rect.top = 600
    bowl.rect.left = 400

    # шаг перемещения
    dist = 10

    running = True
    move = 1
    while running:
        pygame.time.delay(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    move *= -1
                    print('MOVE CHANGED')
        key = pygame.key.get_pressed()
        if move == 1:
            bowl.rect.left += 1
            if bowl.rect.left >= 1000:
                bowl.rect.left = -200
        if move == -1:
            bowl.rect.left -= 1
            if bowl.rect.left <= -200:
                bowl.rect.left = 1000
        print(bowl.rect.left)
            #key = pygame.key.get_pressed()
            #if key[pygame.K_RIGHT]:
            #    bowl.rect.left += dist
            #    print(bowl.rect.left)
            #elif key[pygame.K_LEFT]:
            #    bowl.rect.left -= dist
            #    print(bowl.rect.left)
        screen.fill(pygame.Color("royalblue"))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
