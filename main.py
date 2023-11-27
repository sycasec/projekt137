#!/usr/bin/python

import pygame
import random

from components.keys import Key, KeyHelper
from components.background import Background
from components.score import ScoreHelper
from network.client import GameClient
from network.server import myServer
from screens.home import HomeScreen
from screens.about import AboutScreen
from screens.loading import Waiting
from screens.assignment import ColorAssignment
from screens.countdown import Countdown
from screens.gameover import GameOver

WINDOW_WIDTH = 1125
WINDOW_HEIGHT = 800
FACTOR = 25
WINDOW_TITLE = "Keyboard Splatoon"
GAME_CLOCK = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)


# Temporary Fonts
h1_size: int = 50
h3_size: int = 35

# I dont have DM sans installed yet.
h1_dm_sans = pygame.font.Font(pygame.font.get_default_font(), h1_size)
score_font = pygame.font.Font(pygame.font.get_default_font(), h3_size)
keys_font = pygame.font.Font(pygame.font.get_default_font(),36)

# Temporary Text Surfaces
title_surface = h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

# Surfaces
bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")


# Key generation
keys = KeyHelper(keys_font)
keys.gen_keys()
k_dict = keys.get_keys()

# Score generation
scores = ScoreHelper(score_font)

# Network actions
def receive_keypress(key):
    try:
        key_obj = k_dict[key]
    except KeyError:
        return

    key_obj.on_key_press()
    # TODO: If you press one key extremely fast, sometimes one player 
    # will get multiple points per color toggle. 
    # Ex. scores are 200-150, even if you just spammed Q there's a slight bias to green
    # This can be seemingly fixed by reducing Key.t_duration to 100
    if key_obj.target_color == key_obj.key_green_color:
        to_add = scores.GREEN
    elif key_obj.target_color == key_obj.key_red_color:
        to_add = scores.RED
    scores.add_score(to_add)

def receive_keyboard_state(s):
    keys.set_key_colors_from_string(s)

home_screen = HomeScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
about_screen = AboutScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
waiting_screen = Waiting(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
assignment_screen = ColorAssignment(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
countdown_screen = Countdown(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
gameover_screen = GameOver(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
active_screen = "home"


# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # --------------------------------- EXPERIMENTAL --------------------------------
            if event.key in k_dict:
                try:
                    c.send(event.key)
                except Exception as e:
                    print("Something went wrong when sending your keypress")
            # --------------------------------- EXPERIMENTAL --------------------------------
        result = home_screen.handle_event(event)
        if result is not None:
            if result == 0:  # initialize a game button
                s = myServer()
                c = GameClient(
                    receive_keypress=receive_keypress,
                    receive_keyboard_state=receive_keyboard_state
                )
                active_screen = "play"
            elif result == 1:  # join a game button
                c = GameClient(
                    receive_keypress=receive_keypress,
                    receive_keyboard_state=receive_keyboard_state
                )
                c.send(keys.get_key_colors().encode()) # Synchronize everyone's keyboard colors to ours
                active_screen = "load"
            elif result == 2:  # About button
                active_screen = "about"
            elif result == 3:  # Quit button
                pygame.quit()
                exit()
        elif active_screen == "about":
            about_result = about_screen.handle_event(event)
            if about_result == "back":
                active_screen = "home"
        elif active_screen == "assignment":
            assignment_screen.render(screen)
            result = assignment_screen.handle_event(event)
            if result == "countdown":
                active_screen = "countdown"
                countdown_screen.start_countdown()

    if active_screen == "home":
        home_screen.render(screen)

    elif active_screen == "play":
        for k in k_dict.values():
            k.update_color()

        screen.blit(bg, (0, 0))
        screen.blit(title_surface, (290, 139))

        scores.draw(screen)
        for k in k_dict.values():
            k.draw(screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            active_screen = "home"

        # End the game if all keys are the same color
        if all(
            key.target_color == Key.key_green_color 
            for key in k_dict.values()
            ):
            active_screen = "gameover"
            winner = "GREEN"
        if all(
                key.target_color == Key.key_red_color 
                for key in k_dict.values()
            ):
            active_screen = "gameover"
            winner = "RED"

    elif active_screen == "about":
        about_screen.render(screen)

    elif active_screen == "load":
        waiting_screen.update()
        waiting_screen.render(screen)
        result = waiting_screen.handle_event(event)
        if result == "assignment":
            active_screen = "assignment"

    elif active_screen == "countdown":
        countdown_screen.render(screen)
        if countdown_screen.is_complete():
            active_screen = "play"

    elif active_screen == "gameover":
        # TODO: IMPORTANT! Find a way to kill the client and server before continuing
        gameover_screen.render(screen, winner)
        gameover_result = gameover_screen.handle_event(event)
        if gameover_result == "rematch":
            scores.reset_scores()   # Generate new starting colors
            new_colors = list(("R" * 13) + ("G" * 13))
            random.shuffle(new_colors)
            new_colors = "".join(new_colors)
            keys.set_key_colors_from_string(new_colors)
            c.send(new_colors.encode())

            active_screen = "play"


    pygame.display.update()
    GAME_CLOCK.tick(60)
