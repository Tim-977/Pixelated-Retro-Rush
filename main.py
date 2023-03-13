import os
import random
import sys

import pygame
from pygame import mixer

import dbparser as dbp

# Import required modules


# Helps with loading image
def load_image(name, color_key=None):
    fullname = os.path.join('data\\pics', name)
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


# Function that starts the 1st (start) window
def start_screen():
    global name  # Player's name
    mixer.init()  # Initialize music
    mixer.music.load('data\\music\\start.mp3')
    mixer.music.play()
    pygame.font.init()
    # images loading for the window:
    fon = pygame.transform.scale(load_image('startbg.png'), (WIDTH, HEIGHT))
    gamename = pygame.transform.scale(load_image('gamename.png', -1),
                                      (953, 139))
    screen.blit(fon, (0, 0))
    screen.blit(gamename, (17, 13))
    # Font initialization
    font = pygame.font.Font('data\\fonts\\Arial.ttf', 30)
    submit_image = pygame.image.load("data\\pics\\play.png")
    name = ""
    while True:  # Main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                terminate()  # Terminates the window
            elif event.type == pygame.KEYDOWN:
                # Name input
                if event.unicode.isalpha() and len(name) < 27:
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Check if the submit button was pressed
                if name and submit_rect.collidepoint(mouse_pos):
                    return
        pygame.draw.rect(screen, 'forest green',
                         (100, 223, 405, 65))  # Draw rectangle
        text = font.render(name, True, (0, 0, 0))  # Render text
        screen.blit(text, (120, 238))  # Blit text
        submit_rect = submit_image.get_rect(
            topleft=(100, 373))  # Get submit_image rect
        screen.blit(submit_image, submit_rect)  # Blit submit_image
        pygame.display.flip()  # Update display


def terminate():
    pygame.quit()
    sys.exit()  # Terminates the window


def texts(score, drops_collected, ps, phase):  # Shows the score
    pygame.font.init()
    font = pygame.font.Font("data\\fonts\\BoldPixelSans.ttf", 30)
    if phase == 'middleGame':  # Checks is the game in process or over
        if drops_collected:
            scoretext = font.render(  # Renders text
                f"Score: {str(score)} | Accuracy: {str(round(ps / (drops_collected) * 100))}%",
                1, (200, 0, 0))
            screen.blit(scoretext, (10, 10))  # Blits it
        else:
            scoretext = font.render(  # Renders text
                f"Score: {str(score)} | Accuracy: {str(drops_collected)}%", 1,
                (200, 0, 0))
            screen.blit(scoretext, (10, 10))  # Blits it
    elif phase == 'gameOver':
        if drops_collected:
            scoretext = font.render(  # Renders text
                f"Score: {str(score)} | Accuracy: {str(round(ps / (drops_collected) * 100))}%",
                1, (200, 0, 0))
            screen.blit(scoretext, (20, 150))  # Blits it
        else:
            scoretext = font.render(  # Renders text
                f"Score: {str(score)} | Accuracy: {str(drops_collected)}%", 1,
                (200, 0, 0))
            screen.blit(scoretext, (20, 150))  # Blits it


size = (WIDTH, HEIGHT) = 1000, 700

score = 0
posScore = 0  # Positive score (only buff effect drops)
drops_collected = 0
healthPoints = 3

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pixelated Retro Rush')

start_screen()  # Runs the 1st window

placeSP_group = pygame.sprite.OrderedUpdates()
bowlGR = pygame.sprite.Group()
drops = pygame.sprite.Group()
protection = pygame.sprite.Group()

mixer.init()  # Loads music
pygame.mixer.music.load('data\\music\\fight.mp3')
pygame.mixer.music.play(-1)

bowl = pygame.sprite.Sprite(bowlGR)
frames = [  # Loads frames for the bowl animation
    pygame.transform.scale(load_image("bowl_frame1.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame2.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame3.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame4.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame5.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame6.png", -1), (200, 100)),
    pygame.transform.scale(load_image("bowl_frame7.png", -1), (200, 100))
]
bowl.image = frames[0]
# Sets bowl posititon
bowl.rect = bowl.image.get_rect()
bowl.rect.top = 600
bowl.rect.left = 400
bowl.current_frame = 0
bowl.fps = 15
bowl.anim_time = pygame.time.get_ticks()

