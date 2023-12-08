import pygame

class Score:
    score_rect_size = 30
    def __init__(self, color, coords, t_font, value = 0):
        self.value = value
        self.x, self.y = coords
        self.color = color
        self.font = t_font

    def add_score(self, new_value):
        self.value += new_value

    def draw(self, screen, is_player, multiplier):
        
        if is_player:
            # set necessary shit for multipliers
            multiplier_str = 'x' + str(multiplier)
            mult_font = pygame.font.Font(pygame.font.get_default_font(), 15 + 5*multiplier) # bigger multiplier, larger font
            mult_surf = mult_font.render(multiplier_str, True, "White")
            mult_rect = mult_surf.get_rect(center=(self.x-27-2*multiplier, self.y-20-2*multiplier))
            
            t_surf = self.font.render(str(self.value), True, "White")
            rect_surf = pygame.Rect(self.x-35, self.y-13, 100, 50)        
            
            # Draw surfaces
            pygame.draw.rect(screen, self.color, rect_surf.inflate(15, 15), border_radius=10)
            
            pygame.draw.circle(screen, "White", (self.x-27-2*multiplier, self.y-20-2*multiplier), 25 + 3*multiplier)
            pygame.draw.circle(screen, self.color, (self.x-27-2*multiplier, self.y-20-2*multiplier), 20 + 3*multiplier)
            
            screen.blit(mult_surf, mult_rect)
            
        else:
            t_surf = self.font.render(str(self.value), True, self.color)
            
        t_rect = t_surf.get_rect(center=(self.x + self.score_rect_size // 2, self.y + self.score_rect_size // 2))
        screen.blit(t_surf, t_rect)

    def __gt__(self,other):
        return self.value > other.value

class ScoreHelper:
    red_color = pygame.Color(224,102,102)
    green_color = pygame.Color(147,196,125)
    GREEN = "G"
    RED = "R"
    TIE = "D"

    def __init__(self, score_font):
        self.font = score_font
        self.x_center = 562 # coordinate for CENTER of the scores, NOT the left
        self.y_val = 300
        self.x_inc = 100
        self.scores = self.gen_scores()

    def add_score(self, player, amount=10):
        self.scores[player].add_score(amount)

    def gen_scores(self):
        x = self.x_center - self.x_inc
        y = self.y_val

        scores = {}
        scores[self.GREEN] = Score(self.green_color, (x, y), self.font)
        x += self.x_inc
        scores[self.RED] = Score(self.red_color, (x, y), self.font)

        return scores

    def get_scores(self):
        return self.scores

    def set_score(self, player, value):
        if player not in [self.GREEN, self.RED]:
            return False
        self.scores[player].value = value

    def reset_scores(self):
        for player in self.scores:
            self.scores[player].value = 0

    def publish_winner(self):
        if self.scores[self.GREEN] > self.scores[self.RED]:
            return self.GREEN
        elif self.scores[self.RED] > self.scores[self.GREEN]:
            return self.RED
        else:
            return self.TIE

    def draw(self, screen, player, multiplier):
        player = player[0]
        for key, score in self.scores.items():
            score.draw(screen, is_player = key==player, multiplier=multiplier)
