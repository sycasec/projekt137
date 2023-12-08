import pygame
import sys

class SplashScreen:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width, self.screen_height, self.font = screen_width, screen_height, font
        self.lines = ["NET NINJAS", "presents", "KEYBOARD SPLATOON"]
        self.clock, self.start_time = pygame.time.Clock(), pygame.time.get_ticks()
        self.current_line = 0
        self.typing_speed = 25
        self.pause_duration = 1000
        self.square_animation_duration = 500
        self.square_animation_started = False
        self.square_animation_elapsed = 0
        self.squares = []

    def animate_lines(self, screen):
        if self.current_line < len(self.lines):
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            characters_to_show = min(int(elapsed_time / (1000 / self.typing_speed)), len(self.lines[self.current_line]))

            current_text = self.lines[self.current_line][:characters_to_show]
            text_surface = self.font.render(current_text, True, "Black")

            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text_surface, text_rect)

            if characters_to_show == len(self.lines[self.current_line]):
                if current_time - self.start_time > self.pause_duration:
                    self.current_line += 1
                    self.start_time = current_time
                    if self.current_line == len(self.lines) - 1 and not self.square_animation_started:
                        self.start_square_animation()

    def start_square_animation(self):
        square_sizes = [36, 24, 18]
        container_width = sum(square_sizes) + 2 * 10
        container_height = max(square_sizes)

        container_x_position = self.screen_width // 2 - container_width // 2
        container_y_position = self.screen_height // 2

        self.container = pygame.Rect(container_x_position, container_y_position, container_width, container_height)

        squares_total_width = sum(square_sizes) + 2 * 10
        squares_x_position = container_x_position + (container_width - squares_total_width) // 2

        self.squares = [
            pygame.Rect(squares_x_position, container_y_position, square_sizes[0], square_sizes[0]),
            pygame.Rect(squares_x_position + square_sizes[0] + 10, container_y_position, square_sizes[1], square_sizes[1]),
            pygame.Rect(squares_x_position + square_sizes[0] + square_sizes[1] + 20, container_y_position, square_sizes[2], square_sizes[2])
        ]

        self.current_square_index = 0
        self.square_change_interval = 200  # Increased the animation speed
        self.bounce_directions = [1, -1, 1]
        self.square_animation_started = True

    def animate_squares(self, screen):
        self.square_animation_elapsed += self.clock.tick(60)

        if self.square_animation_elapsed < self.square_animation_duration:
            self.square_change_interval -= 1
            if self.square_change_interval == 0:
                self.square_change_interval = 200  
                self.current_square_index = (self.current_square_index + 1) % len(self.squares)

            for i, square in enumerate(self.squares):
                square.width -= self.bounce_directions[i]
                square.height -= self.bounce_directions[i]

                if square.width > 36 or square.width < 10:
                    self.bounce_directions[i] *= -1

                pygame.draw.rect(screen, (217, 217, 217), square, border_radius=5)

        else:
            self.square_animation_started = False

    def is_finished(self, n):
        return (n == 1 and self.current_line >= len(self.lines) and not self.square_animation_started) or (n == 2 and self.current_line >= len(self.lines))

    def render(self, screen):
        while not self.is_finished(1):
            screen.fill((255, 255, 255))
            self.animate_lines(screen)
            if self.is_finished(2):
                self.square_animation_started = True
                self.animate_squares(screen)

            pygame.display.flip()
            self.clock.tick(60)

        return True