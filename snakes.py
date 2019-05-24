import pygame
import sys
import random
import time
import os
global COL,ROW
class Point():
    def __init__(self, x=0, y=0):
        self.x = x  # 行
        self.y = y  # 列
def judge_point(a, b):  # 判断两个point类是否值相等的函数
    if a.x == b.x and a.y == b.y:
        return True
    else:
        return False
def find_list_index(ste,list1):
    for i in range(len(list1)):
        if ste==list1[i]:
            return i
def snake_move(head,way):
    if  head[0]>way[0] and head[1]==way[1]:
        return "left"
    if  head[0]<way[0] and head[1]==way[1]:
        return "right"
    if  head[0]==way[0] and head[1]>way[1]:
        return "up"
    if  head[0]==way[0] and head[1]<way[1]:
        return "right"
def Bfs(point_dict,head,food):
    queue=[]
    if type(head)==list:
        head=head[0]
    pre_dict={}
    queue.append(head)
    seen=set()
    seen.add(head)
    pre_dict[head]=None
    while(len(queue)>0):
        vertx=queue.pop(0)
        try:
            if point_dict[vertx]:
                nodes=point_dict[vertx]
            for node in nodes:
                if node not in seen:
                    queue.append(node)
                    seen.add(node)
                    pre_dict[node]=vertx
        except:
            print("出现一些小问题")
    node=food
    the_way=[]
    if node not in seen:
        print("没有安全的路径可以到达,开始漫游")
        return False
    else:
        while node !=None:
            the_way.append(node)
            node=pre_dict[node]
        return the_way
def create_dict(all_points,head,snakes):
    point_dict={}
    for points in all_points:
        left_point=(points[0]-1,points[1])
        right_point=(points[0]+1,points[1])
        up_point=(points[0],points[1]-1)
        down_point=(points[0],points[1]+1)
        prelist=[]
        prelist_0=[left_point,right_point,up_point,down_point]
        random.shuffle(prelist_0)    
        for j in prelist_0:
            if j in all_points:
                if j not in snakes:
                    prelist.append(j)
        if points not in snakes:
            point_dict[points]=prelist
    return point_dict
WIDTH = 800
HIGHT = 600
block_size = (30, 30)
ROW = int(HIGHT/block_size[0])
COL = int(WIDTH/block_size[1])
pygame.init()
all_points=[]
for i in range(ROW):
    for j in range(COL):
        all_points.append((j, i))
