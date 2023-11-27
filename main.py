#!/usr/bin/python

import pygame

from components.keys import KeyHelper
from components.background import Background
from network.client import myClient
from network.server import myServer
from screens.home import HomeScreen
from screens.about import AboutScreen
from screens.loading import Waiting
from screens.assignment import ColorAssignment
from screens.countdown import Countdown

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

# I dont have DM sans installed yet.
h1_dm_sans = pygame.font.Font(pygame.font.get_default_font(), h1_size)
keys_font = pygame.font.Font(pygame.font.get_default_font(),36)

# Temporary Text Surfaces
title_surface = h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

# Surfaces
bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")


# Key generation
keys = KeyHelper(keys_font)
keys.gen_keys()
k_dict = keys.get_keys()

# Network actions
def receive_keypress(key):
    print(f"Broadcast received: {key}")
    try:
        k_dict[key].on_key_press()
    except KeyError:
        pass

home_screen = HomeScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
about_screen = AboutScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
waiting_screen = Waiting(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
assignment_screen = ColorAssignment(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
countdown_screen = Countdown(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
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
                c = myClient(on_receive=receive_keypress)
                active_screen = "play"
            elif result == 1:  # join a game button
                c = myClient(on_receive=receive_keypress)
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

        for k in k_dict.values():
            k.draw(screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            active_screen = "home"

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


    pygame.display.update()
    GAME_CLOCK.tick(60)


