'''
+ создать заготовку
+ сделать движение площадки 
+ сделать расстановку кубов
+ сделать движение мяча
+ сделать встречу мяча и куба
+ сделать проигрыш
+ сделать более интересное отскакивание 
+ сделать разные блоки
- сделать разрушение блока

между блоками 75 - в плотную
между блоками 100 - приятный отступ
'''

import arcade
from random import getrandbits, choice

WiDTH = 800
HEIGHT = 600
TITLE = "ARCADE"

STARTING_POINT_X_BAT = HEIGHT / 2 
STARTING_POINT_Y_BAT = 50 
SPEAD_BAT = 5

STARTING_POINT_X_BALL = HEIGHT / 2 
STARTING_POINT_Y_BALL = 100
SPEAD_BALL = 2

STARTING_POINT_FIRST_BLOCK_X = WiDTH / 5.5
STARTING_POINT_FIRST_BLOCK_Y = HEIGHT / 3

TUPLE_PATH_IMAGE_BLOCKS = (
    ("images/block_blue.png", "images/block_blue_destroyed.png"),
    ("images/block_red.png", "images/block_red_destroyed.png"),
    ("images/block_purple.png", "images/block_purple_destroyed.png"))

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()

    def setup(self):
        self.bg = arcade.load_texture("images/bg_space.jpg")
        
        self.bat = Bat("images/bat.png", scale=0.2)
        self.bat.center_x = STARTING_POINT_X_BAT
        self.bat.center_y = STARTING_POINT_Y_BAT

        self.list_blocks = arcade.SpriteList()
        self.layout_blocks_one()

        self.ball = Ball("images/ball.png",scale=0.2)

        self.ball.center_x = STARTING_POINT_X_BALL
        self.ball.center_y = STARTING_POINT_Y_BALL
        self.ball.change_x = -SPEAD_BALL
        self.ball.change_y = -SPEAD_BALL
        self.status = True


    def layout_blocks_one(self):
        centr_x = STARTING_POINT_FIRST_BLOCK_X
        centr_y = STARTING_POINT_FIRST_BLOCK_Y
        for lin in range(9):
            for col in range(7):
                block = Block(tuple_texturs=choice(TUPLE_PATH_IMAGE_BLOCKS))
                block.set_position(centr_x, centr_y)
                self.list_blocks.append(block)
                centr_x += 85
            centr_x = STARTING_POINT_FIRST_BLOCK_X
            centr_y += 35

    def on_draw(self):
        arcade.start_render()
        if self.status:
            arcade.draw_texture_rectangle( WiDTH/2, HEIGHT/2, WiDTH, HEIGHT, self.bg)
            self.bat.draw()
            self.ball.draw()
            self.list_blocks.draw()
        else:
            arcade.draw_text("GAME OVER", WiDTH/2.6, HEIGHT/2, arcade.color.RED, 24)

    def on_key_press(self, symbol: int, modifiers: int):        
        if symbol == arcade.key.LEFT:
            self.bat.change_x = -SPEAD_BAT

        if symbol == arcade.key.RIGHT:
            self.bat.change_x = SPEAD_BAT

        
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.bat.change_x = 0  

    def update(self, delta_time: float):
         
        if self.status:
            self.bat.update()
            self.ball.update()

            rand = getrandbits(1)

            collision_list = arcade.check_for_collision_with_list(self.ball, self.list_blocks)
            if len(collision_list)>0:
                
                self.ball.change_y = -self.ball.change_y  
                
                if rand:
                    self.ball.change_x = -self.ball.change_x    

                for i in collision_list:                
                    i.hit()

            if self.ball.bottom <= 0:
                self.status = False

            if arcade.check_for_collision(self.ball,self.bat):
                self.ball.change_y = -self.ball.change_y

class Bat(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        if self.right >= WiDTH or self.left <= 0:
            self.change_x = 0
        
class Block(arcade.Sprite):
    def __init__(self, tuple_texturs):
        super().__init__(filename = tuple_texturs[0], scale=0.2)
        self.hp = 2
        if len(tuple_texturs)>1:            
            self.append_texture(arcade.load_texture(tuple_texturs[1]))
               
    def hit(self):
        self.hp -= 1       
        if (len(self.textures)>1):
            self.set_texture(1)

        if self.hp == 0:
            self.kill()
           

class Ball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right >= WiDTH or self.left <= 0:
            self.change_x = -self.change_x
        if self.top >= HEIGHT or self.bottom <= 0:
            self.change_y = -self.change_y


game = Game(WiDTH, HEIGHT, TITLE)
arcade.run()


