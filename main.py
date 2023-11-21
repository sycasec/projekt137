#!/usr/bin/python

import pygame

from keys import Key, KeyHelper
from background import Background

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
h1_dm_sans = pygame.font.Font("InterNerdFontPropo-Bold.otf", h1_size)
keys_font = pygame.font.Font("InterNerdFontPropo-Bold.otf",36)

# Temporary Text Surfaces 
title_surface = h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

# Surfaces
bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")


# Test Key Class 
# square_position = (160, 420)
# jkey_pos = (200, 485)
# qkey = Key('Q', square_position, keys_font)
# jkey = Key('J', jkey_pos, keys_font)

keys = KeyHelper(keys_font)
keys.gen_keys()
k_dict = keys.get_keys()
# top_row = keys.gen_top_row()
# top_row = keys.gen_mid_row()
# bot_row = keys.gen_bot_row()

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # --------------------------------- EXPERIMENTAL --------------------------------
        elif event.type == pygame.KEYDOWN:
            for key in k_dict.values():
                if event.key == key.key_code:
                    key.on_key_press()
    # --------------------------------- EXPERIMENTAL --------------------------------

    # qkey.update_color()
    # jkey.update_color()
    for k in k_dict.values():
        k.update_color()

    screen.blit(bg, (0,0))
    screen.blit(title_surface, (290, 139))

    # qkey.draw(screen)
    # jkey.draw(screen)

    for k in k_dict.values():
        k.draw(screen)

    pygame.display.update()
    GAME_CLOCK.tick(60)

