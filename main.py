#!/usr/bin/python

import pygame
from background import Background

WINDOW_WIDTH = 1125 
WINDOW_HEIGHT = 800 
FACTOR = 25
WINDOW_TITLE = "Keyboard Splatoon"
GAME_CLOCK = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)


# >>>>>>>>>>>>>>>>>>>>>>>>>>> Temporary Fonts <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
h1_size: int = 50

# I dont have DM sans installed yet.
h1_dm_sans = pygame.font.Font("InterNerdFontPropo-Bold.otf", h1_size)

# >>>>>>>>>>>>>>>>>>>>>>>  Temporary Text Surfaces <<<<<<<<<<<<<<<<<<<<<<<<<<
title_surface = h1_dm_sans.render("KEYBOARD SPLATOON", True, "Black")

# Surfaces
bg = Background([WINDOW_WIDTH, WINDOW_HEIGHT]).generate("White")



# >>>>>>>>>>>>>>>>>>>>>>>>>> EXPERIMENTAL <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Red square properties
square_size = 50
square_color = pygame.Color("Red")
target_color = pygame.Color("Green")
square_position = (WINDOW_WIDTH // 2 - square_size // 2, 400)

# Transition speed
transition_speed = 0.005 
current_color = pygame.Color(*square_color)
transition_timer = 0
transition_duration = 1000

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # --------------------------------- EXPERIMENTAL --------------------------------
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            # Toggle square color on "j" key press
            # square_color = "Green" if square_color == "Red" else "Red"
            target_color, current_color = current_color, target_color
            transition_timer = pygame.time.get_ticks()


    # Calculate time elapsed since the transition started
    elapsed_time = pygame.time.get_ticks() - transition_timer

    # Interpolate between current color and target color
    if elapsed_time < transition_duration:
        interpolation_factor = elapsed_time / transition_duration
        square_color = pygame.Color(
            int(pygame.math.lerp(square_color.r, target_color.r, interpolation_factor)),
            int(pygame.math.lerp(square_color.g, target_color.g, interpolation_factor)),
            int(pygame.math.lerp(square_color.b, target_color.b, interpolation_factor))
        )    


    # --------------------------------- EXPERIMENTAL --------------------------------

    screen.blit(bg, (0,0))
    screen.blit(title_surface, (290, 339))

     # Draw the square
    pygame.draw.rect(screen, square_color, (square_position[0], square_position[1], square_size, square_size))

    pygame.display.update()
    GAME_CLOCK.tick(60)