backGround_image = pygame.transform.scale(load_image("backGround.png"),
                                          (1000, 700))  # Loads an image
end_image = pygame.transform.scale(load_image("endbg.png"), (600, 700))
health_image_1 = pygame.transform.scale(load_image("heart_label.png", -1),
                                        (100, 100))  # Loads an image
health_image_2 = pygame.transform.scale(load_image("heart_label.png", -1),
                                        (100, 100))  # Loads an image
health_image_3 = pygame.transform.scale(load_image("heart_label.png", -1),
                                        (100, 100))  # Loads an image
died_image_1 = pygame.transform.scale(load_image("dead_label.png", -1),
                                      (100, 100))  # Loads an image
died_image_2 = pygame.transform.scale(load_image("dead_label.png", -1),
                                      (100, 100))  # Loads an image
died_image_3 = pygame.transform.scale(load_image("dead_label.png", -1),
                                      (100, 100))  # Loads an image
bullet_image_cross = pygame.transform.scale(  # Loads an image
    load_image("bullet_label_cross.png", -1), (100, 100))
bullet_image_tick = pygame.transform.scale(  # Loads an image
    load_image("bullet_image_tick.png", -1), (100, 100))
screen.blit(health_image_1, (900, 100))  # Blits an image
screen.blit(health_image_2, (900, 100))  # Blits an image
screen.blit(health_image_3, (900, 100))  # Blits an image
screen.blit(bullet_image_cross, (900, 100))  # Blits an image
pygame.display.flip()
running = True
direction = 1


