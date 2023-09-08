from classBackground import Background
from functions import type_dict,types,colors
from random import choice

background = Background()

# 定义Block类

class Block(object):

    def __init__(self):  # 初始化各项参数
        self.color = ''
        self.center = []
        self.coord = []
        self.type = ''
        self.rot = 0
        self.be_static = False

    def collide(self):  #判断有无与现有方块发生碰撞，若有输出True
        is_collide = False
        x, y = self.center
        for p in self.coord:
            cx, cy = p
            if background.content[y + cy][x + cx] != 0:
                is_collide = True
                break
        return is_collide
    
    def x_outside(self):
        x_is_outside = False
        x = self.center[0]
        for p in self.coord:
            cx = p[0]
            if x + cx >11 or x + cx < 2:
                x_is_outside = True
                break
        return x_is_outside
    
    def y_outside(self):
        y_is_outside = False
        y = self.center[1]
        for p in self.coord:
            cy = p[1]
            if y + cy >21 or y + cy <2 :
                y_is_outside = True
                break
        return y_is_outside
    
    def rotate(self):   #旋转方块
        if self.type in ['I','S','Z']:
            if self.rot != 0:
                rot_ = int(self.rot / abs(self.rot) * (self.rot % 2))
                self.coord = type_dict[self.type][rot_]
        elif self.type in ['J','L','T']:
            if self.rot != 0:
                rot_ = int(self.rot / abs(self.rot) * (self.rot % 4))
                self.coord = type_dict[self.type][rot_]
        else:
            return
        
    def rotate_with_check(self):    #检查旋转后是否发生碰撞或超出边界，若有则取消旋转操作
        self.rotate()
        if self.collide() or self.x_outside():
            self.rot -= 1
            self.rotate_with_check()
        return
    
    def move(self,step):    
        self.center = [self.center[0]+step[0],self.center[1]+step[1]]
        return 
    
    def move_with_check(self,step):  #同理，检查移动后是否碰撞或者出界，若有则取消移动
        self.move(step)
        if self.collide() or self.x_outside():
            self.move((-step[0],-step[1]))
        return
    
    def static_check(self):     #检测方块是否不能再移动，需要变为静态
        self.move((0,1))
        if self.collide() or self.y_outside():
            self.move((0,-1))
            self.be_static = True
        else:
            self.move((0,-1))

        
    def static(self):       #将方块变为静态
        x , y =self.center
        for p in self.coord:
            cx ,cy = p
            background.content[cy + y][cx + x] = self.color
        self.be_static = False

    def spawn(self):
        self.color = choice(colors)
        self.center = [7,3]
        self.type = choice(types)
        self.coord = type_dict[self.type][0]
        return 