all_points_virtual=all_points[:]
all_points=tuple(all_points)
Bg_color = (255, 255, 255)  # 设置背景颜色,白色
Head_color = (0, 0, 0)  # 设置蛇头颜色,黑色
Snake_color=(125,125,125)
Line_color=(215,0,95)
Food_color = (0, 125, 0)
Way_color=(47,134,210)
screen_size = (WIDTH, HIGHT)
head = (int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
food = (head[0] - int(COL/4), head[1])
snakes = [(head[0] + 1, head[1]), (head[0] + 2, head[1]), (head[0] + 3, head[1]),
          (head[0] + 3, head[1] + 1)]
windows = pygame.display.set_mode(screen_size)
pygame.display.set_caption("贪吃蛇尝试")
# 标题显示
clock = pygame.time.Clock()  # 生成时钟的对象
direct = None
scores=0
death = False
eatten = False  # 标记是否食物被吃掉的变量
clocktrick=5
directs=["left","up","down","right"]
Quit=False
point_dict=create_dict(all_points,head,snakes)
the_way=Bfs(point_dict,head,food)
the_first_way=the_way[:]
tail_track=False
while not Quit:
    pygame.Surface.fill(windows, Bg_color)
    for j in range(ROW+1):
        pygame.draw.line(windows,Line_color,(0,j*block_size[0]),(COL*block_size[0],j*block_size[0]))
    for j in range(COL+1):
        pygame.draw.line(windows,Line_color,(j*block_size[0],0),(j*block_size[0],COL*block_size[0]))
    for snake in snakes:
        pygame.draw.rect(windows,Snake_color , ((snake[0] * block_size[0], snake[1] * block_size[0]), block_size))
    for snake in snakes:
        pygame.draw.rect(windows,(124,49,208),((snake[0]*block_size[0]+block_size[0]/4,snake[1]*block_size[0]+block_size[0]/4),(block_size[0]/2,block_size[1]/2)))
    pygame.draw.rect(windows, Food_color, ((food[0] * block_size[0], food[1] * block_size[0]), block_size))
    pygame.draw.rect(windows, Head_color, ((head[0] * block_size[0], head[1] * block_size[0]), block_size))  # 蛇头绘制
    if the_way:
        for way in the_way:
                if type(way)!=bool:
                    pygame.draw.rect(windows,Way_color,((way[0]*block_size[0]+block_size[0]/4,way[1]*block_size[0]+block_size[0]/4),(block_size[0]/2,block_size[1]/2)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
            sys.exit()
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
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
    """ if direct == "up" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, (head[0], head[1]))
        head=(head[0] , head[1]-1)
    if direct == "down":
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, (head[0], head[1]))
        head=(head[0] , head[1]+1)
    if direct == "left" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, (head[0], head[1]))
        head = (head[0] - 1,head[1])
    if direct == "right" :
        if eatten:
            pass
        else:
            snakes.pop()
        snakes.insert(0, (head[0], head[1]))
        head = (head[0] + 1,head[1]) """
    #根据位置定义蛇的运动方向
    if the_way:
        old_tail=snakes.pop()
        snakes.insert(0,head)
        head=the_way.pop()
    else:
        ppp=[]
        if head[0]-1>0 and (head[0]-1,head[1]) not in snakes:
            ppp.append((head[0]-1,head[1]))
        if head[0]+1<COL-1 and (head[0]+1,head[1]) not in snakes:
            ppp.append((head[0]+1,head[1]))
        if head[1]-1>0 and (head[0],head[1]-1) not in snakes:
            ppp.append((head[0],head[1]-1))
        if head[1]+1<ROW-1 and (head[0],head[1]+1) not in snakes:
            ppp.append((head[0],head[0]+1))
        if the_way:
            the_way=[ppp.pop(0)]
        old_tail=snakes.pop()
        snakes.insert(0,head)
        if the_way:
            head=the_way.pop()
        else:
            if head[0]-1>=0 and (head[0]-1,head[1]) not in snakes:
                ppp.append((head[0]-1,head[1]))
            if head[0]+1<COL and (head[0]+1,head[1]) not in snakes:
                ppp.append((head[0]+1,head[1]))
            if head[1]-1>=0 and (head[0],head[1]-1) not in snakes:
                ppp.append((head[0],head[1]-1))
            if head[1]+1<ROW and (head[0],head[1]+1) not in snakes:
                ppp.append((head[0],head[0]+1))
            the_way=[ppp.pop(0)]
            head=the_way.pop()


    count=0
    while tail_track:
        point_dict=create_dict(all_points,head,snakes)
        the_search_way=Bfs(point_dict,head,food)
        count=count+1
        direct=None
        #探路小蛇
        head_virtual=head
        snakes_virtual=snakes[:]
        if the_search_way:
            for way in the_search_way:
                snakes_virtual.pop()
                snakes_virtual.insert(0,head_virtual)
                head_virtual=way
            #生成virtualpointdict
        point_dict_virtual = create_dict(all_points_virtual,head_virtual,snakes_virtual)        #每次被吃到,重新建立关系字典
        if Bfs(point_dict_virtual,head_virtual,snakes_virtual[-1]):
            tail_track=False
            print("迷路的小蛇找到安全的路啦")
            if the_search_way:
                the_way=the_search_way[:]
            else:
                pass

        else:
            the_way=Bfs(point_dict,head,snakes[-1])
        if count >10:
            break
    if food[0] == head[0] and food[1] == head[1]:  # 两个个方块重合,吃到食物
        eatten = True
        scores+=1
        all_points_tp =all_points[:]  # 创建临时列表,用于生成食物
        all_points_tp=list(all_points_tp)
        while True:
            ovet=True
            food=random.choice(all_points_tp)
            for snake in snakes + [head]:
                if food==snake:
                    all_points_tp.remove(food)
                    ovet = False
                    print("食物生成重复")
                    break
            if ovet:
                break
        eatten = False
        point_dict=create_dict(all_points,head,snakes)        #每次被吃到,重新建立关系字典
        the_way=Bfs(point_dict,head,food)
        direct=None
        snakes.append(old_tail)
        #探路小蛇
        head_virtual=head
        snakes_virtual=snakes[:]
        if the_way:
            for way in the_way[::-1]:
                snakes_virtual.pop()
                snakes_virtual.insert(0,head_virtual)
                head_virtual=way
        #生成virtualpointdict
        point_dict_virtual={}        #每次被吃到,重新建立关系字典
        for points in all_points:
            left_point=(points[0]-1,points[1])
            right_point=(points[0]+1,points[1])
            up_point=(points[0],points[1]-1)
            down_point=(points[0],points[1]+1)
            prelist=[]
            prelist_0=[left_point,right_point,up_point,down_point]
            for j in prelist_0:
                if j in all_points:
                    if j not in snakes_virtual[:-1]:
                        prelist.append(j)
            point_dict_virtual[points]=prelist
        if Bfs(point_dict_virtual,head_virtual,snakes_virtual[-1]):
            pass #还可以找到尾巴
            tail_track=False
        else:
            tail_track=True
            the_way=Bfs(point_dict,head,snakes[-1])


    # 判断是否被吃掉
    # 判断是否死亡
    # for snake in snakes:
    #     pygame.draw.rect(windows,Snake_color , ((snake[0] * block_size[0], snake[1] * block_size[0]), block_size))
    # for snake in snakes:
    #     pygame.draw.rect(windows,(124,49,208),((snake[0]*block_size[0]+block_size[0]/4,snake[1]*block_size[0]+block_size[0]/4),(block_size[0]/2,block_size[1]/2)))
    # pygame.draw.rect(windows, Food_color, ((food[0] * block_size[0], food[1] * block_size[0]), block_size))
    # pygame.draw.rect(windows, Head_color, ((head[0] * block_size[0], head[1] * block_size[0]), block_size))  # 蛇头绘制
    clock.tick(clocktrick)  # 控制帧率
    pygame.display.flip()  # 渲染,释放控制权
    """ if death:
        head = (int(COL / 2), int(ROW / 2))  # 蛇头初始位置,正中间
        food = (head[0]-int(COL/4), head[1])
        snakes = [(head[0] + 1, head[1]), (head[0] + 2, head[1]), (head[0] + 3, head[1]),
                  (head[0] + 3, head[1] + 1)]      
        death = False
        direct = None
        print(scores)
        scores=0
        the_way=the_first_way[:]
        # time.sleep(3) """
