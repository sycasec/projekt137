#!/usr/bin/python

import pygame

from components.keys import Key, KeyHelper
from components.background import Background
from components.score import ScoreHelper
from network.client import myClient

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
    print(f"Broadcast received: {key}")
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

    scores.draw(screen)
    for k in k_dict.values():
        k.draw(screen)

    pygame.display.update()
    GAME_CLOCK.tick(60)

    # End the game if all keys are the same color as "A" key
    if all(
        key.target_color == Key.key_green_color 
        for key in k_dict.values()
        ) or all(
            key.target_color == Key.key_red_color 
            for key in k_dict.values()
        ):
        # TODO: REPLACE THIS WITH SOME "GAME OVER" SCREEN!
        # THIS WILL JUST FREEZE THE SCREEN ON THE LAST FRAME
        break
