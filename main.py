import os
import random
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

    def texts(score):
        pygame.font.init()
        font = pygame.font.Font("Arial.ttf", 30)
        scoretext = font.render(f"Score: {str(score)}", 1, (200, 0, 0))
        screen.blit(scoretext, (10, 10))

    size = 1000, 700
    global score
    score = 0
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Бабиджонка!')

    # группа, содержащая все спрайты
    placeSP_group = pygame.sprite.OrderedUpdates()
    all_sprites = pygame.sprite.Group()
    drops = pygame.sprite.Group()

    # изображение должно лежать в папке data
    bowl_image = pygame.transform.scale(load_image("bowl.png", -1), (200, 100))
    bowl = pygame.sprite.Sprite(all_sprites)
    bowl.image = bowl_image
    bowl.rect = bowl.image.get_rect()
    bowl.rect.top = 600
    bowl.rect.left = 400

    class twoPointDrop(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image("twoPointDrop.png", -1),
                                       (75, 75))

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            self.image = twoPointDrop.image
            self.rect = self.image.get_rect()
            self.rect.top = 50
            self.rect.left = random.randint(50, 900)

        def update(self):
            global score
            self.rect = self.rect.move(random.randrange(3) - 1, 3)
            if pygame.sprite.spritecollideany(self, all_sprites):
                placeSP_group.add([self])
                placeSP_group.sprites()[0].kill()
                score += 2
                print(score)
                print('REMOVED: twoPointDrop')

    class fourPointDrop(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image("fourPointDrop.png", -1),
                                       (75, 75))

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            self.image = fourPointDrop.image
            self.rect = self.image.get_rect()
            self.rect.top = 50
            self.rect.left = random.randint(50, 900)

        def update(self):
            global score
            self.rect = self.rect.move(random.randrange(3) - 1, 3)
            if pygame.sprite.spritecollideany(self, all_sprites):
                placeSP_group.add([self])
                placeSP_group.sprites()[0].kill()
                score += 4
                print(score)
                print('REMOVED: fourPointDrop')

    class minusDrop(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image("minusDrop.png", -1),
                                       (75, 75))

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            self.image = minusDrop.image
            self.rect = self.image.get_rect()
            self.rect.top = 50
            self.rect.left = random.randint(50, 900)

        def update(self):
            global score
            self.rect = self.rect.move(random.randrange(3) - 1, 3)
            if pygame.sprite.spritecollideany(self, all_sprites):
                placeSP_group.add([self])
                placeSP_group.sprites()[0].kill()
                score -= 20
                print(score)
                print('REMOVED: minusDrop')

    class slice(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image("slice.png", -1), (75, 75))

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            self.image = slice.image
            self.rect = self.image.get_rect()
            self.rect.top = 50
            self.rect.left = random.randint(50, 900)

        def update(self):
            global score
            self.rect = self.rect.move(random.randrange(3) - 1, 3)
            if pygame.sprite.spritecollideany(self, all_sprites):
                placeSP_group.add([self])
                placeSP_group.sprites()[0].kill()
                score //= 2
                print(score)
                print('REMOVED: slice')

    running = True
    move = 1
    while running:
        nrand = random.randint(0, 1025000)
        if nrand < 10000:
            twoPointDrop(drops)
            print('SPAWNED: twoPointDrop')
        elif 10000 <= nrand < 15000:
            fourPointDrop(drops)
            print('SPAWNED: fourPointDrop')
        elif 15000 <= nrand < 20000:
            minusDrop(drops)
            print('SPAWNED: minusDrop')
        elif 20000 <= nrand < 30000:
            slice(drops)
            print('SPAWNED: minusDrop')
        drops.update()
        #simpleDrop
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    move *= -1
                    #print('MOVE CHANGED')
        if move == 1:
            bowl.rect.left += 5
            if bowl.rect.left >= 1000:
                bowl.rect.left = -200
        if move == -1:
            bowl.rect.left -= 5
            if bowl.rect.left <= -200:
                bowl.rect.left = 1000
        #print(bowl.rect.left)
        screen.fill(pygame.Color("royalblue"))
        all_sprites.draw(screen)
        drops.draw(screen)
        texts(score)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
