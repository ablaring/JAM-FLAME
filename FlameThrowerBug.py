import pygame
import random
import math
import sys

pygame.init()

# Declare variables
WIDTH = 478
HEIGHT = 300
FRAMERATE = 60
BUGWIDTH = 60
BUGHEIGHT = 50
SPEED = 2
BALLOONWIDTH = 32
BALLOONHEIGHT = 60
FLAMEWIDTH = 48
FLAMEHEIGHT = 30
LIVES = 3

playerX = 100
playerY = 100
bullets = []
shooting = False
slopeX = 0
slopeY = 0
angle = 0
score = 0

# Game states
MENU = 0
MANUAL = 1
AI = 2
game_state = MENU

# Declare classes
class Flame:
    SPEED = 3

    def __init__(self, x, y, angle, slopeX, slopeY):
        self.x = x
        self.y = y
        self.slopeX = slopeX
        self.slopeY = slopeY
        self.angle = angle
        self.img = pygame.transform.rotate(flame, angle)
        self.vels = moving(self.slopeX, self.slopeY, self.SPEED)

    def checkCollision(self):
        global score
        if (self.x + flame.get_width() >= balloonObj.x and
                self.x <= balloonObj.x + balloon.get_width() and
                self.y + flame.get_height() >= balloonObj.y and
                self.y <= balloonObj.y + balloon.get_height()):
            balloonObj.popped()
            pygame.mixer.Sound.play(pop_sound)
            score += 10
            return True
        return False

    def update(self):
        if self.checkCollision() or borderCheck(self.x, self.y):
            return False
        self.x -= self.vels[0]
        self.y -= self.vels[1]
        screen.blit(self.img, (round(self.x), round(self.y)))
        return True


class Balloon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = balloon.get_width()
        self.height = balloon.get_height()

    def popped(self):
        self.x = random.randint(1, WIDTH - balloon.get_width())
        self.y = random.randint(1, HEIGHT - balloon.get_height())

    def update(self):
        screen.blit(balloon, (self.x, self.y))


def moving(slopeX, slopeY, speed):
    if abs(slopeX) > abs(slopeY):
        vx = math.copysign(speed, slopeX)
        a = abs(slopeX / speed)
        vy = slopeY / a
    else:
        vy = math.copysign(speed, slopeY)
        a = abs(slopeY / speed)
        vx = slopeX / a
    return vx, vy


def borderCheck(x, y):
    return x > WIDTH or x < 0 or y > HEIGHT or y < 0


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render("fps: " + fps, 1, pygame.Color("black"))
    return fps_text


def update_score():
    score_text = font.render("Score: " + str(score), 1, pygame.Color("black"))
    return score_text


def update_lives():
    lives_text = font.render("Lives: " + str(LIVES), 1, pygame.Color("black"))
    return lives_text


def draw_menu():
    screen.fill((255, 255, 255))
    title = font.render("FlameThrowerBug", True, (0, 0, 0))
    manual_option = font.render("1. Play Manually", True, (0, 0, 0))
    ai_option = font.render("2. Watch AI Play", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(manual_option, (WIDTH // 2 - manual_option.get_width() // 2, HEIGHT // 2))
    screen.blit(ai_option, (WIDTH // 2 - ai_option.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.flip()


def ai_logic():
    global playerX, playerY, slopeX, slopeY, angle, shooting
    slopeX = playerX - balloonObj.x
    slopeY = playerY - balloonObj.y
    angle = round(math.degrees(math.atan2(slopeX, slopeY)) + 90)
    shooting = True
    if slopeX != 0 and slopeY != 0:
        vels = moving(slopeX, slopeY, SPEED)
        if not borderCheck(playerX - vels[0], playerY - vels[1]):
            playerX -= vels[0]
            playerY -= vels[1]

# Load assets
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlameThrowerBug")

backGround = pygame.image.load("BackGround.png")
backGround = pygame.transform.scale(backGround, (WIDTH, HEIGHT))

bug = pygame.image.load("Bug.png")
bug = pygame.transform.scale(bug, (BUGWIDTH, BUGHEIGHT))

balloon = pygame.image.load("Balloon.png")
balloon = pygame.transform.scale(balloon, (BALLOONWIDTH, BALLOONHEIGHT))
pop_sound = pygame.mixer.Sound("Pop.wav")

flame = pygame.image.load("Flame.png")
flame = pygame.transform.scale(flame, (FLAMEWIDTH, FLAMEHEIGHT))

balloonObj = Balloon(random.randint(1, WIDTH - balloon.get_width()), random.randint(1, HEIGHT - balloon.get_height()))

pygame.display.flip()
font = pygame.font.SysFont("Arialms", 18)
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_1:
                    game_state = MANUAL
                elif event.key == pygame.K_2:
                    game_state = AI
            elif event.key == pygame.K_d:
                running = False
        elif event.type == pygame.MOUSEMOTION and game_state == MANUAL:
            mousePos = event.pos
            slopeX = playerX - mousePos[0]
            slopeY = playerY - mousePos[1]
            angle = round(math.degrees(math.atan2(slopeX, slopeY)) + 90)
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == MANUAL:
            shooting = True
        elif event.type == pygame.MOUSEBUTTONUP and game_state == MANUAL:
            shooting = False

    if game_state == MENU:
        draw_menu()
        continue

    # Shoot flames
    if shooting and slopeX != 0 and slopeY != 0:
        bullets.append(Flame(playerX, playerY, angle, slopeX, slopeY))

    if game_state == MANUAL:
        # Move player
        if slopeX != 0 and slopeY != 0:
            vels = moving(slopeX, slopeY, SPEED)
            if not borderCheck(playerX - vels[0], playerY - vels[1]):
                playerX -= vels[0]
                playerY -= vels[1]
    elif game_state == AI:
        ai_logic()

    # Refresh sprites
    screen.blit(backGround, (0, 0))
    bullets = [bullet for bullet in bullets if bullet.update()]
    balloonObj.update()
    rotated_bug = pygame.transform.rotate(bug, angle)
    screen.blit(rotated_bug, (playerX - rotated_bug.get_width() // 2, playerY - rotated_bug.get_height() // 2))
    screen.blit(update_fps(), (10, 0))
    screen.blit(update_score(), (10, 20))
    screen.blit(update_lives(), (10, 40))
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()
