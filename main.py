import pygame
from random import randint
pygame.init()


win_w = 600
win_h = 480
FPS = 40

# pygame.mixer_music.load("space.ogg")
# pygame.mixer_music.set_volume(0.1)
# pygame.mixer_music.play(-1)

# fire_snd = pygame.mixer.Sound("fire.ogg")
# 
star_img = pygame.image.load("star.png")


class GameSprite:
    def init(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Pers(GameSprite):
    def init(self, x, y, w, h, image, speed):
        super().init(x, y, w, h, image)
        self.speed = speed
        self.clip = 5

    def move(self, key_left, key_right):
        k = pygame.key.get_pressed()
        if k[key_right]:
            if self.rect.right <= win_w:
                self.rect.x += self.speed 
        elif k[key_left]:
            if self.rect.left >= 0:
                self.rect.x -= self.speed

    def shoot(self):
        if self.clip > 0:
        # fire_snd.play()
            b = Star(self.rect.centerx-7, self.rect.y, 15, 20, star_img, 4)
            self.clip -= 1
    def reload(self):
        if self.clip <= 0:
            self.clip = 5

class Enemy(GameSprite):
    def init(self, x, y, w, h, image, speed):
        super().init(x, y, w, h, image)
        self.speed = speed
        # self.direction = direction
        # self.x2 = x2
        # self.x1 = x
    
    def move(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            lost += 1
            print(lost)
            self.rect.x = randint(0, win_w - self.rect.w)
            self.rect.y = randint(-500, -self.rect.h)
            self.speed = randint(1, 3)

stars = []
class Star(GameSprite):
    def init(self, x, y, w, h, image, speed):
        super().init(x, y, w, h, image)
        self.speed = speed
        stars.append(self)
    
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= -20:
            stars.remove(self)
    
font1 = pygame.font.SysFont("Arial", 20)
font2 = pygame.font.SysFont("Arial", 50)

reload_alert = font1.render("Щоб перезарядитись, натисни E", True, (255, 0, 0))

window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Shooter 0.1")
clock = pygame.time.Clock()

background = pygame.image.load("forest.jpg")
background = pygame.transform.scale(background, (win_w, win_h))
window.blit(background, (0, 0))


hero = pygame.image.load("ninlab.jpg")
hero = Pers(330, 400, 50, 60, star_img, 5)

enemy_img = pygame.image.load("ninjar.jpg") 

enemies = []
for i in range(5):
    enemy = Enemy(randint(0, win_w-50), randint(-500, 0), 70, 40, enemy_img, randint(1, 3))
    enemies.append(enemy)

# record
with open("record.txt", "r", encoding="UTF-8") as file:
    record = int(file.read())

print(record)
def new_record(old, new):
    if new > old:
        with open("record.txt", "w", encoding="UTF-8") as file:
            file.write(str(new))        

score = 0
lost = 0
game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        hero.update()
        hero.move(pygame.K_a, pygame.K_d)
        for enemy in enemies:
            enemy.update()
            enemy.move()
            if hero.rect.colliderect(enemy.rect):
                finish = True
                new_record(record, score)
                game_over = font2.render("Game Over", True, (255, 0, 0))
            for star in stars:
                if star.rect.colliderect(enemy.rect):
                    score += 1
                    # print(score)
                    enemy.rect.x, enemy.rect.y = randint(0, win_w-50), randint(-500, 0)
                    star.remove(star)
