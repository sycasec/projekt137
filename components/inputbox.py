import pygame

class InputBox:
    def __init__(self, x, y, w, h, text_font):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.color = "Black"
        self.rect_color = (217, 217, 217)
        self.text = ""
        self.text_font = text_font
        self.text_surface = self.text_font.render(self.text, True, self.color)
        self.last_input_time = 0
        self.final_text = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.final_text = self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.text_surface = self.text_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.text_surface.get_width()+10)
        self.rect.w = width

    def render(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.rect_color, self.rect.inflate(15, 15), border_radius=10)
        # Blit the text.
        screen.blit(self.text_surface, (self.x, self.y))
