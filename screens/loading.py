import pygame
import sys
from components.inputbox import InputBox

class Waiting:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50
        self.title_spacing = 10
        
        self.ip_address_text_size = 20
        self.ip_address_spacing = 60
        self.ip_address_inputbox = None

        self.title()
        self.create_squares()
        
        self.ip_address_display(None, None)
        self.ip_input_box = InputBox(self.screen_width // 2 - 30, 
                                     self.screen_height // 2 - self.ip_address_spacing-9,
                                     155,
                                     18,
                                     self.ip_address_text_font)
        

    def title(self):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        title_text = "Waiting for other players"
        self.title_surface = self.title_font.render(title_text, True, "Black")
        
    def ip_address_display(self, client_type, ip_address):
        self.ip_address_text_font = pygame.font.Font(pygame.font.get_default_font(), self.ip_address_text_size)
        
        if client_type == "host" and ip_address != None:
            ip_address_text = "Your IP address is: " + ip_address
            self.ip_address_surface = self.ip_address_text_font.render(ip_address_text, True, "Black")
        elif client_type == "client":
            ip_address_text = "Enter the host's IP address:"
            self.ip_address_surface = self.ip_address_text_font.render(ip_address_text, True, "Black")
            
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
        self.ip_input_box.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return "assignment"
        
        
    def get_final_ip(self):
        if self.ip_input_box.final_text != '':
            return self.ip_input_box.final_text
        return None
        

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
    
    
    def render(self, screen, client_type, ip_address, event):
        self.ip_address_display(client_type, ip_address)
        
        screen.fill((255, 255, 255))
        screen.blit(self.title_surface, 
                    self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.title_spacing)))
        
        if client_type == "host":
            screen.blit(self.ip_address_surface, 
                        self.ip_address_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.ip_address_spacing)))
        elif client_type == "client":
            screen.blit(self.ip_address_surface, 
                        self.ip_address_surface.get_rect(center=(self.screen_width // 2 - 175, self.screen_height // 2 - self.ip_address_spacing)))
        
        if client_type == 'client':
            self.ip_input_box.render(screen)
            
        pygame.draw.rect(screen, (255, 255, 255), self.container)

        for i, square in enumerate(self.squares):
            pygame.draw.rect(screen, (217, 217, 217), square, border_radius=5)

        pygame.display.flip()
