import pygame,sys
from functions import res
from classBlock import Block,background

pygame.init()
screen = pygame.display.set_mode((530, 1060))

is_falling = False

falling_block=Block()

pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 创建一个计时器，每隔1000毫秒创建一个USEREVENT+1

while True:
    #检测是否有正在下落的方块
    if not is_falling:
        falling_block.spawn()
        if falling_block.collide():     #若生成在其他方块上，则直接退出游戏
            pygame.quit()
            sys.exit()
        is_falling = True
    
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
            elif event.key == pygame.K_SPACE:
                falling_block.direct_to_bottom()
            falling_block.rotate_with_check()    #根据rot旋转
        
        elif event.type == pygame.USEREVENT + 1:    #间隔时间自动下落
            falling_block.move_with_check((0,1))
            

    #检测方块是否需要变为静态，并进行转换
    falling_block.static_check()

    if falling_block.be_static == True:
        
        falling_block.static()
        is_falling = False

        #检测背景是否需要消除某行,并消除
        background.fade_check()
        background.move_on()
        
    #重置底色
    screen.fill('black')


    #渲染背景
    for j,rang1 in enumerate(background.content):

        for i,item in enumerate(rang1):
            if item != 0:
                screen.blit(res[item],((i-2)*53,(j-2)*53))
    
    #渲染下落方块
    if is_falling:
        x , y = falling_block.center
        for p in falling_block.coord:
            cx , cy = p
            screen.blit(res[falling_block.color],(((x+cx-2)*53),(y+cy-2)*53))

    #显示图像
    pygame.display.flip()