import pygame
import sys
import random

class ColorAssignment:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50

        self.assigned_colors = []

        self.text()

    def text(self):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        random_color, color_rgb = self.get_random_color()

        you_are_text = "You are "
        you_are_surface = self.title_font.render(you_are_text, True, (0, 0, 0))

        assigned_color_text = f"{random_color}"
        color_surface = self.title_font.render(assigned_color_text, True, color_rgb)

        self.title_surface = pygame.Surface((you_are_surface.get_width() + color_surface.get_width(), max(you_are_surface.get_height(), color_surface.get_height())), pygame.SRCALPHA)
        self.title_surface.set_colorkey(None)
        self.title_surface.blit(you_are_surface, (0, 0))
        self.title_surface.blit(color_surface, (you_are_surface.get_width(), 0))

    def get_random_color(self):
        colors = {
            "RED": (224, 102, 102),
            "GREEN": (102, 224, 102),
        }

        available_colors = [color for color in colors.keys() if color not in self.assigned_colors]

        if not available_colors:
            self.assigned_colors = []
            available_colors = list(colors.keys())

        random_color = random.choice(available_colors)
        color_rgb = colors[random_color]
        self.assigned_colors.append(random_color)

        return random_color, color_rgb

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return "countdown"

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2)))
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1125, 800))
    assignment = ColorAssignment(1125,800,pygame.font.Font(pygame.font.get_default_font(),36))
    while True:
        assignment.render(screen)