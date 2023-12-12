#!/usr/bin/python

import os
import pygame

from pygame import mixer
from components.keys import Key, KeyHelper
from components.background import Background
from components.timer import Timer
from components.screenhandler import ScreenHandler
from components.score import ScoreHelper
from network.client import GameClient
from network.server import myServer

from sys import exit

WINDOW_WIDTH = 1125
WINDOW_HEIGHT = 800
FACTOR = 25
WINDOW_TITLE = "Keyboard Splatoon"
GAME_CLOCK = pygame.time.Clock()
pygame.mixer.init()

class KeyboardSplatoon():
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.FULLSCREEN)

        # logo
        img = pygame.image.load('assets/logo.png')
        pygame.display.set_icon(img)

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
        self.active_screen = "splash"
        self.winner = None

        # self.active_screen = "gameover"
        # self.winner = "RED"

        self.client_type = None
        self.host_address = None
        self.is_client_initialized = False

        #Network attributes
        self.server = None
        self.client = None

        self.color = None

        self.multiplier = 1

        self.moves = "DDD"

        self.is_game_start = False

        #Sound
        mixer.music.load('assets/sounds/bg.mp3')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)
        mixer.music.set_pos(10.4)

        self.combo_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "combo.wav"))
        self.countdown_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "countdown.mp3"))
        self.timer_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "gametimer.mp3"))
        self.win_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "gameover.mp3"))

        self.countdown_channel = pygame.mixer.Channel(1)

        #event constant
        self.GAMESTART = "GAME START"
        self.BACKHOME = "BACK TO HOME"

    def gameover_sound(self):
        self.timer_sound.stop()
        self.win_sound.play()

    def encode_game_state(self, delimiter="$"):
        """Takes the current keyboard and player scores and encodes them in a delimited string

        Returns:
            str: delimited string containing the colors of each key,
                the green player's score, and the red player's score
        """
        keys = self.keys.get_key_colors()
        scores = self.scores.get_scores()

        game_state = []
        game_state.append(keys)
        game_state.append(str(scores[self.scores.GREEN].value))
        game_state.append(str(scores[self.scores.RED].value))

        return delimiter.join(game_state)

    def decode_game_state(self, game_state, delimiter="$"):
        keys, green_score, red_score = game_state.split(delimiter)
        self.keys.set_key_colors_from_string(keys)

        self.scores.set_score(self.scores.GREEN, int(green_score))
        self.scores.set_score(self.scores.RED, int(red_score))

    def increment_combo(self, key_obj):
        if key_obj.target_color == key_obj.key_green_color:
            new_key_color = "G"
        elif key_obj.target_color == key_obj.key_red_color:
            new_key_color = "R"
        else:
            new_key_color = "D"
        # Append new color to list of moves
        self.moves = self.moves[1:] + new_key_color

        if (self.color == "GREEN" and self.moves == "GGG") or (
            self.color == "RED" and self.moves == "RRR"
        ):
            self.multiplier += 1
            self.combo_sound.set_volume(0.25)
            self.combo_sound.play()
            self.moves = "DDD"
        elif (self.color == "GREEN" and new_key_color != "G") or (
            self.color == "RED" and new_key_color != "R"
        ):
            self.multiplier = 1

    # Network actions
    def receive_keypress(self, key):
        try:
            key_obj: Key = self.k_dict[key]
        except KeyError:
            return

        key_obj.on_key_press()
        self.increment_combo(key_obj)

        if key_obj.target_color == key_obj.key_green_color:
            to_add = self.scores.GREEN
        elif key_obj.target_color == key_obj.key_red_color:
            to_add = self.scores.RED
        self.scores.add_score(to_add, 10 * self.multiplier)

    def receive_keyboard_state(self, s):
        self.scores.reset_scores()
        self.timer_bar.reset()
        self.keys.set_key_colors_from_string(s)

    def event_listener(self,msg):
        if msg == self.GAMESTART:
            if self.server is not None:
                self.keys.randomize_key_colors()
                self.client.send(self.keys.get_key_colors().encode())

            self.scores.reset_scores()
            self.timer_bar.reset()
            self.multiplier = 1
            self.is_game_start = True
            self.multiplier = 1

            self.active_screen = "countdown"
            self.screen_handler.begin_countdown()

        elif msg == self.BACKHOME:
            self.on_drop_connection()

    def on_drop_connection(self):
        self.is_game_start = False
        self.active_screen = "home"
        if self.server is not None:
            self.server.kill()
            self.server = None
        if self.client is not None:
            self.client.kill()
            self.client = None

    #Main Play
    def play(self, event):

        for k in self.k_dict.values():
            k.update_color()

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title_surface, (290, 139))

        dt = GAME_CLOCK.tick(60) / 1000.0
        self.timer_bar.update(dt)
        self.timer_bar.draw(self.screen)
        self.scores.draw(self.screen, self.color, self.multiplier)

        if self.timer_bar.start_countdown and not self.timer_bar.played_timer_sound:
            self.countdown_channel.play(self.timer_sound)
            self.timer_bar.played_timer_sound = True

        if self.timer_bar.is_done():
            winner = self.scores.publish_winner()

            self.keys.set_key_colors_from_string(winner * 26)
            self.client.send(self.encode_game_state())

        for k in self.k_dict.values():
            k.draw(self.screen)

        # End the game if all keys are the same color
        if all(
            key.target_color == Key.key_green_color
            for key in self.k_dict.values()
            ):
            self.active_screen = "gameover"
            self.winner = "GREEN"
            self.is_game_start = False
            self.gameover_sound()
        elif all(
                key.target_color == Key.key_red_color
                for key in self.k_dict.values()
            ):
            self.active_screen = "gameover"
            self.winner = "RED"
            self.is_game_start = False
            self.gameover_sound()
        elif all(
                key.target_color == Key.key_default_color
                for key in self.k_dict.values()
            ):
            self.active_screen = "gameover"
            self.winner = "TIE"
            self.is_game_start = False
            self.gameover_sound()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    # --------------------------------- EXPERIMENTAL --------------------------------
                    if self.active_screen == "play" and event.key in self.k_dict:
                        try:
                            self.receive_keypress(event.key)
                            self.client.send(self.encode_game_state())
                        except Exception as e:
                            print("Something went wrong when sending your keypress")
                    # --------------------------------- EXPERIMENTAL --------------------------------
                if self.active_screen == "home":
                    self.active_screen = self.screen_handler.update_home(event)

                # Handle entering of IP address for waiting client
                if self.active_screen == "waiting":
                    if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                        self.active_screen = self.screen_handler.update_waiting(event, self.client_type)

                        if self.client_type == "client" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            self.host_address = self.screen_handler.get_host()
                            print("Connecting to host", self.screen_handler.get_host())

            if self.active_screen == "quit":
                print("Quitting game")
                pygame.quit()
                exit()

            if self.active_screen == "play":
                if not mixer.music.get_busy():
                        mixer.music.set_volume(0.25)
                        mixer.music.play(-1)
                        mixer.music.set_pos(14)
                self.play(event)

            else:
                kwargs = {}
                if self.active_screen in ("about", "gameover"):
                    kwargs.update({'event': event})
                if self.active_screen == "gameover":
                    kwargs.update({"winner":self.winner})
                    mixer.music.stop()
                if self.active_screen == "countdown":
                    kwargs.update({"color":self.color})
                    self.countdown_sound.set_volume(0.25)
                    self.countdown_sound.play()
                    mixer.music.stop()
                if self.active_screen == "waiting":
                    kwargs.update({"client_type": self.client_type,
                                   "ip_address": self.host_address,
                                   "color": self.color})
                    mixer.music.stop()

                # fix overriding of active_screen issue
                if self.is_game_start and (self.active_screen == "waiting"):
                    self.active_screen = "countdown"
                    kwargs.update({"color":self.color})
                    mixer.music.stop()
                self.active_screen = self.screen_handler.switch_screen(self.active_screen, **kwargs)

                if self.active_screen == "host":
                    if self.server is None:
                        self.server = myServer(on_drop_connection=self.on_drop_connection)
                    self.client = GameClient(
                        receive_keypress=self.receive_keypress,
                        receive_keyboard_state=self.receive_keyboard_state,
                        receive_game_state=self.decode_game_state,
                        event_listener=self.event_listener,
                        on_drop_connection=self.on_drop_connection,
                    )
                    print("Initialized Server")
                    print("Initialized Game Client")
                    self.active_screen = "waiting"
                    self.color = "GREEN"
                    self.client_type = "host"
                    self.host_address = self.server.hostAddress
                    mixer.music.stop()

                elif self.active_screen == "join":
                    self.color = "RED"
                    self.client_type = "client"
                    self.active_screen = "waiting"
                    mixer.music.stop()

                # Handle waiting client. Wait for user input on host address
                elif self.client_type == "client" and self.active_screen == "waiting":
                    # Ensure GameClient is run only once
                    if self.host_address != None and not self.is_client_initialized:
                        try:
                            self.client = GameClient(
                                host=self.host_address,
                                receive_keypress=self.receive_keypress,
                                receive_keyboard_state=self.receive_keyboard_state,
                                receive_game_state=self.decode_game_state,
                                event_listener=self.event_listener,
                                on_drop_connection=self.on_drop_connection,
                            )
                            self.is_client_initialized = True
                            print("Initialized Game Client")
                        except:
                            self.host_address = None

                elif self.active_screen == "rematch":
                    # necessary. otherwise not synching if hosts initiate rematch
                    if self.server != None:
                        self.server.broadcast(self.GAMESTART.encode())
                    else:
                        self.client.send(self.GAMESTART.encode())

                elif self.active_screen == "home":
                    self.host_address = None
                    self.screen_handler.clear_loading_inputbox()
                    self.is_client_initialized = False

                    if self.server is not None:
                        self.server.broadcast(self.BACKHOME.encode())
                    if self.client is not None:
                        self.client.send(self.BACKHOME.encode())

            pygame.display.update()
            GAME_CLOCK.tick(60)
if __name__ == "__main__":
    game = KeyboardSplatoon()
    game.run()
