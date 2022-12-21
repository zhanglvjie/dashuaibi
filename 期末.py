import os
import sys
import cfg
import random
import pygame
from modules import *
from random import randint
import time,sys

# 玩家
class Player:

    def __init__(self,stoneNumber):
        self.stoneNumber = stoneNumber # 灵石数量
        self.warriors = {}  # 拥有的战士，包括弓箭兵和斧头兵

# 战士
class Warrior:

    # 初始化参数是生命值
    def __init__(self, strength):
        self.strength = strength

    # 用灵石疗伤
    def healing(self, stoneCount):
        # 如果已经到达最大生命值，灵石不起作用，浪费了
        if self.strength == self.maxStrength:
            return

        self.strength += stoneCount

        # 不能超过最大生命值
        if self.strength > self.maxStrength:
            self.strength = self.maxStrength


# 弓箭兵 是 战士的子类
class Archer(Warrior):
    # 种类名称
    typeName = '弓箭兵'

    # 雇佣价 100灵石，属于静态属性
    price = 100

    # 最大生命值 ，属于静态属性
    maxStrength = 100


    # 初始化参数是生命值, 名字
    def __init__(self, name, strength = maxStrength):
        Warrior.__init__(self, strength)
        self.name = name

    # 和妖怪战斗
    def fightWithMonster(self,monster):
        if monster.typeName== '鹰妖':
            self.strength -= 20
        elif monster.typeName== '狼妖':
            self.strength -= 80
        else:
            print('未知类型的妖怪！！！')



# 斧头兵 是 战士的子类
class Axeman(Warrior):
    # 种类名称
    typeName = '斧头兵'

    # 雇佣价 120灵石
    price = 120

    # 最大生命值
    maxStrength = 120


    # 初始化参数是生命值, 名字
    def __init__(self, name, strength = maxStrength):
        Warrior.__init__(self, strength)
        self.name = name

    # 和妖怪战斗
    def fightWithMonster(self,monster):
        if monster.typeName== '鹰妖':
            self.strength -= 80
        elif monster.typeName== '狼妖':
            self.strength -= 20
        else:
            print('未知类型的妖怪！！！')

# 鹰妖
class Eagle():
    typeName = '鹰妖'

# 狼妖
class Wolf():
    typeName = '狼妖'

# 森林
class Forest():
    def __init__(self,monster):
        # 该森林里面的妖怪
        self.monster = monster

print('''
***************************************
****           游戏开始             ****
***************************************

'''
)

# 森林数量
forest_num = 7

# 森林 列表
forestList = []

# 为每座森林随机产生 鹰妖或者 狼妖
notification = '前方森林里的妖怪是：'  # 显示在屏幕上的内容
for i in range(forest_num):
    typeName = randint(0,1)
    if typeName == 0:
        forestList.append( Forest(Eagle()) )
    else:
        forestList.append( Forest(Wolf()) )

    notification += \
        f'第{i+1}座森林里面是 {forestList[i].monster.typeName}  '

