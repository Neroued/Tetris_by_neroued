### 游戏主要思路

*为了避免在移动或者旋转过程中产生下标越界，将背景矩阵扩大至14x24。*  
*先进行旋转或者移动操作，再判断是否超出范围。若超出范围，则将中心点相应的移动至合适位置。*

- display()方法: 将当前下落的方块对象与固定在底部的方块用pygame模块显示出来
- spawn()方法：生成一个颜色、类型随机，中心点坐标为初始值的方块对象
- 每1000ms创建一个自定义事件pygame.USEREVENT + 1,实现固定时间自动下落(未来可改进为随着游戏事件增加加速)
- rot变量表示总共进行的旋转次数，+1表示顺时针，-1表示逆时针，通过mod 2 或mod 4 表示不同状态  

* 创建一个Block对象
  - __init__()中：
    - color   保存颜色
    - center  保存中心点位置
    - coord   保存全部点的坐标，保存在list中，使用相对坐标
  - spawn() --创建一个新下落方块对象
    - 通过random随机选择一个方块类型和颜色
    - 初始化方块的中心点坐标
  - collide() --检测是否与现有方块碰撞
    - 遍历方块各个点坐标，判断是否与背景中有重合，若有返回True
 
  - move(tuple) --移动方块的中心点
  - rotate(rot) --旋转方块，通过mod运算判断当前状态，并修改coord内容。
  - move_static() --检测移动后是否需要变为静态(到达底部或者触碰到最上面的静态方块)
  - rotate_with_check() --检查旋转后坐标是否存在越界或碰撞，若有则取消旋转。
  - move_with_check() --检查移动后是否碰撞或出界，若有则取消移动
  - static_check() -- 检测是否需要将方块变为静态
  - static() --将方块变为静态

* 创建一个Background对象，保存背景的内容与属性
  - __init__()中：
    - content     保存内容
    - faded       保存需要消失的行号list
  - move_on(list)     将需要消失的行删除，并将背景整体下移
  - fade_check()  检查是否有行需要消失，若有self.faded.append(行号)

************

### 整体逻辑

- 初始化
- 游戏主循环  
  1. 检测is_falling是否存在下落的方块对象，若否则使用spawn()生成falling_block，并将is_falling置为False
  2. 判断新生成的方块是否与现有固定方块碰撞，若碰撞立刻结束游戏  
      调用Block.collide()方法
  3. 监测键盘事件
     1.  quit()退出游戏
     2.  检测定时事件
     3.  方向键盘左右控制左右移动，ad顺逆时针旋转，按下键向下移动 --move()与 ratate()
     4.  旋转后需要判断是否越界 --rotate_coor_check()
          再使用move()
  4.  若移动到底部，便将下落的方块变为静态，is_falling置为False

TODO list:
- 修复新生成方块会自己旋转一次的bug **Done!!!**
- 显示下一次生成的方块  **Done!!**
- 修改界面
- 添加计分板  **Done!!**
- 根据分数加快游戏速度 **Done!!**
- 添加背景方格  **Done!!**
- 添加消失动画
- 游戏结束后刷新重来  **Done!!**