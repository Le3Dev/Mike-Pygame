import pygame
from random import randint
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import  event
from pygame.locals import QUIT, KEYUP , K_SPACE
from  pygame.time import Clock
from pygame import font

pygame.init()

sizeScreen = (800,600)
mikeSize = (60,60)
boneSize = (20,20)
fonte = font.SysFont('poppings',50)
fontLose = font.SysFont('poppings', 100)

screen = display.set_mode(sizeScreen,display=1);

display.set_caption(
    'MIKE E OS GATOS INVASORES'
)

background = scale(
    load('./img/parkBackground.jpg'),
    sizeScreen)



class Mike(Sprite):
    def __init__(self, bones):
        super().__init__()

        self.image = load('./img/MikeCerto.png')
        self.rect = self.image.get_rect()
        self.bones = bones
        self.speed = 2
    def throwBones(self):

        if len(self.bones) < 10:
            self.bones.add(
                Bone(*self.rect.center)
            )
    def update(self):
        keys = pygame.key.get_pressed()
        bonesFont= fonte.render(
            f'Bones: {10 - len(self.bones)}',
            True,
            (0,0,0)
        )
        screen.blit(bonesFont, (20, 20))
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Bone(Sprite):
    def __init__(self,x ,y):
        super().__init__()

        self.image = load('./img/OssoCerto.png')
        self.rect =self.image.get_rect(
            center = (x,y)
        )

    def update(self):
        self.rect.x += 2
        if self.rect.x> sizeScreen[0]:
            self.kill()


class EvilCat(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('./img/EvilCatCerto.png')
        self.rect = self.image.get_rect(
            center=(800, randint(20, 580))
        )
        self.pos_x = float(self.rect.x)  # Armazena posição x como float
        self.velocidade = 0.8 # Define a velocidade com valor decimal

    def update(self):
        global lose
        self.pos_x -= self.velocidade  # Atualiza a posição x com valor decimal
        self.rect.x = int(self.pos_x)   # Atualiza o rect com a parte inteira

        if self.rect.x <= 0:
            self.kill()
            lose =True



def drawBotton(text, x, y, width, height, color, hoverColor):
    mouse = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        if mouseClick[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    textSurface = fonte.render(text, True, (0, 0, 0))
    screen.blit(textSurface, (x + (width // 2 - textSurface.get_width() // 2), y + (height // 2 - textSurface.get_height() // 2)))
    return False



def restartButton():
    global deaths, lose, round
    deaths = 0
    lose = False
    round = 0
    group_enemies.empty()
    group_bone.empty()
    group_enemies.add(EvilCat())
    mike.rect.center = (400, 300)


clock = Clock()
deaths = 0
round = 0
lose = False
group_enemies = Group()
group_bone = Group()
mike = Mike(group_bone)
group_mike = GroupSingle(mike)

group_enemies.add(EvilCat())

while True:
    clock.tick(120)
    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()
        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                mike.throwBones()
    if not lose:
        if round % 120 ==0:
            if deaths < 20:
               group_enemies.add(EvilCat())
            for i in range(int(deaths / 20)):
                group_enemies.add(EvilCat())


        if groupcollide(group_bone,group_enemies,True,True):
            deaths += 1

        screen.blit(background, (0,0))

        deathsFont = fonte.render(
            f'Kills: {deaths}',
            True,
            (0, 0, 0)
        )
        screen.blit(deathsFont,(20,70))
        group_enemies.draw(screen)
        group_mike.draw(screen)
        group_bone.draw(screen)

        group_bone.update()
        group_enemies.update()
        group_mike.update()

    if lose:
        gameOver = fontLose.render(
            'Game Over',
            True,
            (255,0,0)
        )
        screen.blit(gameOver,(200,200))
        display.update()
        if drawBotton("Restart", 350, 400, 150, 50, (0, 255, 0), (50, 205, 50)):
            restartButton()

    display.update()
    round+=1