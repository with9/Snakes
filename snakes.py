import pygame
import sys
import random
import time
import os
class Point():
    def __init__(self, x=0, y=0):
        self.x = x  # 行
        self.y = y  # 列
def judge_point(a, b):  # 判断两个point类是否值相等的函数
    if a.x == b.x and a.y == b.y:
        return True
    else:
        return False
WIDTH = 800
HIGHT = 600
block_size = (50, 50)
ROW = int(HIGHT/block_size[0])
COL = int(WIDTH/block_size[1])
pygame.init()
all_points = []
for i in range(ROW):
    for j in range(COL):
        all_points.append(Point(j, i))
all_points_virtual=all_points[:]
Bg_color = (255, 255, 255)  # 设置背景颜色,白色
Head_color = (0, 0, 0)  # 设置蛇头颜色,黑色
Snake_color=(125,125,125)
Line_color=(215,0,95)
Food_color = (0, 125, 0)
screen_size = (WIDTH, HIGHT)
head = Point(int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
food = Point(head.x - int(COL/4), head.y)
snakes = [Point(head.x + 1, head.y), Point(head.x + 2, head.y), Point(head.x + 3, head.y),
          Point(head.x + 3, head.y + 1)]
#使得所有的point类都来自于all_point列表
for i in all_points:
    if judge_point(head,i):
        head=i
    if judge_point(food,i):
        food=i
for i in all_points:
    for snake in snakes:
        if judge_point(i,snake):
            snake=i       
windows = pygame.display.set_mode(screen_size)
pygame.display.set_caption("贪吃蛇尝试")
# 标题显示
clock = pygame.time.Clock()  # 生成时钟的对象
direct = None
death = False
eatten = False  # 标记是否食物被吃掉的变量
clocktrick=10
directs=["left","up","down","right"]
Quit=False
while not Quit:
    pygame.Surface.fill(windows, Bg_color)
    for j in range(ROW+1):
        pygame.draw.line(windows,Line_color,(0,j*block_size[0]),(COL*block_size[0],j*block_size[0]))
    for j in range(COL+1):
        pygame.draw.line(windows,Line_color,(j*block_size[0],0),(j*block_size[0],COL*block_size[0]))
    for snake in snakes:
        pygame.draw.rect(windows,Snake_color , ((snake.x * block_size[0], snake.y * block_size[0]), block_size))
    pygame.draw.rect(windows, Food_color, ((food.x * block_size[0], food.y * block_size[0]), block_size))
    pygame.draw.rect(windows, Head_color, ((head.x * block_size[0], head.y * block_size[0]), block_size))  # 蛇头绘制
    if food.x == head.x and food.y == head.y:  # 两个个方块重合,吃到食物
        eatten = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
            sys.exit()
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            """ if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == 273 and direct != "down":
                direct = "up"
                break
            if event.key == 274 and direct != "up":
                direct = "down"
                break
            if event.key == 276 and direct != "right":
                direct = "left"
                break
            if event.key == 275 and direct != "left":
                direct = "right"
                break """
            ##控制速度
            if event.key==91 :
                clocktrick=clocktrick*0.9
                break
            if event.key==93:
                clocktrick=clocktrick+10
                break
            if event.key==8:
                clocktrick=10
    # 蛇头移动
    if direct == "up" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, Point(head.x, head.y))
        head.y = head.y - 1
    if direct == "down":
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, Point(head.x, head.y))
        head.y = head.y + 1
    if direct == "left" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, Point(head.x, head.y))
        head.x = head.x - 1
    if direct == "right" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, Point(head.x, head.y))
        head.x = head.x + 1
    all_points_tp =[]  # 创建临时列表,用于生成食物
    for p in all_points:
        all_points_tp.append(p)
    if eatten:
        ovet=True
        while True:
            food = random.choice(all_points_tp)
            for snake in snakes + [head]:
                if judge_point(food, snake):
                    all_points_tp.remove(food)
                    ovet = False
                    break
            if ovet:
                break
        for i in all_points:
            if judge_point(i,food):
                food=i
        eatten = False

    # 判断是否被吃掉
    # 判断是否死亡
    if head.x < 0 or head.x >= COL or head.y < 0 or head.y >= ROW:
        death = True
    for snake in snakes:
        if judge_point(head, snake):
            death = True
            break

    clock.tick(clocktrick)  # 控制帧率
    pygame.display.flip()  # 渲染,释放控制权
    if death:
        head = Point(int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
        food = Point(head.x-int(COL/4), head.y)
        snakes = [Point(head.x + 1, head.y), Point(head.x + 2, head.y), Point(head.x + 3, head.y),
                  Point(head.x + 3, head.y + 1)]      
        death = False
        direct = None
        # time.sleep(3)
    for i in all_points:
        if judge_point(head,i):
            head=i
        if judge_point(food,i):
            food=i
    for i in all_points:
        for snake in snakes:
            if judge_point(i,snake):
                snake=i       
