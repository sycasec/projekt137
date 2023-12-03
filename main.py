#!/usr/bin/python

import pygame
import random

from components.keys import Key, KeyHelper
from components.background import Background
from components.timer import Timer
from components.screenhandler import ScreenHandler
from components.score import ScoreHelper
from network.client import GameClient
from network.server import myServer
WINDOW_WIDTH = 1125
WINDOW_HEIGHT = 800
FACTOR = 25
WINDOW_TITLE = "Keyboard Splatoon"
GAME_CLOCK = pygame.time.Clock()

class KeyboardSplatoon():
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Temporary Fonts
        self.h1_size: int = 50
        self.h3_size: int = 35

        # I dont have DM sans installed yet.
        self.h1_dm_sans = pygame.font.Font(pygame.font.get_default_font(), self.h1_size)
        self.score_font = pygame.font.Font(pygame.font.get_default_font(), self.h3_size)
        self.keys_font = pygame.font.Font(pygame.font.get_default_font(),36)

        # Temporary Text Surfaces
        self.title_surface = self.h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

        # Surfaces
        self.bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")

        # Timer
        self.timer_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.timer_bar = Timer(50, 50, (WINDOW_WIDTH-200), 10, self.timer_font)

        # Key generation
        self.keys = KeyHelper(self.keys_font)
        self.keys.gen_keys()
        self.k_dict = self.keys.get_keys()

        # Score generation
        self.scores = ScoreHelper(self.score_font)

        #Scren handler
        self.screen_handler = ScreenHandler(self.screen,WINDOW_WIDTH,WINDOW_HEIGHT,self.keys_font)
        self.active_screen = "home"

        #Network attributes
        self.server = None
        self.client = None

    # Network actions
    def receive_keypress(self,key):
        try:
            key_obj = self.k_dict[key]
        except KeyError:
            return

        key_obj.on_key_press()
        # TODO: If you press one key extremely fast, sometimes one player
        # will get multiple points per color toggle.
        # Ex. scores are 200-150, even if you just spammed Q there's a slight bias to green
        # This can be seemingly fixed by reducing Key.t_duration to 100

        to_add = 0
        if key_obj.target_color == key_obj.key_green_color:
            to_add = self.scores.GREEN
        elif key_obj.target_color == key_obj.key_red_color:
            to_add = self.scores.RED
        self.scores.add_score(to_add)

    def receive_keyboard_state(self, s):
        self.scores.reset_scores()
        self.keys.set_key_colors_from_string(s)

    def begin_game(self):
        self.active_screen = "countdown"
        self.screen_handler.begin_countdown()

    #Main Play
    def play(self, event):
        for k in self.k_dict.values():
            k.update_color()

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title_surface, (290, 139))

        dt = GAME_CLOCK.tick(60) / 1000.0
        self.timer_bar.update(dt)
        self.timer_bar.draw(self.screen)
        self.scores.draw(self.screen)

        for k in self.k_dict.values():
            k.draw(self.screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active_screen = "home"

        # End the game if all keys are the same color
        if all(
            key.target_color == Key.key_green_color
            for key in self.k_dict.values()
            ):
            self.active_screen = "gameover"
            winner = "GREEN"
        if all(
                key.target_color == Key.key_red_color
                for key in self.k_dict.values()
            ):
            self.active_screen = "gameover"
            winner = "RED"

    def run(self):
        while True:
            if self.active_screen == "quit":
                pygame.quit()
                exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    # --------------------------------- EXPERIMENTAL --------------------------------
                    if self.active_screen == "play" and event.key in self.k_dict:
                        try:
                            self.client.send(event.key)
                        except Exception as e:
                            print("Something went wrong when sending your keypress")
                    # --------------------------------- EXPERIMENTAL --------------------------------
                if self.active_screen == "home":
                    self.active_screen = self.screen_handler.update_home(event)

            if self.active_screen == "play":
                self.play(event)

            else:
                self.active_screen = self.screen_handler.switch_screen(self.active_screen,event)

                if self.active_screen == "host":
                    self.server = myServer()
                    self.client = GameClient(
                        receive_keypress=self.receive_keypress,
                        receive_keyboard_state=self.receive_keyboard_state,
                        begin_game=self.begin_game
                    )

                elif self.active_screen == "join":
                    self.client = GameClient(
                        receive_keypress=self.receive_keypress,
                        receive_keyboard_state=self.receive_keyboard_state,
                        begin_game=self.begin_game
                    )


            pygame.display.update()
            GAME_CLOCK.tick(60)
if __name__ == "__main__":
    game = KeyboardSplatoon()
    game.run()