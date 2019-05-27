import pygame
import sys
import random
import time
import os
global COL,ROW
def find_list_index(ste,list1):
    for i in range(len(list1)):
        if ste==list1[i]:
            return i
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
def create_dict(all_points,snakes):
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
                if j not in snakes[:]:
                    prelist.append(j)
        if points not in snakes:
            point_dict[points]=prelist
    return point_dict
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
            if (snake[1]==head[1] and snake[0]+1==head[0]) or head[0]==0:
                flags[0]=1
                for snake_two in snakes:
                    if (snake_two[0]==head[0] and snake_two[1]<=head[1]):
                        flags[1]=1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two[0]==head[0] and snake_two[1]>head[1]:
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
            if (snake[0]==head[0] and snake[1]+1==head[1]) or head[1]==0:
                flags[0]=1
                for snake_two in snakes:
                    if snake_two[1]==head[1] and snake_two[0]<=head[0]:
                        flags[1]=1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two[1]==head[1] and snake_two[0]>head[0]:
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
            if (snake[1] == head[1] and snake[0] - 1 == head[0]) or head[0] >= COL-1:
                flags[0] = 1
                for snake_two in snakes:
                    if (snake_two[0]== head[0] and snake_two[1] <= head[1]):
                        flags[1] = 1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two[0]== head[0] and snake_two[1] > head[1]:
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
            if (snake[0] == head[0] and snake[1] - 1 == head[1]) or head[1] >=ROW-1:
                flags[0] = 1
                for snake_two in snakes:
                    if snake_two[1] == head[1] and snake_two[0]<= head[0]:
                        flags[1] = 1
                        snake_distance[0]=find_list_index(snake_two,snakes)
                        break
                for snake_two in snakes:
                    if snake_two[1] == head[1] and snake_two[0]> head[0]:
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
Quit=False
point_dict=create_dict(all_points,snakes)
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
    # else:
    #     ppp=[]
    #     if head[0]-1>0 and (head[0]-1,head[1]) not in snakes:
    #         ppp.append((head[0]-1,head[1]))
    #     if head[0]+1<COL-1 and (head[0]+1,head[1]) not in snakes:
    #         ppp.append((head[0]+1,head[1]))
    #     if head[1]-1>0 and (head[0],head[1]-1) not in snakes:
    #         ppp.append((head[0],head[1]-1))
    #     if head[1]+1<ROW-1 and (head[0],head[1]+1) not in snakes:
    #         ppp.append((head[0],head[1]+1))
    #     if ppp:
    #         old_tail=snakes.pop()
    #         snakes.insert(0,head)
    #         head=ppp[0]
    #     else:
    #         if head[0]-1>=0 and (head[0]-1,head[1]) not in snakes:
    #             ppp.append((head[0]-1,head[1]))
    #         if head[0]+1<=COL-1 and (head[0]+1,head[1]) not in snakes:
    #             ppp.append((head[0]+1,head[1]))
    #         if head[1]-1>=0 and (head[0],head[1]-1) not in snakes:
    #             ppp.append((head[0],head[1]-1))
    #         if head[1]+1<=ROW-1 and (head[0],head[1]+1) not in snakes:
    #             ppp.append((head[0],head[1]+1))
    #         old_tail=snakes.pop()
    #         snakes.insert(0,head)
    #         head=ppp[0]
    else:
        if head[0]>food[0] and direct!='right':
            direct = "left"
        elif head[0]<food[0] and direct!='left':
            direct="right"
        else:
            if head[1]>food[1] and direct!='down':
                direct="up"
            elif head[1]<food[1] and direct!='up':
                direct="down"
            else:
                pass
        direct=safe(direct,head,snakes,COL,ROW)
        if direct == "up" :
            old_tail = snakes.pop()
            snakes.insert(0,head)
            head=(head[0]-1,head[1])
        if direct == "down":
            old_tail = snakes.pop()
            snakes.insert(0, head)
            head=(head[0],head[1]+1)
        if direct == "left" :
            old_tail = snakes.pop()
            snakes.insert(0, head)
            head=(head[0]-1,head[1])
        if direct == "right" :
            old_tail = snakes.pop()
            snakes.insert(0, head)
            head=(head[0]+1,head[1])

    count=0
    while tail_track:
        point_dict=create_dict(all_points,snakes[:-1])
        the_search_way=Bfs(point_dict,head,food)
        count=count+1
        #探路小蛇
        head_virtual=head
        snakes_virtual=snakes[:]
        if the_search_way:
            for way in the_search_way[::-1]:
                snakes_virtual.pop()
                snakes_virtual.insert(0,head_virtual)
                head_virtual=way
            #生成virtualpointdict
        point_dict_virtual = create_dict(all_points,snakes_virtual[:-1])        #每次被吃到,重新建立关系字典
        if Bfs(point_dict_virtual,food,snakes_virtual[-1]):
            tail_track=False
            print("迷路的小蛇找到安全的路啦")
            if the_search_way:
                the_way=the_search_way[:]
            else:
                pass

        else:
            pass
        if count >2:
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
        snakes.append(old_tail)
        point_dict=create_dict(all_points,snakes[:-1])        #每次被吃到,重新建立关系字典
        the_way=Bfs(point_dict,head,food)
        head_virtual=head
        snakes_virtual=snakes[:]
        if the_way:
            for way in the_way[::-1]:
                snakes_virtual.pop()
                snakes_virtual.insert(0,head_virtual)
                head_virtual=way
            head_virtual=food
            point_dict_virtual=create_dict(all_points,snakes_virtual[:-1])
            the_way_to_tail=Bfs(point_dict_virtual,head_virtual,snakes_virtual[-1])
            if the_way_to_tail:
                pass
            else:
                tail_track=True
                the_way=None
                # if len(snakes)>14:
                #     the_way=Bfs(point_dict,head,snakes[-1])
        # the_way_to_tail=Bfs()


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
