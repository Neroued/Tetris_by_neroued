import pygame,os
from functions import spawn
from classBlock import Block

pygame.init()

screen = pygame.display.set_mode((530, 1060))

# 导入图片素材,存放在一个字典中
path = os.getcwd() + os.sep + "pic"
res = {}
for p in os.listdir(path):
    res[p.split(".")[0]] = pygame.image.load(path + os.sep + p)

b = Block()

t = spawn()

x , y = t.center
for p in t.coord:
    print(p)
    cx ,cy = p
    screen.blit(res[t.color], ((x+cx-2)*53,(y+cy-2)*53))


while True:

    pygame.display.flip()