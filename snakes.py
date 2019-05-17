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


# 判断最高分文件是否存在,不存在时创建
if not os.path.exists("high_score"):
    with open("high_score", "w")as f:
        f.write("0\n")
        f.close()
with open("high_score", "r")as f:
    highscore = int(f.readlines()[-1])
    f.close()
def find_list_index(ste,list1):
    for i in range(len(list1)):
        if ste==list1[i]:
            return i
def safe(direct,head,snakes,COL,ROW):#判断目前方向会不会造成死亡,并返回方向字符串..
    if direct=="left":
        flags=[0,0,0]
        snake_distance=[0,0]
        #第一个1标记有无危险,第二个2标记up有危险,第三个标记down有危险
        #0  代表没有危险,不用动方向
        #1  代表up有危险,方向向down
        #2  代表down有危险,方向向up
        #3  代表都有危险,这时候看蛇那边是更列表更长
        for snake in snakes:
            if (snake.y==head.y and snake.x+1==head.x) or head.x==0:
                flags[0]=1
                for snake_two in snakes:
                    if (snake_two.x==head.x and snake_two.y<=head.y):
                        flags[1]=1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two.x==head.x and snake_two.y>head.y:
                        flags[2]=1
                        snake_distance[1] = find_list_index(snake_two, snakes)
                        break
        flag=sum(flags)
        if flag==0:
            pass
        if flag==1:
            direct=random.choice(["up","down"])
        elif flags[1]==1 and flags[2]==0:
            direct="down"
        elif flags[2]==1 and flags[1]==0:
            direct="up"
        elif flag==3:
            if snake_distance[0]>=snake_distance[1]:
                direct="up"
            else:
                direct="down"
        return direct
    if direct=="up":
        flags=[0,0,0]
        snake_distance=[0,0]
        #0 安全,不用动方向
        #1 left危险,方向right
        #2 right危险.方向left
        #3 都危险,方向看蛇尾巴
        for snake in snakes:
            if (snake.x==head.x and snake.y+1==head.y) or head.y==0:
                flags[0]=1
                for snake_two in snakes:
                    if snake_two.y==head.y and snake_two.x<=head.x:
                        flags[1]=1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two.y==head.y and snake_two.x>head.x:
                        flags[2]=1
                        snake_distance[1] = find_list_index(snake_two, snakes)
                        break
        if sum(flags)==0:
            pass
        if sum(flags)==1:
            print("up is danger ,random direct")
            direct=random.choice(["left","right"])
        if sum(flags)==3:
            if snake_distance[0]<=snake_distance[1]:
                print("up is all danger to right")
                direct="right"
            else:
                print("up is all danger to right")
                direct="left"
        else:
            if flags[1]==1:
                print("up is danger,right is safe")
                direct="right"
            if flags[2]==1:
                print("up is danger,left is safe")
                direct="left"
        return direct
    if direct=="right":
        flags = [0, 0, 0]
        snake_distance=[0,0]
        # 第一个1标记有无危险,第二个2标记up有危险,第三个标记down有危险
        # 0  代表没有危险,不用动方向
        # 1  代表up有危险,方向向down
        # 2  代表down有危险,方向向up
        # 3  代表都有危险,这时候看蛇尾巴在什么地方
        for snake in snakes:
            if (snake.y == head.y and snake.x - 1 == head.x) or head.x >= COL-1:
                flags[0] = 1
                for snake_two in snakes:
                    if (snake_two.x == head.x and snake_two.y <= head.y):
                        flags[1] = 1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two.x == head.x and snake_two.y > head.y:
                        flags[2] = 1
                        snake_distance[1] = find_list_index(snake_two, snakes)
                        break
        flag = sum(flags)
        if flag == 0:
            pass
        if flag == 1:
            direct = random.choice(["up", "down"])
        elif flags[1] == 1 and flags[2] == 0:
            direct = "down"
        elif flags[2] == 1 and flags[1] == 0:
            direct = "up"
        elif flag == 3:
            if snake_distance[0]<=snake_distance[1]:
                direct = "down"
            else:
                direct = "up"
        return direct
    if direct=="down":
        flags = [0, 0, 0]
        snake_distance=[0,0]
        # 0 安全,不用动方向
        # 1 left危险,方向right
        # 2 right危险.方向left
        # 3 都危险,方向看蛇尾巴
        for snake in snakes:
            if (snake.x == head.x and snake.y - 1 == head.y) or head.y >=ROW-1:
                flags[0] = 1
                for snake_two in snakes:
                    if snake_two.y == head.y and snake_two.x <= head.x:
                        flags[1] = 1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two.y == head.y and snake_two.x > head.x:
                        flags[2] = 1
                        snake_distance[1] = find_list_index(snake_two, snakes)
                        break
        if sum(flags) == 0:
            pass
        if sum(flags) == 1:
            direct = random.choice(["left", "right"])
        if sum(flags) == 3:
            if snake_distance[0]<=snake_distance[1]:
                direct = "right"
            else:
                direct = "left"
        else:
            if flags[1] == 1:
                direct = "right"
            if flags[2] == 1:
                direct = "left"
        return direct
