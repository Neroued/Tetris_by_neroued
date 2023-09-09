import pygame,sys
from functions import res
from classBlock import Block,background
from classNotes import Notes
import copy

pygame.init()
screen = pygame.display.set_mode((615, 610))
pygame.display.set_caption("俄罗斯方块")

#生成字体对象
font = pygame.font.Font('ttf\SmileySans-Oblique-2.ttf',25)

next_block = Block()
notes = Notes()

#游戏初始化
def game_init():        
    global is_falling,timer_speed,fail,falling_block,printed
    fail = False
    is_falling = False
    next_block.spawn()
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 创建一个计时器，每隔1000毫秒创建一个USEREVENT+1
    timer_speed = 1     #记录目前的游戏速度
    background.restart()   #刷新游戏区域
    falling_block = Block()
    printed = False
    notes.current_note = 0

game_init()

#将游戏主循环变为函数
def main():     
    #函数中使用全局变量需要先声明
    global is_falling,timer_speed,fail,falling_block
    #检测是否有正在下落的方块
    if not is_falling:
        falling_block = copy.deepcopy(next_block)
        next_block.spawn()
        if falling_block.collide():     #若生成在其他方块上，则游戏失败
            fail = True
        is_falling = True
    
    #根据当前分数设定游戏速度
    if notes.current_note > 5 and notes.current_note <= 10 and timer_speed != 2:
        timer_speed = 2
        pygame.time.set_timer(pygame.USEREVENT + 1, 800)
    elif notes.current_note > 10 and notes.current_note <= 20 and timer_speed != 3:
        timer_speed = 3
        pygame.time.set_timer(pygame.USEREVENT + 1, 600)

    #事件监测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:     #ad控制左右旋转
                falling_block.rot += 1
            elif event.key == pygame.K_d:
                falling_block.rot -= 1
            elif event.key == pygame.K_LEFT:    #左右键控制左右移动
                falling_block.move_with_check((-1,0))
            elif event.key == pygame.K_RIGHT:
                falling_block.move_with_check((1,0))
            elif event.key == pygame.K_DOWN:
                falling_block.move_with_check((0,1))
            elif event.key == pygame.K_SPACE:   #空格直达底部
                falling_block.direct_to_bottom()
            falling_block.rotate_with_check()    #根据rot旋转
        
        elif event.type == pygame.USEREVENT + 1:    #间隔时间自动下落
            falling_block.move_with_check((0,1))
            
    #检测方块是否需要变为静态，并进行转换
    falling_block.static_check()

    if falling_block.be_static == True:
        
        falling_block.static()
        is_falling = False

        #检测背景是否需要消除某行
        background.fade_check()

        #根据需要消失的行数加分
        notes.get_note(background.faded)
        notes.change_best()

        #清除需要消失的行
        background.move_on()

    #渲染底色 
    screen.fill('black')

    #添加5像素宽度的边框
    screen.fill((255,235,215),rect=(5,5,300,600))
    screen.fill((255,235,215),rect=(310,5,300,600))

    #游戏区域渲染网格
    #竖线
    for i in range(9):
        pygame.draw.line(screen,(184, 171, 162),[35+30*i,5],[35+30*i,605])
    #横线
    for i in range(19):
        pygame.draw.line(screen,(184, 171, 162),[5,35+30*i],[305,35+30*i])

    #显示分数
    note = font.render("当前分数为：{}".format(notes.current_note),True,(0,0,0))
    screen.blit(note,(394.0, 175))  #这个位置是通过函数算出来的

    #显示最高分数
    max_notes = font.render("最高分数：{}".format(notes.best_note),True,(0,0,0))
    screen.blit(max_notes,(404.0, 235))

    #显示阶段
    stage = font.render("当前阶段：{}".format(timer_speed),True,(0,0,0))
    screen.blit(stage,(406.5, 205))

    #渲染游戏静态方块
    for j,rang1 in enumerate(background.content):
        for i,item in enumerate(rang1):
            if item != 0:
                screen.blit(res[item],((i-2)*30+5,(j-2)*30+5))
    
    #渲染下落方块
    if is_falling: 
        x , y = falling_block.center
        for p in falling_block.coord:
            cx , cy = p
            screen.blit(res[falling_block.color],(((x+cx-2)*30)+5,(y+cy-2)*30+5))

    #在右侧渲染下一个生成的方块
    x , y = next_block.center
    for p in next_block.coord:
        cx , cy = p
        screen.blit(res[next_block.color],(((x+cx-3)*30)+310,(y+cy-2)*30+5))

    #显示图像
    pygame.display.flip() 

while True:
    if not fail:
        main()
    else:
        #在右侧显示提示
        if printed == False:
            game_failed = font.render("游戏结束！",True,(0,0,0))
            restart = font.render("按任意键重新开始",True,(0,0,0))

            screen.blit(game_failed,(410.0, 255))
            screen.blit(restart,(380.0, 285))

            pygame.display.flip()

            printed = True

        #更新最高分数
        notes.change_best()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game_init()
                