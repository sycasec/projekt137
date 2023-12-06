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
        self.title_font_size = 50
        self.color = None


        self.start_time = None

    def choose_color(self, color):
        if color == "RED":
            self.color = ("RED", (224, 102, 102))

        if color == "GREEN":
            self.color = ("GREEN", (102, 224, 102))

    def text(self):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        self.text_font = pygame.font.Font(pygame.font.get_default_font(), self.text_font_size)
        color, color_rgb = self.color

        you_are_text = "You are "
        you_are_surface = self.title_font.render(you_are_text, True, (0, 0, 0))

        assigned_color_text = f"{color}"
        color_surface = self.title_font.render(assigned_color_text, True, color_rgb)

        helper_text = f"Press the {'GREEN' if color == 'RED' else 'RED'} keys to win!"
        helper_surface = self.text_font.render(helper_text, True, "Black")


        self.title_surface = pygame.Surface(
            (
                max(
                    you_are_surface.get_width() + color_surface.get_width(), 
                    helper_surface.get_width()
                ), 
                max(you_are_surface.get_height(), color_surface.get_height()) 
                + helper_surface.get_height()
            ), 
            pygame.SRCALPHA
            )
        self.title_surface.set_colorkey(None)
        self.title_surface.blit(you_are_surface, (0, 0))
        self.title_surface.blit(color_surface, (you_are_surface.get_width(), 0))
        self.title_surface.blit(helper_surface, (0, max(you_are_surface.get_height(), color_surface.get_height())))


        text = "Game starting in"
        self.text_surface = self.text_font.render(text, True, "Black")

        self.countdown_font = pygame.font.Font(pygame.font.get_default_font(), self.countdown_font_size)

    def start_countdown(self):
        self.start_time = time.time()

    def render(self, screen, color):
        self.choose_color(color)
        self.text()

        screen.fill((255, 255, 255))
        # Display "Game starting in"
        text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.countdown_font_size // 2))
        title_rect = self.text_surface.get_rect(center=((self.screen_width - 100) // 2, (self.screen_height - 450) // 2))
        screen.blit(self.text_surface, text_rect)
        screen.blit(self.title_surface,title_rect)

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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1125, 800))
    countdown = Countdown(1125,800,pygame.font.Font(pygame.font.get_default_font(),36))
    countdown.start_countdown()
    while True:
        countdown.render(screen, "RED")
        pygame.display.update()