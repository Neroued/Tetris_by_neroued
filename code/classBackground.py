#定义Background类，存储背景的信息

#初始生成一个24x14的矩阵


init_back = [[0 for i in range(14)] for j in range(24)]

class Background(object):
    def __init__(self):
        self.content = init_back[:]
        self.faded = []
    
    def move_on(self):
        for rang in self.faded:
            self.content.pop(rang)
            self.content.insert(0,[0 for i in range(14)])
            self.faded.pop()

    def fade_check(self):
        for index,rang in enumerate(self.content):
            full = True
            for item in rang[2:12]:
                if item == 0:
                    full = False
            if full:
                self.faded.append(index)