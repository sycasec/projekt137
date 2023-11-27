import pygame
import sys

class Waiting:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50
        self.title_spacing = 10

        self.title()
        self.create_squares()

    def title(self):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        title_text = "Waiting for other players"
        self.title_surface = self.title_font.render(title_text, True, "Black")

    def create_squares(self):
        square_sizes = [36, 24, 18] 

        container_width = sum(square_sizes) + 2 * 10 
        container_height = max(square_sizes) 

        container_x_position = self.screen_width // 2 - container_width // 2
        container_y_position = self.screen_height // 2 + self.title_spacing + self.title_font_size // 2  # Adjusted to place the container below the title

        self.container = pygame.Rect(container_x_position, container_y_position, container_width, container_height)

        squares_total_width = sum(square_sizes) + 2 * 10  
        squares_x_position = container_x_position + (container_width - squares_total_width) // 2

        self.squares = [
            pygame.Rect(squares_x_position, container_y_position, square_sizes[0], square_sizes[0]),
            pygame.Rect(squares_x_position + square_sizes[0] + 10, container_y_position, square_sizes[1], square_sizes[1]),
            pygame.Rect(squares_x_position + square_sizes[0] + square_sizes[1] + 20, container_y_position, square_sizes[2], square_sizes[2])
        ]

        self.current_square_index = 0
        self.square_change_interval = 120 
        self.bounce_directions = [1, -1, 1] 

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return "assignment"

    def update(self):
        self.square_change_interval -= 1
        if self.square_change_interval == 0:
            self.square_change_interval = 120  # Reset the interval for slower changes
            self.current_square_index = (self.current_square_index + 1) % len(self.squares)

        for i, square in enumerate(self.squares):
            square.width -= self.bounce_directions[i]
            square.height -= self.bounce_directions[i]

            if square.width > 36 or square.width < 10:  # Adjusted the conditions
                self.bounce_directions[i] *= -1

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.title_surface,
                    self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.title_spacing)))

        pygame.draw.rect(screen, (255, 255, 255), self.container)

        for i, square in enumerate(self.squares):
            pygame.draw.rect(screen, (217, 217, 217), square, border_radius=5)

        pygame.display.flip()
