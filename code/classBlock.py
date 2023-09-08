from classBackground import Background
from functions import type_dict
background = Background()

# 定义Block类

class Block(object):

    def __init__(self):  # 初始化各项参数
        self.color = ''
        self.center = []
        self.coord = []
        self.type = ''

    def collide(self):  #判断有无与现有方块发生碰撞，若有输出True
        is_collide = False
        x, y = self.center
        for p in self.coord:
            cx, cy = p
            if background.content[y + cy][x + cx] != 0:
                is_collide = True
                break
        return is_collide
    
    def outside(self):
        is_outside = False
        x = self.center[0]
        for p in self.coord:
            cx = p[0]
            if x + cx >10 or x + cx < 2:
                is_outside = True
                break
        return is_outside
    
    def rotate(self,rot_num):   #旋转方块
        if self.type in ['I','S','Z']:
            rot = rot_num % 2
            self.coord = type_dict[self.type][rot]
        elif self.type in ['J','L','T']:
            rot = rot_num % 4
            self.coord = type_dict[self.type][rot]
        else:
            return
        
    def rotate_with_check(self,rot_num):    #检查旋转后是否发生碰撞或超出边界，若有则取消旋转操作
        self.rotate(rot_num)
        if self.collide() or self.outside():
            self.rotate(rot_num-1)
        return
    
    def move(self,step):    
        self.center = [self.center[0]+step[0],self.center[1]+step[1]]
        return 
    
    def move_with_check(self,step):  #同理，检查移动后是否碰撞或者出界，若有则取消移动
        self.move(step)
        if self.collide() or self.outside():
            self.move((-step[0],-step[1]))
        return
    
    def static_check(self):     #检测方块是否不能再移动，需要变为静态
        tmp = self.center.copy()
        self.move((0,1))
        if self.collide():
            self.center = tmp.copy()
            return False
        else:
            return True
        
    def static(self):       #将方块变为静态
        x , y =self.center
        for p in self.coord:
            cx ,cy = p
            background.content[cy + y][cx + x] = self.color