#!/usr/bin/python

import pygame

from keys import Key
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

# Temporary Text Surfaces 
title_surface = h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

# Surfaces
bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")


# Test Key Class 
square_position = (WINDOW_WIDTH // 2 - 150 // 2, 400)
jkey_pos = (WINDOW_WIDTH // 2 + 150 // 2, 400)
qkey = Key('Q', square_position)
jkey = Key('J', jkey_pos)

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # --------------------------------- EXPERIMENTAL --------------------------------
        # not sure how to make it so that we wont have to if else for each key
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            # Toggle square color on "q" key press
            qkey.on_key_press()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            jkey.on_key_press()

    # --------------------------------- EXPERIMENTAL --------------------------------

    qkey.update_color()
    jkey.update_color()

    screen.blit(bg, (0,0))
    screen.blit(title_surface, (290, 139))

    qkey.draw(screen)
    jkey.draw(screen)

    pygame.display.update()
    GAME_CLOCK.tick(60)

