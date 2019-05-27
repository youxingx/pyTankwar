import pygame # www.pygame.org/docs
import sys
import time
import random
from pygame.locals import *


# 坦克大战游戏中所有对象的父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass

    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image, self.rect)

class Tank(BaseItem):
    width = 60
    height = 60

    def __init__(self, screen, left, top):
        super().__init__()
        self.screen = screen
        self.direction = "U" # 坦克方向默认向上(上下左右)
        self.speed = 5
        self.images = {}
        self.images["L"] = pygame.image.load('images/p1tankL.gif')
        self.images["R"] = pygame.image.load('images/p1tankR.gif')
        self.images["U"] = pygame.image.load('images/p1tankU.gif')
        self.images["D"] = pygame.image.load('images/p1tankD.gif')
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        # print(self.rect)
        self.rect.left = left
        self.rect.top = top
        # print(self.rect)
        # print(self.rect.height)
        # print(self.rect.width)
        # print(dir(self.rect))
        self.live = True # 决定坦克是否消灭了

    # 把坦克显示在对应的窗口上
    def display(self):
        self.image = self.images[self.direction]
        self.screen.blit(self.image, self.rect)
        pass

    def move(self):
        if not self.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
                pass
            elif self.direction =="R":
                if self.rect.right < TankMain.width:
                    self.rect.left += self.speed
                pass
            elif self.direction =="U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
                pass
            elif self.direction =="D":
                if self.rect.bottom < TankMain.height:
                    self.rect.top += self.speed
                pass
        pass

    def fire(self):
        pass

class Bullet(BaseItem):
    width = 16
    height = 16
    def __init__(self, screen, tank):
        super().__init__()
        self.screen = screen
        self.tank = tank
        self.direction = tank.direction  # 炮弹方向有发射的坦克方向决定
        self.speed = 12
        self.images = {}
        self.images["L"] = pygame.image.load('images/bulletL.png')
        self.images["R"] = pygame.image.load('images/bulletR.png')
        self.images["U"] = pygame.image.load('images/bulletU.png')
        self.images["D"] = pygame.image.load('images/bulletD.png')
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + (tank.width - self.width)//2
        self.rect.top = tank.rect.top + (tank.height - self.height)//2
        self.live = True  # 决定炮弹是否消灭了

    def move(self):
        if self.live:
            if self.direction == "L":
                if self.rect.left>0:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif self.direction == "U":
                if self.rect.top>0:
                    self.rect.top -= self.speed
                else:
                    self.live = False
            if self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False

class MyTank(Tank):
    def __init__(self, screen):
        super().__init__(screen, 370, 540)
        self.stop = True
        self.speed = 8

    def fire(self):
        m = Bullet(self.screen, self)
        return m
        pass

class EnemyTank(Tank):
    def __init__(self, screen):
        init_x = [0, 370, 740]
        super().__init__(screen, init_x[random.randint(0,2)], 0)
        self.images["L"] = pygame.image.load('images/enemy1L.gif')
        self.images["R"] = pygame.image.load('images/enemy1R.gif')
        self.images["U"] = pygame.image.load('images/enemy1U.gif')
        self.images["D"] = pygame.image.load('images/enemy1D.gif')
        self.image = self.images[self.direction]
        self.stop = False
        self.speed = 5
        self.get_random_direction()

    def get_random_direction(self):
        r = random.randint(0, 3)
        # if r == 4:
        #     self.stop = True
        if r == 0:
            self.direction = "L"
        elif r == 1:
            self.direction = "R"
        elif r == 2:
            self.direction = "U"
        elif r == 3:
            self.direction = "D"

    # 一直移动，直到碰到墙壁或到窗口边界，随机改变方向
    def random_move(self):
        if self.live:
            if self.direction == "L" and self.rect.left == 0:
                self.get_random_direction()
            elif self.direction == "R" and self.rect.right == TankMain.width:
                self.get_random_direction()
            elif self.direction == "U" and self.rect.top == 0:
                self.get_random_direction()
            elif self.direction == "D" and self.rect.bottom == TankMain.height:
                self.get_random_direction()
            self.move()
            # if self.rect.left == 0:
        pass

class TankMain(object):
    '''坦克大战的主窗口'''
    width = 800
    height = 600

    my_tank_bullet_list = []
    enemyList = []
    # 开始游戏的方法
    def startGame(self):
        pygame.init() # pygame模块初始化，加载系统资源
        # 创建一个屏幕， 屏幕的大小(宽和高), 窗口大小是否可变（0，RESIZEABLE，FULLSCREEM），颜色位数
        screen = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        # 给窗口设置一个标题
        pygame.display.set_caption("坦克大战")

        myTank = MyTank(screen)
        # enemy = EnemyTank(screen)
        for i in range(0, 3):
            TankMain.enemyList.append(EnemyTank(screen))
        while True:
            # 设置屏幕变景色为黑色 color RGB(0,0,0)
            screen.fill((0, 0, 0))
            # 显示文字
            for i, text in enumerate(self.writeText(), 0):
                screen.blit(text, (0, 5 + 18*i))
            self.getEvent(myTank)

            myTank.display()
            myTank.move()

            # 显示所有的敌方坦克
            for enemy in TankMain.enemyList:
                enemy.display()
                enemy.random_move()

            for m in TankMain.my_tank_bullet_list:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.my_tank_bullet_list.remove(m)

            time.sleep(0.05)
            # 显示重置
            pygame.display.update()
        pass

    # 获取所有事件
    def getEvent(self, myTank):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    myTank.direction = "L"
                    myTank.stop = False
                    pass
                if event.key == K_RIGHT or event.key == K_d:
                    myTank.direction = "R"
                    myTank.stop = False
                    pass
                if event.key == K_UP or event.key == K_w:
                    myTank.direction = "U"
                    myTank.stop = False
                    pass
                if event.key == K_DOWN or event.key == K_s:
                    myTank.direction = "D"
                    myTank.stop = False
                    pass
                if event.key == K_SPACE:
                    TankMain.my_tank_bullet_list.append(myTank.fire())
                if event.key == K_ESCAPE:
                    self.stopGame()
                    pass
                pass
            if event.type == MOUSEBUTTONUP:
                pass
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_UP:
                    myTank.stop = True

    # 关闭游戏
    def stopGame(self):
        sys.exit();
        pass

    # 设置标题
    def setTitle(self):
        pass

    # 在屏幕左上角显示文字
    def writeText(self):
        font = pygame.font.SysFont("simsunnsimsun", 18)
        text_sf1 = font.render("敌方坦克:%d"%len(TankMain.enemyList), True, (255, 0, 0))
        text_sf2 = font.render("炮弹数量:%d"%len(TankMain.my_tank_bullet_list), True, (255, 0, 0))
        return text_sf1, text_sf2
        pass


if __name__ == '__main__':
    # print(pygame.font.get_fonts())
    game = TankMain()
    game.startGame()
