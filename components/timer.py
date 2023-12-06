import pygame

class Timer:
    b_rad = 10
    timer_run_color = pygame.Color(224, 102, 102)
    timer_bg_color = pygame.Color(217, 217, 217)

    def __init__(self, x, y, width, max_time, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.max_time = max_time
        self.current_time = max_time
        self.font = font

    def update(self, dt):
        self.current_time -= dt
        if self.current_time < 0:
            self.current_time = 0

    def reset(self):
        self.current_time = self.max_time

    def is_done(self):
        return self.current_time <= 0

    def draw(self, surface):
        # Draw text
        text_surface = self.font.render("TIMER", True, (0, 0, 0))
        surface.blit(text_surface, (self.x , self.y))

        # Draw timer bar
        x = self.x + text_surface.get_width() + 20
        fill_width = int((self.current_time / self.max_time) * self.width)
        pygame.draw.rect(surface, self.timer_bg_color, (x, self.y, self.width, self.height), 0, self.b_rad)
        pygame.draw.rect(surface, self.timer_run_color, (x, self.y, fill_width, self.height), 0, self.b_rad)
