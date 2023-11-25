#!/usr/bin/python

import pygame

from components.keys import KeyHelper
from components.background import Background
from network.client import myClient

WINDOW_WIDTH = 1125 
WINDOW_HEIGHT = 800 
FACTOR = 25
WINDOW_TITLE = "Keyboard Splatoon"
GAME_CLOCK = pygame.time.Clock()
SCORES = {"R":0, "G":0}

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
        key_obj = k_dict[key]
        key_obj.on_key_press()
        if key_obj.target_color == key_obj.key_green_color:
            to_add = "G"
        elif key_obj.target_color == key_obj.key_red_color:
            to_add = "R"
        SCORES[to_add] += 10

        print(SCORES)
    except KeyError:
        pass

c = myClient(on_receive=receive_keypress)

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # --------------------------------- EXPERIMENTAL --------------------------------
        elif event.type == pygame.KEYDOWN:
            if event.key in k_dict:
                try:
                    c.send(event.key)
                except Exception as e:
                    print("Something went wrong when sending your keypress")
    # --------------------------------- EXPERIMENTAL --------------------------------

    for k in k_dict.values():
        k.update_color()

    screen.blit(bg, (0,0))
    screen.blit(title_surface, (290, 139))

    for k in k_dict.values():
        k.draw(screen)

    pygame.display.update()
    GAME_CLOCK.tick(60)


