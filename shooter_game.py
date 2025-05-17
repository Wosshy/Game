import pygame
from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)  # Зацикливание музыки
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.Font(None, 80)
win_text = font1.render("YOU WIN", True, (225, 225, 225))
lose_text = font1.render("YOU LOSE", True, (180, 0, 0))

font2 = font.Font(None, 36)

win_width = 700
win_height = 500

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
score = 0
goal = 10
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost += 1  # Увеличиваем счетчик пропущенных врагов

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

pygame.init()
window = display.set_mode((win_width, win_height))
pygame.display.set_caption('Шутер')
background = transform.scale(image.load(img_back), (win_width, win_height))
clock = pygame.time.Clock()
FPS = 60

monsters = sprite.Group()
for i in range(3):  # Создаем троих врагов
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
run = True

# Создаем игрока
ship = Player(img_hero, 5, win_height - 100, 10)  # Исправлено: передаем только нужные аргументы

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        colliders = sprite.groupcollide(monsters, bullets, True, True)
        for c in colliders:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))

        text = font2.render('Счет:' + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()
    else:
        score = 0
        lost = 0
        bullets.empty()
        monsters.empty()

        time.delay(1000)

        for i in range(3):  # Создаем троих врагов после окончания игры
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)

    clock.tick(FPS)

pygame.quit()
