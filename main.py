import os
import random
import sys

import pygame
from pygame import mixer

#from time import sleep


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


def start_screen():
    intro_text = [
        "ЗАСТАВКА", "", "Правила игры", "Если в правилах несколько строк,",
        "приходится выводить их построчно"
    ]
    mixer.init()
    mixer.music.load('data\\start.mp3')
    mixer.music.play()
    pygame.font.init()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('Arial.ttf', 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


def texts(score, drops_collected, ps):
    pygame.font.init()
    font = pygame.font.Font("BoldPixelSans.ttf", 30)
    if drops_collected:
        scoretext = font.render(
            f"Score: {str(score)} | Accuracy: {str(round(ps / (drops_collected) * 100))}%",
            1, (200, 0, 0))
        screen.blit(scoretext, (10, 10))
    else:
        scoretext = font.render(
            f"Score: {str(score)} | Accuracy: {str(drops_collected)}%", 1,
            (200, 0, 0))
        screen.blit(scoretext, (10, 10))


size = (WIDTH, HEIGHT) = 1000, 700

global score
global posScore
global drops_collected

score = 0
posScore = 0
drops_collected = 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Бабиджонка!')

start_screen()

placeSP_group = pygame.sprite.OrderedUpdates()
bowlGR = pygame.sprite.Group()
drops = pygame.sprite.Group()
protection = pygame.sprite.Group()

mixer.init()
pygame.mixer.music.load('data\\fight.mp3')
pygame.mixer.music.play(-1)

bowl_image = pygame.transform.scale(load_image("bowl.png", -1), (200, 100))
bowl = pygame.sprite.Sprite(bowlGR)
bowl.image = bowl_image
bowl.rect = bowl.image.get_rect()
bowl.rect.top = 600
bowl.rect.left = 400


class bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet.image
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left + 100

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)
        #if pygame.sprite.spritecollideany(self, bowlGR):
        #    placeSP_group.add([self])
        #    placeSP_group.sprites()[0].kill()
        #    score += 2
        #    posScore += 1
        #    drops_collected += 1
        #    mixer.Channel(1).play(mixer.Sound('data\\coin.mp3'))
        #    print(score)
        #    print('REMOVED: bullet')


class twoPointDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("twoPointDrop.png", -1),
                                   (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = twoPointDrop.image
        self.rect = self.image.get_rect()
        self.rect.top = 50
        self.rect.left = random.randint(50, 900)

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score += 2
            posScore += 1
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\coin.mp3'))
            print(score)
            print('REMOVED: twoPointDrop')

        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\kill.mp3'))


class fourPointDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("fourPointDrop.png", -1),
                                   (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = fourPointDrop.image
        self.rect = self.image.get_rect()
        self.rect.top = 50
        self.rect.left = random.randint(50, 900)

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score += 4
            posScore += 1
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\coin.mp3'))
            print(score)
            print('REMOVED: fourPointDrop')

        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\kill.mp3'))


class minusDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("minusDrop.png", -1), (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = minusDrop.image
        self.rect = self.image.get_rect()
        self.rect.top = 50
        self.rect.left = random.randint(50, 900)

    def update(self):
        global score
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score -= 20
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\expl2.mp3'))
            print(score)
            print('REMOVED: minusDrop')

        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\kill.mp3'))


class slice(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("slice.png", -1), (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = slice.image
        self.rect = self.image.get_rect()
        self.rect.top = 50
        self.rect.left = random.randint(50, 900)

    def update(self):
        global score
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score //= 2
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\expl1.mp3'))
            print(score)
            print('REMOVED: slice')

        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\kill.mp3'))


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
        print('SPAWNED: slice')
    drops.update()
    protection.update()
    #simpleDrop
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet(protection)
                mixer.Channel(0).play(mixer.Sound('data\\rotate.mp3'))
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
    #all_sprites.draw(screen)
    bowlGR.draw(screen)
    protection.draw(screen)
    drops.draw(screen)
    texts(score, drops_collected, posScore)
    pygame.display.flip()

pygame.quit()