from math import factorial

#定义一个分数类，实现相关分数的功能

class Notes(object):
    def __init__(self):
        self.current_note = 0
        self.best_note = 0

    def get_note(self,a_list):
        if lenth := len(a_list) != 0:
            self.current_note += factorial(lenth)
        
    def change_best(self):
        self.best_note = max(self.best_note,self.current_note)
    
