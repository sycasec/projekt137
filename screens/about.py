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
            Lorem ipsum dolor sit amet consectetur. Nulla at aenean neque ipsum
            fringilla egestas. Nulla vitae varius hendrerit vitae dictum volutpat
            vivamus nunc. Mus etiam etiam ornare eget pretium tincidunt massa.
            Rutrum donec iaculis ultrices suspendisse feugiat. Lectus scelerisque
            dolor morbi tempor quis praesent netus elit id. Sit morbi habitant
            bibendum etiam. Ac consequat amet aliquam tempus viverra fermentum in.

            Est tortor et etiam consequat facilisis elementum lacinia feugiat.
            Eu tempor porttitor diam sed dignissim. Ultrices aliquam cras tincidunt
            sagittis libero eu pharetra nullam. Pretium fusce est et viverra nunc
            feugiat quis turpis. Eget platea quis vitae fringilla egestas amet.
            Nibh integer enim quam placerat commodo dictum adipiscing. Leo convallis
            malesuada aliquet congue aliquet sit. Volutpat nisi a mi facilisis dui
            vehicula risus arcu consequat. Arcu enim massa aenean id gravida. Donec
            tristique morbi commodo sagittis pretium ultricies tempor sed. Quis
            pretium vitae tempor orci congue erat.
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
