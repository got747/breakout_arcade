from traceback import print_tb
import arcade
import arcade.gui

from random import getrandbits, choice

from Sprites.Ball import Ball
from Sprites.Bat import Bat
from Sprites.Block import Block
from typing import Dict
from config import *

from  db.controller_db import save_game, loud_game

class Game(arcade.View):
    def __init__(self, game_data: Dict = {} ):
        super().__init__()
        self.status = True
        self.ball = Ball("images/ball.png", scale=0.2)
        self.list_blocks = arcade.SpriteList()
        self.bat = Bat("images/bat.png", scale=0.2)
        self.bg = arcade.load_texture("images/bg_space.jpg")
        
        self.setup(game_data)

    def setup(self, game_data = {}):
        if not game_data:
            self.bat.center_x = STARTING_POINT_X_BAT
            self.bat.center_y = STARTING_POINT_Y_BAT

            self.layout_blocks_one()

            self.ball.center_x = STARTING_POINT_X_BALL
            self.ball.center_y = STARTING_POINT_Y_BALL
            self.ball.change_x = -SPEAD_BALL
            self.ball.change_y = -SPEAD_BALL
        else:

            self.bat.center_x = game_data['x']
            self.bat.center_y = game_data['y']

            self.layout_blocks_one()

            self.ball.center_x = game_data['x_1']
            self.ball.center_y = game_data['y_1']
            self.ball.change_x = -game_data['change_x_1']
            self.ball.change_y = -game_data['change_y']
    

    def layout_blocks_one(self):
        centr_x = STARTING_POINT_FIRST_BLOCK_X
        centr_y = STARTING_POINT_FIRST_BLOCK_Y
        for lin in range(9):
            for col in range(7):
                block = Block(tuple_texturs=choice(TUPLE_PATH_IMAGE_BLOCKS))
                block.set_position(centr_x, centr_y)
                self.list_blocks.append(block)
                centr_x += BLOCK_STEP_X_AXIS
            centr_x = STARTING_POINT_FIRST_BLOCK_X
            centr_y += BLOCK_STEP_Y_AXIS

    def on_draw(self):
        arcade.start_render()
        if self.status:
            arcade.draw_texture_rectangle(WiDTH / 2, HEIGHT / 2, WiDTH, HEIGHT, self.bg)
            self.bat.draw()
            self.ball.draw()
            self.list_blocks.draw()
        else:
            arcade.draw_text("GAME OVER", WiDTH / 2.6, HEIGHT / 2, arcade.color.RED, 24)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.bat.change_x = -SPEAD_BAT

        if symbol == arcade.key.RIGHT:
            self.bat.change_x = SPEAD_BAT

        if symbol == arcade.key.ESCAPE:
            { 'bats_info': {'x': 12, 'y': 12, 'change_x': 12}}
            game_data = {

                'balls_info': {
                    'x': self.ball.center_x
                    , 'y': self.ball.center_y
                    , 'change_x': self.ball.change_x
                    , 'change_y': self.ball.change_y},

                'bats_info': {
                    'x': self.bat.center_x
                    , 'y': self.bat.center_y
                    , 'change_x': self.bat.change_x}
            }
            save_game("quick_save", game_data)
            view = StopView()
            self.window.show_view(view)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.bat.change_x = 0

    def update(self, delta_time: float):

        if self.status:
            self.bat.update()
            self.ball.update()

            rand = getrandbits(1)

            collision_list = arcade.check_for_collision_with_list(self.ball, self.list_blocks)
            if len(collision_list) > 0:

                self.ball.change_y = -self.ball.change_y

                if rand:
                    self.ball.change_x = -self.ball.change_x

                for i in collision_list:
                    i.hit()

            if self.ball.bottom <= 0:
                self.status = False

            if arcade.check_for_collision(self.ball, self.bat):
                self.ball.change_y = -self.ball.change_y
                self.ball.bottom = self.bat.top

class StopView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="Click escape to finish or enter the name of the save and click return to exit.\
                                                    Clicking on return without name save will end the game without saving",
                                              width=450,
                                              height=60)

        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        self.ui_text_input = arcade.gui.UIInputText(width=450, height=40) 
       
        self.v_box.add(self.ui_text_input.with_space_around(1).with_border(color=arcade.color.WHITE))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
  
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RETURN: 
            if self.ui_text_input.text.strip() != "":
                pass
            else:
                exit()
            
        if symbol == arcade.key.ESCAPE: 
            game = Game(loud_game("quick_save"))
            self.window.show_view(game)

class StartView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="Enter the name of the save or click return",
                                              width=450,
                                              height=60)

        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        self.ui_text_input = arcade.gui.UIInputText(width=450, height=40) 
       
        self.v_box.add(self.ui_text_input.with_space_around(1).with_border())

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
    
    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
  
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RETURN: 
            game = Game(loud_game(self.ui_text_input.text.strip()))
            self.window.show_view(game)

window = arcade.Window(WiDTH, HEIGHT, TITLE)
menu = StartView()
window.show_view(menu)
arcade.run()