# Classes for bullets:
class bullet_1(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet_1.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left + 100

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)  # Movement
        if self.rect.top < 0:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class bullet_2(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet_2.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left - 100

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)  # Movement
        if self.rect.top < 0:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class bullet_3(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet_3.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left + 300

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)  # Movement
        if self.rect.top < 0:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class bullet_4(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet_4.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left - 5

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)  # Movement
        if self.rect.top < 0:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class bullet_5(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bullet.png", -1), (30, 95))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = bullet_5.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.bottom = bowl.rect.top
        self.rect.left = bowl.rect.left + 200

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(0, -12)  # Movement
        if self.rect.top < 0:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class heartDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("heart.png", -1), (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = heartDrop.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.top = 115
        self.rect.left = random.randint(50, 875)

    def update(self):
        global score
        global posScore
        global drops_collected
        global healthPoints
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        if pygame.sprite.spritecollideany(
                self, bowlGR):  # If bowl takes a falling heart
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            if healthPoints < 3:
                healthPoints += 1
            mixer.Channel(1).play(mixer.Sound('data\\music\\health.mp3'))

        if pygame.sprite.spritecollideany(
                self, protection):  # If bowl touches a fire
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\music\\kill.mp3'))
        if self.rect.top > 1000:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class twoPointDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("twoPointDrop.png", -1),
                                   (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = twoPointDrop.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.top = 115
        self.rect.left = random.randint(50, 875)

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        # If bowl collects
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score += 2
            posScore += 1
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\music\\coin.mp3'))
        # If bullet kills
        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\music\\kill.mp3'))
        if self.rect.top > 1000:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class fourPointDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("fourPointDrop.png", -1),
                                   (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = fourPointDrop.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.top = 115
        self.rect.left = random.randint(50, 875)

    def update(self):
        global score
        global posScore
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        # If bowl collects
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score += 4
            posScore += 1
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\music\\coin.mp3'))
        # If bullet kills
        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\music\\kill.mp3'))
        if self.rect.top > 1000:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class minusDrop(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("minusDrop.png", -1), (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = minusDrop.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.top = 115
        self.rect.left = random.randint(50, 875)

    def update(self):
        global score
        global drops_collected
        global running
        global healthPoints
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        # If bowl collects
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            healthPoints -= 1
            if not healthPoints:
                mixer.Channel(1).play(mixer.Sound('data\\music\\gameOver.mp3'))
                running = False
            else:
                mixer.Channel(1).play(mixer.Sound('data\\music\\expl2.mp3'))
        # If bullet kills
        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\music\\kill.mp3'))
        if self.rect.top > 1000:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


class slice(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("slice.png", -1), (75, 75))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = slice.image
        # Sets position
        self.rect = self.image.get_rect()
        self.rect.top = 115
        self.rect.left = random.randint(50, 875)

    def update(self):
        global score
        global drops_collected
        self.rect = self.rect.move(random.randrange(3) - 1, 3)
        # If bowl collects
        if pygame.sprite.spritecollideany(self, bowlGR):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            score //= 2
            drops_collected += 1
            mixer.Channel(1).play(mixer.Sound('data\\music\\expl1.mp3'))
        # If bullet kills
        if pygame.sprite.spritecollideany(self, protection):
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()
            mixer.Channel(1).play(mixer.Sound('data\\music\\kill.mp3'))
        if self.rect.top > 1000:
            placeSP_group.add([self])
            placeSP_group.sprites()[0].kill()


cooldown_time = 10
last_press_time = 0
isReady = False

while running:  # Loop of the main window
    nrand = random.randint(0, 1025000)  # Allows drops spawn randomly
    if nrand < 10000:
        twoPointDrop(drops)
    elif 10000 <= nrand < 15000:
        fourPointDrop(drops)
    elif 15000 <= nrand < 20000:
        minusDrop(drops)
    elif 20000 <= nrand < 30000:
        slice(drops)
    elif 30000 <= nrand <= 30500 and healthPoints < 3:
        heartDrop(drops)

    drops.update()
    protection.update()
    # Shoot cooldown
    if pygame.time.get_ticks() - bowl.anim_time > 1000 / bowl.fps:
        bowl.anim_time = pygame.time.get_ticks()
        bowl.current_frame = (bowl.current_frame + 1) % len(frames)
        bowl.image = frames[bowl.current_frame]
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:  # Bowl direction reverse
            if event.key == pygame.K_SPACE:
                mixer.Channel(0).play(mixer.Sound('data\\music\\rotate.mp3'))
                direction *= -1
        current_time = pygame.time.get_ticks()
        if current_time - last_press_time > cooldown_time * 1000:
            isReady = True
        # Shot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if isReady:
                    bullet_1(protection)
                    bullet_2(protection)
                    bullet_3(protection)
                    bullet_4(protection)
                    bullet_5(protection)
                    last_press_time = current_time
                    isReady = False
    # Bowl movement
    if direction == 1:
        bowl.rect.left += 5
        if bowl.rect.left >= 1000:
            bowl.rect.left = -200
    if direction == -1:
        bowl.rect.left -= 5
        if bowl.rect.left <= -200:
            bowl.rect.left = 1000
    # Display screen stuff:
    screen.fill(pygame.Color("royalblue"))
    screen.blit(backGround_image, (0, 0))
    bowlGR.draw(screen)
    protection.draw(screen)
    drops.draw(screen)
    texts(score, drops_collected, posScore, 'middleGame')
    screen.blit(health_image_1, (890, 0))
    if isReady:
        screen.blit(bullet_image_tick, (550, 10))
    else:
        screen.blit(bullet_image_cross, (550, 10))
    if healthPoints == 1:
        screen.blit(health_image_1, (890, 0))
        screen.blit(died_image_2, (780, 0))
        screen.blit(died_image_1, (670, 0))
    if healthPoints == 2:
        screen.blit(health_image_1, (890, 0))
        screen.blit(health_image_2, (780, 0))
        screen.blit(died_image_1, (670, 0))
    if healthPoints == 3:
        screen.blit(health_image_1, (890, 0))
        screen.blit(health_image_2, (780, 0))
        screen.blit(health_image_3, (670, 0))
    pygame.display.flip()
# Final window, after losing all hearts:
size = (WIDTH, HEIGHT) = 600, 200
mixer.music.stop()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game Over!')
running = True
while running:  # Final window loop
    # Draws background and text
    screen.fill(pygame.Color("black"))
    screen.blit(end_image, (0, 0))
    texts(score, drops_collected, posScore, 'gameOver')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()

# Inserts result in the database:
dbp.insert_result('records.db', name, score,
                  round(posScore / (drops_collected) * 100))
