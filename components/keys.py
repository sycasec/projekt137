import pygame
import random

class Key:
    t_speed = 0.005
    t_duration = 100
    key_red_color = pygame.Color(224,102,102) 
    key_green_color = pygame.Color(147,196,125) 
    key_default_color = pygame.Color(199,199,199)
    key_rect_size = 60
    b_rad = 3 

    def __init__(self, assigned_key, coords, t_font):
        self.key = assigned_key
        self.x = coords[0]
        self.y = coords[1] 
        start_color = self.random_color()
        self.color = start_color
        self.target_color = start_color
        self.t_timer = 0
        self.font = t_font

    def toggle_red(self):
        self.target_color = self.key_red_color

    def toggle_green(self):
        self.target_color = self.key_green_color

    def toggle_default(self):
        self.target_color = self.key_default_color

    def random_color(self):
        return random.choice((self.key_red_color, self.key_green_color))

    def on_key_press(self):
        self.t_timer = pygame.time.get_ticks()
        # change when server-client logic added
        if self.target_color == self.key_default_color:
            self.toggle_green()
        if self.target_color == self.key_red_color:
            self.toggle_green() 
        if self.target_color == self.key_green_color:
            self.toggle_red()

    def update_color(self):
        elapsed_time = pygame.time.get_ticks() - self.t_timer

        if elapsed_time < self.t_duration:
            interpolation_factor = elapsed_time / self.t_duration 
            self.color = pygame.Color(
                int(pygame.math.lerp(
                    self.color.r, self.target_color.r, interpolation_factor)),
                int(pygame.math.lerp(
                    self.color.g, self.target_color.g, interpolation_factor)),
                int(pygame.math.lerp(
                    self.color.b, self.target_color.b, interpolation_factor))
            )

    def draw(self, screen):

        # render rounded rect
        pygame.draw.rect(screen, self.color,
            pygame.Rect(self.x, self.y, self.key_rect_size, self.key_rect_size), 
            0,
            self.b_rad
        )

        # render inner rectangle
        pygame.draw.rect(screen, self.color,
            pygame.Rect(self.x + self.b_rad, 
             self.y + self.b_rad, 
             self.key_rect_size - (2 * self.b_rad), 
             self.key_rect_size - (2 * self.b_rad)) 
        )

        t_surf = self.font.render(self.key, True, (255,255,255))
        t_rect = t_surf.get_rect(center=(self.x + self.key_rect_size // 2, self.y + self.key_rect_size//2))
        screen.blit(t_surf, t_rect)


class KeyHelper:
    def __init__(self, keys_font):
        self.top_row = "QWERTYUIOP"
        self.mid_row = "ASDFGHJKL"
        self.bot_row = "ZXCVBNM"
        self.y_vals = [420,495,570]
        self.x_vals = [145,190,265]
        self.x_inc = 85
        self.font = keys_font
        self.keys_dict = {}

    def gen_key_row(self, row):
        kd = {}
        sel_row = self.top_row

        if row == 1:
            sel_row = self.mid_row
        elif row == 2:
            sel_row = self.bot_row

        c_x = self.x_vals[row]

        for char in sel_row:
            key_code = pygame.K_a + (ord(char.upper()) - ord('A'))
            kd[key_code] = Key(char, (c_x, self.y_vals[row]), self.font)
            c_x += self.x_inc

        return kd

    def gen_keys(self):
        for i in range(0,3):
            self.keys_dict.update(self.gen_key_row(i))

    def get_keys(self):
        return self.keys_dict
    
    def get_key_colors(self):
        """Generates a string representing the colors of all 26 keys on the keyboard

        R = red
        G = green
        D = default

        Returns:
            string: 26-character long string of colors
        """
        result = ""
        for letter in range(pygame.K_a, pygame.K_z + 1):
            key = self.keys_dict[letter]
            if key.target_color == Key.key_red_color:
                color = "R"
            elif key.target_color == Key.key_green_color:
                color = "G"
            else:
                color = "D"
            result += color
        return result

    def set_key_colors_from_string(self, s):
        """Takes a 26-letter string consisting of "R", and "G", then updates the keyboard colors to match the string


        Args:
            s (str): 26-letter string representing the color of each letter in alphabetical order
        """
        for i in range(len(s)):
            key = self.keys_dict[pygame.K_a + i]
            key.t_timer = pygame.time.get_ticks() # IDK what this line does but if you remove it, the colors don't change
            char = s[i]
            if char == "R":
                key.toggle_red()
            elif char == "G":
                key.toggle_green()
            else:
                key.toggle_default()

