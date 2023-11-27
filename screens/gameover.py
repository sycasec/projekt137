import pygame

class GameOver:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title_font_size = 50


    def text(self, winner):
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), self.title_font_size)
        color_rgb = (224, 102, 102) if winner == "RED" else (102, 224, 102)

        color_surface = self.title_font.render(winner, True, color_rgb)

        wins_text = " WINS!"
        wins_surface = self.title_font.render(wins_text, True, (0, 0, 0))

        self.title_surface = pygame.Surface((color_surface.get_width() + wins_surface.get_width(), max(color_surface.get_height(), wins_surface.get_height())), pygame.SRCALPHA)
        self.title_surface.set_colorkey(None)
        self.title_surface.blit(color_surface, (0, 0))
        self.title_surface.blit(wins_surface, (color_surface.get_width(), 0))


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
        ):
            return "rematch"


    def render(self, screen, winner):
        self.text(winner)
        screen.fill((255, 255, 255))
        screen.blit(self.title_surface, self.title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2)))
        pygame.display.flip()