pygame.init()
pygame.mixer.init()  # 声音初始化
pygame.time.delay(1000)
#soundbgm=pygame.mixer.Sound("2.wav")
#soundbgm.play()
WIDTH = 800
HIGHT = 600
ROW = 30
COL = 40
scores = 0
all_points = []
for i in range(ROW):
    for j in range(COL):
        all_points.append(Point(j, i))
block_size = (20, 20)
BG_color = (255, 255, 255)  # 设置背景颜色,白色
Head_color = (0, 0, 0)  # 设置蛇头颜色,黑色
Food_color = (0, 125, 0)
screen_size = (WIDTH, HIGHT)
head = Point(int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
food = Point(head.x - 10, head.y)
snakes = [Point(head.x + 1, head.y), Point(head.x + 2, head.y), Point(head.x + 3, head.y),
          Point(head.x + 3, head.y + 1)]
windows = pygame.display.set_mode(screen_size)
pygame.display.set_caption("贪吃蛇尝试")
# 标题显示
font = pygame.font.SysFont("Times", 25)
str123 = "Welcome To SimpleSnake" + "\n" + "Press ESC To Quit"
title_surface = font.render(str123, True, (0, 0, 0))
scores_title = font.render("YouScore:", True, (0, 0, 0))
high_scores_title = font.render("HighScore:", True, (0, 0, 0))
# 分数显示
scores_surface = font.render(str(scores), True, (0, 0, 0))
Quit = False
clock = pygame.time.Clock()  # 生成时钟的对象
direct = None
death = False
eatten = False  # 标记是否食物被吃掉的变量
clocktrick=10
directs=["left","up","down","right"]
while not Quit:
    # print(highscore)
    pygame.Surface.fill(windows, BG_color)
    windows.blit(title_surface, (20, 23))  # 标题显示
    scores_surface = font.render(str(scores), True, (0, 0, 0))
    high_scores_surface = font.render(str(highscore), True, (0, 0, 0))
    for snake in snakes:
        pygame.draw.rect(windows, (125, 125, 125), ((snake.x * 20, snake.y * 20), block_size))
    pygame.draw.rect(windows, Food_color, ((food.x * 20, food.y * 20), block_size))
    pygame.draw.rect(windows, Head_color, ((head.x * 20, head.y * 20), block_size))  # 蛇头绘制
    windows.blit(scores_surface, (712, 26))  # 分数显示
    windows.blit(scores_title, (578, 26))
    windows.blit(high_scores_surface, (712, 52))
    windows.blit(high_scores_title, (578, 52))
    if food.x == head.x and food.y == head.y:  # 两个个方块重合,吃到食物
        eatten = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
            sys.exit()
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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
                break
            ##控制速度
            if event.key==91 :
                clocktrick=clocktrick*0.9
                break
            if event.key==93:
                clocktrick=clocktrick+10
                break
            if event.key==8:
                clocktrick=10
    direct1 = direct
    #简单追踪食物#目前处于安全情况下,追击食物
    #判断危险情况

    if head.x>food.x and direct!='right':
        direct = "left"
        for snake in snakes:
            if snake.y==head.y and (snake.x+2>=head.x and snake.x<head.x):
                direct=direct1
                break
    elif head.x<food.x and direct!='left':
        direct="right"
        for snake in snakes:
            if snake.y==head.y and (snake.x-2<=head.x and snake.x>head.x):
                direct=direct1
                break
    else:
        if head.y>food.y and direct!='down':
            direct="up"
            for snake in snakes:
                if snake.x==head.x and snake.y+2<=head.y and snake.y<head.y:
                    direct=direct1
        elif head.y<food.y and direct!='up':
            direct="down"
            for snake in snakes:
                if snake.x==head.x and snake.y-2<=head.y and snake.y>head.y:
                    direct=direct1
        else:
            pass
    direct=safe(direct,head,snakes,COL,ROW)
    direct = safe(direct, head, snakes, COL, ROW)
    if direct=="left":
        for snake in snakes:
            if snake.x==head.x-1 and snake.y==head.y-1:
                for snake_two in snakes:
                    if snake_two.x==head.x-1 and snake_two.y==head.y+1:
                        for snake_three in snakes:
                            if snake_three.y==head.y and snake_three.x<head.y:
                                direct=direct1
                                break


    if direct == "right":
        for snake in snakes:
            if snake.x == head.x + 1 and snake.y == head.y - 1:
                for snake_two in snakes:
                    if snake_two.x == head.x + 1 and snake_two.y == head.y + 1:
                        for snake_three in snakes:
                            if snake_three.y == head.y and snake_three.x > head.y:
                                direct = direct1
                                break
    if direct=="up":
        for snake in snakes:
            if snake.y==head.y-1 and snake.x==head.x-1:
                for snake_two in snakes:
                    if snake_two.y==head.y-1 and snake_two.x==head.x+1:
                        for snake_three in snakes:
                            if snake_three.x == head.x and snake_three.y < head.y:
                                direct = direct1
                                break
    if direct=="down":
        for snake in snakes:
            if snake.y==head.y+1 and snake.x==head.x-1:
                for snake_two in snakes:
                    if snake_two.y==head.y+1 and snake_two.x==head.x+1:
                        for snake_three in snakes:
                            if snake_three.x == head.x and snake_three.y > head.y:
                                direct = direct1
                                break
    direct = safe(direct, head, snakes, COL, ROW)
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
    all_points_tp = all_points[:]  # 创建临时列表,用于生成食物
    if eatten:
        while True:
            ovet = True
            food = random.choice(all_points_tp)
            if scores <= 200:  # 分数不是过高时,食物不生成在角落
                if food.x >= 2 and food.x <= COL - 2 and food.y >= 2 and food.y <= ROW - 2:
                    pass
                else:
                    ovet = False
            for snake in snakes + [head]:
                if judge_point(food, snake):
                    all_points_tp.remove(food)
                    ovet = False
                    break
            if ovet:
                break
        eatten = False
        scores = scores + 1

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
        print("aswl",end="\t")
        print(direct,direct1)
        with open("robot_list","a")as f:
            f.write(str(scores))
            f.write('\n')
            f.close()
        if scores > highscore:
            highscore = scores
            with open("high_score", "a")as f:
                f.write(str(scores))
                f.write('\n')
                f.close()
        scores = 0
        head = Point(int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
        food = Point(head.x - 10, head.y)
        snakes = [Point(head.x + 1, head.y), Point(head.x + 2, head.y), Point(head.x + 3, head.y),
                  Point(head.x + 3, head.y + 1)]
        death = False
        direct = None
        # time.sleep(3)
