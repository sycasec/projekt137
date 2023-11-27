import pygame
import time

class Countdown:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.text_font_size = 24
        self.countdown_font_size = 100
        self.countdown_duration = 3  # seconds

        self.text()

        self.start_time = None

    def text(self):
        self.text_font = pygame.font.Font(pygame.font.get_default_font(), self.text_font_size)
        text = "Game starting in"
        self.text_surface = self.text_font.render(text, True, "Black")

        self.countdown_font = pygame.font.Font(pygame.font.get_default_font(), self.countdown_font_size)

    def start_countdown(self):
        self.start_time = time.time()

    def render(self, screen):
        screen.fill((255, 255, 255))
        # Display "Game starting in"
        text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.countdown_font_size // 2))
        screen.blit(self.text_surface, text_rect)

        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.countdown_duration - elapsed_time)
            countdown_text = str(int(remaining_time) + 1)

            digit_surfaces = [self.countdown_font.render(digit, True, "Black") for digit in countdown_text]

            total_width = sum([surface.get_width() for surface in digit_surfaces])
            x_position = (self.screen_width - total_width) // 2
            y_position = self.screen_height // 2 -20

            for digit_surface in digit_surfaces:
                screen.blit(digit_surface, (x_position, y_position))
                x_position += digit_surface.get_width()

            
    def is_complete(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            return elapsed_time >= self.countdown_duration
        return False
