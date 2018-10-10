import pygame


class ScoreBoard:
    """Represents the score display for the screen"""

    SCORE_WHITE = (255, 255, 255)

    def __init__(self, screen, pos=(0, 0)):
        self.screen = screen
        self.score = 0
        self.color = ScoreBoard.SCORE_WHITE
        self.font = pygame.sysfont.SysFont(None, 36)
        self.image = None
        self.rect = None
        self.prep_image()
        self.pos = pos
        self.position()

    def position(self):
        """Re-position the scoreboard based on its pos value"""
        self.rect.centerx, self.rect.centery = self.pos

    def prep_image(self):
        """Render the score to a font image"""
        score_str = str(self.score)
        self.image = self.font.render(score_str, True, self.color)
        self.rect = self.image.get_rect()

    def update(self, n_score):
        """Increment the scoreboard and prepare a new image"""
        self.score += n_score
        self.prep_image()
        self.position()

    def blit(self):
        """Blit the score to the screen"""
        self.screen.blit(self.image, self.rect)
