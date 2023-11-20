import pygame

class Key:
    t_speed = 0.005
    t_duration = 1000
    key_red_color = pygame.Color(224,102,102) 
    key_green_color = pygame.Color(147,196,125) 
    key_default_color = pygame.Color(199,199,199)
    key_rect_size = 50


    def __init__(self, assigned_key, coords):
        self.key = assigned_key
        self.x = coords[0]
        self.y = coords[1] 
        self.color = self.key_default_color
        self.target_color = self.key_default_color
        self.t_timer = 0

    def toggle_red(self):
        self.target_color = self.key_red_color

    def toggle_green(self):
        self.target_color = self.key_green_color

    def on_key_press(self):
        self.t_timer = pygame.time.get_ticks()
        # change when server-client logic added
        if self.color == self.key_default_color:
            self.toggle_green()
        if self.color.r == self.key_red_color.r or self.color.g == self.key_red_color.g or self.color.b == self.key_red_color.b:
            self.toggle_green() 
        if self.color.r == self.key_green_color.r or self.color.g == self.key_green_color.g or self.color.b == self.key_green_color.b:
            self.toggle_red()

    def update_color(self):
        elapsed_time = pygame.time.get_ticks() - self.t_timer

        if elapsed_time < self.t_duration:
            interpolation_factor = elapsed_time / self.t_duration 
            self.color = pygame.Color(
                int(pygame.math.lerp(self.color.r, self.target_color.r, interpolation_factor)),
                int(pygame.math.lerp(self.color.g, self.target_color.g, interpolation_factor)),
                int(pygame.math.lerp(self.color.b, self.target_color.b, interpolation_factor))
            )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.key_rect_size, self.key_rect_size))


