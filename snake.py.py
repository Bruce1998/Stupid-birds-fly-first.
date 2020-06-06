#coding=UTF-8
from Tkinter import *    #tkinter库的使用
from random import randint  #随机数的生成
import tkMessageBox       #tkMessageBox库的使用

class Grid(object):
    def __init__(self, root, height=10, width=10, grid_width=20, bg='white'):
        self.height = height
        self.width = width
        self.grid_width = grid_width
        self.bg = bg
        self.canvas = Canvas(root, width=self.width*self.grid_width, height=self.height*self.grid_width, bg=self.bg)
        self.canvas.pack(side=LEFT)
    def draw(self, pos, color ):
        x = pos[0] * self.grid_width 
        y = pos[1] * self.grid_width # 网格颜色一致化
        self.canvas.create_rectangle(x, y, x + self.grid_width, y + self.grid_width, fill=color, outline=self.bg)#???
class Food(object):
    def __init__(self, grid, color = "pink"):
        self.grid = grid
        self.color = color
        self.set_pos()
    def set_pos(self):
        x = randint(0, self.grid.width - 1 )
        y = randint(0, self.grid.height - 1)
        self.pos = (x, y)
    def display(self):
        self.grid.draw(self.pos, self.color)    
class Snake(object):
    def __init__(self, grid, color = 'red'):
        self.grid = grid
        self.color = color
        self.body = [(2, 5), (2, 6), (2, 7)]
        self.direction = "Right"
        for i in self.body:
            self.grid.draw(i, self.color)
    #游戏重新开始时初始化贪吃蛇的位置
    def initial(self):
        while len(self.body) > 0:
            pop = self.body.pop()
            self.grid.draw(pop, self.grid.bg)
        self.body = [(8, 11), (8, 12), (8, 13)]
        self.color = "blue"
        self.direction = "Up"
        for i in self.body:
            self.grid.draw(i, self.color)
    #蛇向一个指定点移动
    def move(self, new):
        self.body.insert(0, new)
        pop = self.body.pop()
        self.grid.draw(pop, self.grid.bg)
        self.grid.draw(new, self.color)
    #蛇向一个指定点移动，并增加长度
    def add(self ,new):
        self.body.insert(0, new)
        self.grid.draw(new, self.color)
class SnakeGame(Frame):
    def __init__(self, master = None):# Fixed usage
        Frame.__init__(self, master)  #Fixed usage
        self.grid = Grid(master)
        self.snake = Snake(self.grid)
        self.food = Food(self.grid)
        self.gameover = False
        self.score = 0
        self.status = ['run', 'stop']
        self.speed = 250
        self.grid.canvas.bind_all("<KeyRelease>", self.key_release)# 调用电脑键盘
        self.display_food()       
        #界面左侧显示分数
        Tk()
        self.m = StringVar()
        self.ft1 = ('Fixdsys', 40, "bold")
        self.m1 = Message(root, textvariable=self.m, aspect=5000, font=self.ft1, bg="#696969")
        self.m1.pack(side=LEFT, fill=Y)
        self.m.set("Score:"+str(self.score))
    #这个方法用于游戏重新开始时初始化游戏（引用自CSDN博客）
    def initial(self):
        self.gameover = False
        self.score = 0
        self.m.set("Score:"+str(self.score))
        self.snake.initial()    
    def display_food(self):
        self.food.color = "pink"
        self.food.type = 1 #???       
        while (self.food.pos in self.snake.body):
            self.food.set_pos()
        self.food.display()
    def key_release(self, event):
        key = event.keysym
        key_dict = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}  #要boom了
        #蛇不可以像自己的反方向走
        if key_dict.has_key(key) and not key == key_dict[self.snake.direction]:
            self.snake.direction = key
            self.move()
        elif key == 'p':
            self.status.reverse() #???
    def run(self):
        #首先判断游戏是否暂停
        if not self.status[0] == 'stop':
            #判断游戏是否结束
            if self.gameover == True:
                message = tkMessageBox.showinfo("Game Over", "your score: %d" % self.score)
                if message == 'ok':
                    self.initial()
            
            else:
                self.move()
        self.after(self.speed, self.run)
    def move(self, color="#EE82EE"):
        # 计算蛇下一次移动的点
        head = self.snake.body[0]
        if self.snake.direction == 'Up':
            if head[1] - 1 < 0:
                new = (head[0], 16)
            else:
                new = (head[0], head[1] - 1)
        elif self.snake.direction == 'Down':
            new = (head[0], (head[1] + 1) % 16)
        elif self.snake.direction == 'Left':
            if head[0] - 1 < 0:
                new = (24, head[1])
            else:
                new = (head[0] - 1, head[1])
        else:
            new = ((head[0] + 1) % 24, head[1])
            #撞到自己，设置游戏结束的标志位，等待下一循环
        if new in self.snake.body:
            self.gameover=True
        #吃到食物
        elif new == self.food.pos:
            if self.food.type == 1:
                self.snake.add(new)
            else:
                self.snake.init(new)
            self.display_food()
            self.score = self.score+1
            self.m.set("Score:" + str(self.score))
        #什么都没撞到，继续前进
        else:
            self.snake.move(new)
if __name__ == '__main__':
    root = Tk()
    snakegame = SnakeGame()
    snakegame.run()
    snakegame.mainloop()
