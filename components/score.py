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

    def draw(self, screen):
        t_surf = self.font.render(str(self.value), True, self.color)
        t_rect = t_surf.get_rect(center=(self.x + self.score_rect_size // 2, self.y + self.score_rect_size // 2))
        screen.blit(t_surf, t_rect)

class ScoreHelper:
    red_color = pygame.Color(224,102,102) 
    green_color = pygame.Color(147,196,125)
    GREEN = "G"
    RED = "R"

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

    def draw(self, screen):
        for score in self.scores.values():
            score.draw(screen)
    