import pygame
import sys

class HomeScreen:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50
        self.button_font_size = 24
        self.button_spacing = 40  
        self.title_spacing = 50 
        self.selected_button = 0
        #self.bg_music = pygame.mixer.Sound('assets/sounds/bg.mp3')
        self.button_click = pygame.mixer.Sound("assets/sounds/buttonclick.mp3")
        self.button_nav = pygame.mixer.Sound("assets/sounds/buttonnav.mp3")
    
        self.title()
        self.menu()

    def title(self):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)  
        title_text = "KEYBOARD SPLATOON"
        self.title_surface = self.title_font.render(title_text, True, "Black")
       
    def menu(self):
        self.button_font = pygame.font.Font(pygame.font.get_default_font(), self.button_font_size)
        self.buttons = ["Initialize game", "Join a game", "About", "Quit"]
        self.button_surfaces = [self.button_font.render(button, True, "Black") for button in self.buttons]
        title_rect = self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.title_spacing))
        self.button_rects = [surface.get_rect(topleft=(title_rect.left + 50, title_rect.bottom + i * self.button_spacing + 16)) for i, surface in enumerate(self.button_surfaces)]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(event.pos):
                        self.button_click.play()
                        return i
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.button_nav.play() 
                self.select_button(1)
            elif event.key == pygame.K_UP:
                self.button_nav.play() 
                self.select_button(-1)
            elif event.key == pygame.K_RETURN:
                self.button_click.play()
                return self.selected_button

    def select_button(self, dir):
        self.selected_button = (self.selected_button + dir) % len(self.buttons)

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - self.title_spacing)))

        for i, (rect, surface) in enumerate(zip(self.button_rects, self.button_surfaces)):
            if i == self.selected_button:
                enlarged_rect = rect.inflate(15, 15)
                pygame.draw.rect(screen, (217, 217, 217), enlarged_rect, border_radius=10)

            screen.blit(surface, rect)

        pygame.display.flip()
