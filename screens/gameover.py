import pygame

class GameOver:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50
        self.home_button_rect = pygame.Rect(20, 20, 250, 40)
        self.rematch_button_rect = pygame.Rect( screen_width // 2 - 75, screen_height // 2 + 30, 150,40)

    def buttons(self, screen):
        button_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        
        home_button_text = button_font.render("Back to Home screen", True, "Black")
        rematch_button_text = button_font.render("Rematch", True, "Black")
        
        home_button_text_x = self.home_button_rect.x + (self.home_button_rect.width - home_button_text.get_width()) // 2
        home_button_text_y = self.home_button_rect.y + (self.home_button_rect.height - home_button_text.get_height()) // 2
        
        rematch_button_text_x = self.rematch_button_rect.x + (self.rematch_button_rect.width - rematch_button_text.get_width()) // 2
        rematch_button_text_y = self.rematch_button_rect.y + (self.rematch_button_rect.height - rematch_button_text.get_height()) // 2
        
        pygame.draw.rect(screen, (217, 217, 217), self.home_button_rect, border_radius=10)
        screen.blit(home_button_text, (home_button_text_x, home_button_text_y))
        
        pygame.draw.rect(screen, (217,217,217), self.rematch_button_rect, border_radius=10)
        screen.blit(rematch_button_text, (rematch_button_text_x, rematch_button_text_y))

    def text(self, winner):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        self.win_lose_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        
        if winner == "TIE":
            color_rgb = (199 ,199 ,199)
            wins_text = "!"
        else:
            color_rgb = (224, 102, 102) if winner == "RED" else (102, 224, 102)
            wins_text = " WINS!"
        
        color_surface = self.title_font.render(winner, True, color_rgb)
        wins_surface = self.title_font.render(wins_text, True, (0, 0, 0))

        self.title_surface = pygame.Surface((color_surface.get_width() + wins_surface.get_width(), max(color_surface.get_height(), wins_surface.get_height())), pygame.SRCALPHA)
        self.title_surface.set_colorkey(None)
        self.title_surface.blit(color_surface, (0, 0))
        self.title_surface.blit(wins_surface, (color_surface.get_width(), 0))


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rematch_button_rect.colliderect(pygame.Rect(event.pos, (1, 1)))) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            return "rematch"
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.home_button_rect.colliderect(pygame.Rect(event.pos, (1, 1)))) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "home"

    def render(self, screen, winner):
        self.text(winner)
        screen.fill((255, 255, 255))
        
        self.buttons(screen)
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2)))
        pygame.display.flip()
