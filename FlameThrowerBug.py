import pygame
import random
import math
import sys
import time

pygame.init()

# Declare variables
WIDTH = 1920
HEIGHT = 1080
FRAMERATE = 60
BUGWIDTH = 180
BUGHEIGHT = 150
SPEED = 2
BALLOONWIDTH = 64
BALLOONHEIGHT = 120
FLAMEWIDTH = 88
FLAMEHEIGHT = 60
ENEMYWIDTH = 150
ENEMYHEIGHT = 150
LIVES = 3
POWER_UP_DURATION = 50  # Power-up duration in milliseconds

playerX = 100
playerY = 100
bullets = []
enemy_bullets = []
shooting = False
slopeX = 0
slopeY = 0
angle = 0
score = 0
level = 1
power_up_active = None
power_up_end_time = 0


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


class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        if power_type == "speed":
            self.image = pygame.transform.scale(speed_power_up, (32, 32))
        elif power_type == "invincibility":
            self.image = pygame.transform.scale(invincibility_power_up, (32, 32))
        elif power_type == "rapid_fire":
            self.image = pygame.transform.scale(rapid_fire_power_up, (32, 32))

    def update(self):
        screen.blit(self.image, (self.x, self.y))

    def checkCollision(self, player_rect):
        return player_rect.colliderect(pygame.Rect(self.x, self.y, 32, 32))


class Enemy:
    SPEED = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = enemy_image.get_width()
        self.height = enemy_image.get_height()
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        screen.blit(enemy_image, (self.x, self.y))
        self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:  # Shoot every second
            slopeX = playerX - self.x
            slopeY = playerY - self.y
            angle = round(math.degrees(math.atan2(slopeX, slopeY)) + 90)
            enemy_bullets.append(Flame(self.x, self.y, angle, slopeX, slopeY))
            self.last_shot_time = current_time


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


def update_level():
    level_text = font.render("Level: " + str(level), 1, pygame.Color("black"))
    return level_text


def spawn_power_up():
    power_type = random.choice(["speed", "invincibility", "rapid_fire"])
    x = random.randint(0, WIDTH - 32)
    y = random.randint(0, HEIGHT - 32)
    return PowerUp(x, y, power_type)


def apply_power_up(power_up):
    global power_up_active, power_up_end_time, SPEED, shooting_interval
    power_up_active = power_up.power_type
    power_up_end_time = pygame.time.get_ticks() + POWER_UP_DURATION
    if power_up_active == "speed":
        SPEED *= 2
    elif power_up_active == "rapid_fire":
        shooting_interval /= 2


def reset_power_up():
    global power_up_active, SPEED, shooting_interval
    if power_up_active == "speed":
        SPEED //= 2
    elif power_up_active == "rapid_fire":
        shooting_interval *= 2
    power_up_active = None


# Draw the scenario
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

enemy_image = pygame.image.load("Enemy2.png")
enemy_image = pygame.transform.scale(enemy_image, (ENEMYWIDTH, ENEMYHEIGHT))

speed_power_up = pygame.image.load("Green-block.png")
invincibility_power_up = pygame.image.load("yellow-block.png")
rapid_fire_power_up = pygame.image.load("red-block.png")

balloonObj = Balloon(random.randint(1, WIDTH - balloon.get_width()), random.randint(1, HEIGHT - balloon.get_height()))

pygame.display.flip()
font = pygame.font.SysFont("Arialms", 18)
clock = pygame.time.Clock()

shooting_interval = 500  # Milliseconds between shots
last_shot_time = pygame.time.get_ticks()

enemies = [Enemy(random.randint(0, WIDTH - ENEMYWIDTH), random.randint(0, HEIGHT - ENEMYHEIGHT)) for _ in range(level)]

# Game loop
running = True
power_up = spawn_power_up()
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                running = False
        elif event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
            slopeX = playerX - mousePos[0]
            slopeY = playerY - mousePos[1]
            angle = round(math.degrees(math.atan2(slopeX, slopeY)) + 90)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            shooting = False

    # Shoot flames
    if shooting and slopeX != 0 and slopeY != 0:
        if current_time - last_shot_time >= shooting_interval:
            bullets.append(Flame(playerX, playerY, angle, slopeX, slopeY))
            last_shot_time = current_time

    # Move player
    if slopeX != 0 and slopeY != 0:
        vels = moving(slopeX, slopeY, SPEED)
        if not borderCheck(playerX - vels[0], playerY - vels[1]):
            playerX -= vels[0]
            playerY -= vels[1]

    # Check power-up collision
    player_rect = pygame.Rect(playerX, playerY, BUGWIDTH, BUGHEIGHT)
    if power_up.checkCollision(player_rect):
        apply_power_up(power_up)
        power_up = spawn_power_up()

    # Check for collisions with enemy bullets
    for bullet in enemy_bullets:
        if player_rect.colliderect(pygame.Rect(bullet.x, bullet.y, FLAMEWIDTH, FLAMEHEIGHT)):
            LIVES -= 1
            enemy_bullets.remove(bullet)
            if LIVES == 0:
                running = False

    # Refresh sprites
    screen.blit(backGround, (0, 0))
    bullets = [bullet for bullet in bullets if bullet.update()]
    enemy_bullets = [bullet for bullet in enemy_bullets if bullet.update()]
    balloonObj.update()
    power_up.update()
    for enemy in enemies:
        enemy.update()
    rotated_bug = pygame.transform.rotate(bug, angle)
    screen.blit(rotated_bug, (playerX - rotated_bug.get_width() // 2, playerY - rotated_bug.get_height() // 2))
    screen.blit(update_fps(), (10, 0))
    screen.blit(update_score(), (10, 20))
    screen.blit(update_lives(), (10, 40))
    screen.blit(update_level(), (10, 60))
    pygame.display.flip()
    clock.tick(FRAMERATE)

    # Check power-up duration
    if power_up_active and current_time >= power_up_end_time:
        reset_power_up()

    # Level progression
    if score >= level * 100:
        level += 1
        SPEED += 1  # Increase difficulty by increasing speed
        enemies.append(Enemy(random.randint(0, WIDTH - ENEMYWIDTH), random.randint(0, HEIGHT - ENEMYHEIGHT)))

pygame.quit()
