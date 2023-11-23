import pygame

class Text:
    def __init__(self, font, font_size):
        self.fontfamily = font
        self.size = font_size
        self.generate_font()

    def generate_font(self):
        self.font = pygame.font.Font(self.fontfamily, self.size)

    def render_text(self, text, color):
        return self.font.render(text, True, color)

    def change_font(self, font, font_size: None):
        self.fontfamily = font
        if font_size:
            self.size = font_size