# 显示 妖怪信息
print(notification,end='')
def startGame(screen):
   clock = pygame.time.Clock()
   # 加载字体
   font = pygame.font.SysFont('arial', 18)
   if not os.path.isfile('score'):
       f = open('score', 'w')
       f.write('0')
       f.close()
   with open('score', 'r') as f:
       highest_score = int(f.read().strip())
   # 敌方
   enemies_group = pygame.sprite.Group()
   for i in range(55):
       if i < 11:
           enemy = enemySprite('small', i, cfg.WHITE, cfg.WHITE)
       elif i < 33:
           enemy = enemySprite('medium', i, cfg.WHITE, cfg.WHITE)
       else:
           enemy = enemySprite('large', i, cfg.WHITE, cfg.WHITE)
       enemy.rect.x = 85 + (i % 11) * 50
       enemy.rect.y = 120 + (i // 11) * 45
       enemies_group.add(enemy)
   boomed_enemies_group = pygame.sprite.Group()
   en_bullets_group = pygame.sprite.Group()
   ufo = ufoSprite(color=cfg.RED)
   # 我方
   myaircraft = aircraftSprite(color=cfg.GREEN, bullet_color=cfg.WHITE)
   my_bullets_group = pygame.sprite.Group()
   # 用于控制敌方位置更新
   # --移动一行
   enemy_move_count = 24
   enemy_move_interval = 24
   enemy_move_flag = False
   
   
   enemy_shot_interval = 100
   enemy_shot_count = 0
   enemy_shot_flag = False
  
   running = True
   is_win = False
  
   while running:
       screen.fill(cfg.BLACK)
       for event in pygame.event.get():
          
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   pygame.quit()
                   sys.exit()
           
           if event.type == pygame.MOUSEBUTTONDOWN:
               my_bullet = myaircraft.shot()
               if my_bullet:
                   my_bullets_group.add(my_bullet)
       
       for enemy in enemies_group:
           if pygame.sprite.spritecollide(enemy, my_bullets_group, True, None):
               boomed_enemies_group.add(enemy)
               enemies_group.remove(enemy)
               myaircraft.score += enemy.reward
       if pygame.sprite.spritecollide(ufo, my_bullets_group, True, None):
           ufo.is_dead = True
           myaircraft.score += ufo.reward
       
       enemy_shot_count += 1
       if enemy_shot_count > enemy_shot_interval:
           enemy_shot_flag = True
           enemies_survive_list = [enemy.number for enemy in enemies_group]
           shot_number = random.choice(enemies_survive_list)
           enemy_shot_count = 0
     
       enemy_move_count += 1
       if enemy_move_count > enemy_move_interval:
           enemy_move_count = 0
           enemy_move_flag = True
           enemy_need_move_row -= 1
           if enemy_need_move_row == 0:
               enemy_need_move_row = enemy_max_row
           enemy_change_direction_count += 1
           if enemy_change_direction_count > enemy_change_direction_interval:
               enemy_change_direction_count = 1
               enemy_move_right = not enemy_move_right
               enemy_need_down = True
              
       for enemy in enemies_group:
           if enemy_shot_flag:
               if enemy.number == shot_number:
                   en_bullet = enemy.shot()
                   en_bullets_group.add(en_bullet)
           if enemy_move_flag:
               if enemy.number in range((enemy_need_move_row-1)*11, enemy_need_move_row*11):
                   if enemy_move_right:
                       enemy.update('right', cfg.SCREENSIZE[1])
                   else:
                       enemy.update('left', cfg.SCREENSIZE[1])
           else:
               enemy.update(None, cfg.SCREENSIZE[1])
           if enemy_need_down:
               if enemy.update('down', cfg.SCREENSIZE[1]):
                   running = False
                   is_win = False
               enemy.change_count -= 1
           enemy.draw(screen)
       enemy_move_flag = False
       enemy_need_down = False
       enemy_shot_flag = False
       
       for boomed_enemy in boomed_enemies_group:
           if boomed_enemy.boom(screen):
               boomed_enemies_group.remove(boomed_enemy)
               del boomed_enemy
      
       if not myaircraft.one_dead:
           if pygame.sprite.spritecollide(myaircraft, en_bullets_group, True, None):
               myaircraft.one_dead = True
       if myaircraft.one_dead:
           if myaircraft.boom(screen):
               myaircraft.resetBoom()
               myaircraft.num_life -= 1
               if myaircraft.num_life < 1:
                   running = False
                   is_win = False
       else:
           
           myaircraft.update(cfg.SCREENSIZE[0])
          
           myaircraft.draw(screen)
       if (not monster.has_boomed) and (monster.is_dead):
           if monster.boom(screen):
               monster.has_boomed = True
       else:

           monster.update(cfg.SCREENSIZE[0])
           
           monster.draw(screen)
       
       for bullet in my_bullets_group:
           if bullet.update():
               my_bullets_group.remove(bullet)
               del bullet
           else:
               bullet.draw(screen)
       
       for bullet in en_bullets_group:
           if bullet.update(cfg.SCREENSIZE[1]):
               en_bullets_group.remove(bullet)
               del bullet
           else:
               bullet.draw(screen)
       if myaircraft.score > highest_score:
           highest_score = myaircraft.score
      
       if (myaircraft.score % 100 == 0) and (myaircraft.score > 0) and (myaircraft.score != myaircraft.old_score):
           myaircraft.old_score = myaircraft.score
           myaircraft.num_life = min(myaircraft.num_life + 1, myaircraft.max_num_life)
       
       if len(enemies_group) < 1:
           is_win = True
           running = False
      
       
       showLife(screen, myaircraft.num_life, cfg.GREEN)
       pygame.display.update()
       clock.tick(cfg.FPS)
   with open('score', 'w') as f:
       f.write(str(highest_score))
   return is_win
 
 

def main():
   
   pygame.init()
   pygame.display.set_caption('当选国王')
   screen = pygame.display.set_mode(cfg.SCREENSIZE)
   pygame.mixer.init()
   pygame.mixer.music.load(cfg.BGMPATH)
   pygame.mixer.music.set_volume(0.4)
   pygame.mixer.music.play(-1)
   while True:
       is_win = startGame(screen)
       endInterface(screen, cfg.BLACK, is_win)
 
 
'''run'''
if __name__ == '__main__':
   main()