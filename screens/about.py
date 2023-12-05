import pygame

class AboutScreen:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

        self.containers()
        self.fonts()
        self.text_content()

    def containers(self):
        margin_size = 100

        left_container_width = (4 * (self.screen_width - 2 * margin_size)) // 6
        right_container_width = (2 * (self.screen_width - 2 * margin_size)) // 6

        self.left_container_rect = pygame.Rect(margin_size, margin_size, left_container_width, self.screen_height - 2 * margin_size)
        self.right_container_rect = pygame.Rect(margin_size + left_container_width + margin_size, margin_size, right_container_width, self.screen_height - 2 * margin_size)

        self.back_button_rect = pygame.Rect(20, 20, 100, 40)

    def fonts(self):
        default_font = pygame.font.get_default_font()
        self.title_font = pygame.font.Font(default_font, 42)
        self.text_font = pygame.font.Font(default_font, 16)
        self.developers_title_font = pygame.font.Font(default_font, 30)
        self.developers_text_font = pygame.font.Font(default_font, 12)

    def text_content(self):
        self.title_text = "ABOUT KEYBOARD SPLATOON"
        self.about_text = """
            Keyboard Splatoon is a multiplayer keyboard-based game where players try 
            to “paint” the game’s keyboard in their color before the opponent can do 
            the same 

            Mechanics:
            Each player sees a keyboard where each key is either red or green. 
            When a player presses a key, that key will toggle its color. 

            Win Conditions/Scoring System:
            Whenever a key turns into a player’s color, that player gets 10 points 
            (i.e. if the green player turns a red key into green, they get 10 points). 
            Pressing multiple keys successively with no mistakes adds a combo 
            multiplier up to 5x points. Player 1’s goal is to make all keys green, 
            and player 2’s goal is to make all keys red. If one player succeeds, they 
            automatically win. If no player succeeds after 10 seconds, the player with 
            the highest score wins. 

	        If one player manages to cover the entire keyboard in their respective color, 
            they immediately win. If no player succeeds in this after 10 seconds, the 
            player with the highest score wins instead.

        """
        self.developers_title_y_offset = 30
        self.developers_text = "  del Castillo, Kyle Adrian\n  Dy, Alwyn\n  Gudito, Justine\n  Modequillo, Jethro\n  Pilpa, Myka Jean\n  Tupa, Sam Bondj\n  Ypanto, Goody Carlo"

        self.title_surface = self.title_font.render(self.title_text, True, "Black")
        self.about_lines = [self.text_font.render(line, True, "Black") for line in self.about_text.split('\n')]
        self.developers_title_surface = self.developers_title_font.render("THE TEAM", True, "Black")
        self.developers_lines = [self.developers_text_font.render(line, True, "Black") for line in self.developers_text.split('\n')]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.back_button_rect.colliderect(pygame.Rect(event.pos, (1, 1))):
            return "back"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def render(self, screen):
        screen.fill((255, 255, 255))

        screen.blit(self.title_surface, (self.left_container_rect.x + 20, self.left_container_rect.y + 20))

        y_offset = 70
        for about_surface in self.about_lines:
            screen.blit(about_surface, (self.left_container_rect.x + 10, self.left_container_rect.y + y_offset))
            y_offset += self.text_font.get_height() + 5

        pygame.draw.rect(screen, (255, 255, 255), self.right_container_rect)

        screen.blit(self.developers_title_surface, (self.right_container_rect.x+10, self.right_container_rect.y + self.developers_title_y_offset))

        y_offset = self.developers_title_y_offset + 40
        for developers_surface in self.developers_lines:
            screen.blit(developers_surface, (self.right_container_rect.x + 20, self.right_container_rect.y + y_offset))
            y_offset += self.text_font.get_height()

        pygame.draw.rect(screen, (217, 217, 217), self.back_button_rect, border_radius=10)

        back_button_text = self.text_font.render("Back", True, "Black")
        text_x = self.back_button_rect.x + (self.back_button_rect.width - back_button_text.get_width()) // 2
        text_y = self.back_button_rect.y + (self.back_button_rect.height - back_button_text.get_height()) // 2
        screen.blit(back_button_text, (text_x, text_y))
