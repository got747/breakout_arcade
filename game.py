'''
+  создать загтовку
+ сделать движение площадки 
+ сделать растановку кубов
+ сделать движение мяча
+ сделать встречу мяча и куба
- сделать проигрышь
- сделать более интересное откскакивание 
- сделать разные блоки
- сделать разрушение плока


между блоками 75 - в плотную
между блоками 100 - приятный отступ
'''

import arcade

WiDTH = 800
HEIGHT = 600
TITLE = "ARCADE"

STARTING_POINT_X_BAT = HEIGHT / 2 
STARTING_POINT_Y_BAT = 50 
SPEAD_BAT = 5

STARTING_POINT_X_BALL = HEIGHT / 2 
STARTING_POINT_Y_BALL = 100
SPEAD_BALL = 3

STARTING_POINT_FIRST_BLOCK_X = WiDTH / 5.5
STARTING_POINT_FIRST_BLOCK_Y = HEIGHT / 3



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

        self.ball = Ball("images/ball.png", scale=0.2)
        self.ball.center_x = STARTING_POINT_X_BALL
        self.ball.center_y = STARTING_POINT_Y_BALL
        self.ball.change_x = -SPEAD_BALL
        self.ball.change_y = -SPEAD_BALL


    def layout_blocks_one(self):
        centr_x = STARTING_POINT_FIRST_BLOCK_X
        centr_y = STARTING_POINT_FIRST_BLOCK_Y
        for lin in range(9):
            for col in range(7):
                block = Block("images/block_blue.png", center_x= centr_x, center_y=centr_y, scale=0.2)
                self.list_blocks.append(block)
                centr_x += 85
            centr_x = STARTING_POINT_FIRST_BLOCK_X
            centr_y += 35

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle( WiDTH/2, HEIGHT/2, WiDTH, HEIGHT, self.bg)
        self.bat.draw()
        self.ball.draw()
        self.list_blocks.draw()

    def on_key_press(self, symbol: int, modifiers: int):        
        if symbol == arcade.key.LEFT:
            self.bat.change_x = -SPEAD_BAT

        if symbol == arcade.key.RIGHT:
            self.bat.change_x = SPEAD_BAT

        
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.bat.change_x = 0
            
         

    def update(self, delta_time: float):
        self.bat.update()
        self.ball.update()
        
        collision_list = arcade.check_for_collision_with_list(self.ball, self.list_blocks)
        if len(collision_list)>0:
            self.ball.change_y = -self.ball.change_y        
            for i in collision_list:                
                i.remove_from_sprite_lists()


        if arcade.check_for_collision(self.ball,self.bat):
            self.ball.change_y = -self.ball.change_y

class Bat(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        if self.right >= WiDTH or self.left <= 0:
            self.change_x = 0
        
class Block(arcade.Sprite):
    pass

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