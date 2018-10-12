import json
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


class ItemCounter:
    """Displays a count of the number of a given item image to the screen"""
    def __init__(self, screen, image_name, pos=(0, 0)):
        self.screen = screen
        self.counter = 0
        self.item_image = pygame.image.load('images/' + image_name)
        self.item_rect = self.item_image.get_rect()
        self.font = pygame.sysfont.SysFont(None, 36)
        self.color = ScoreBoard.SCORE_WHITE
        self.text_image = None
        self.text_rect = None
        self.pos = pos
        self.prep_image()

    def add_items(self, n_items):
        """Increment the item counter by the given number of items"""
        self.counter += n_items
        self.prep_image()

    def prep_image(self):
        """Render the counter's image for future display"""
        text = str(self.counter) + ' X '
        self.text_image = self.font.render(text, True, self.color)
        self.text_rect = self.text_image.get_rect()
        self.position()

    def position(self):
        """Resets the position of the item counter to its stored position"""
        self.text_rect.centerx, self.text_rect.centery = self.pos
        x_offset = int(self.text_rect.width * 1.5)
        self.item_rect.centerx, self.item_rect.centery = self.pos[0] + x_offset, self.pos[1]

    def blit(self):
        """Blit the counter to the screen"""
        self.screen.blit(self.text_image, self.text_rect)
        self.screen.blit(self.item_image, self.item_rect)


class ScoreController:
    """Handles scoring and representation of scores"""
    def __init__(self, screen, items_image, sb_pos=(0, 0), itc_pos=(0, 0)):
        self.score = 0
        self.high_scores = []
        self.scoreboard = ScoreBoard(screen=screen, pos=sb_pos)
        self.item_counter = ItemCounter(screen=screen, pos=itc_pos, image_name=items_image)

    def add_score(self, score, items=None):
        """Add new score and prepare for scoreboard display"""
        self.scoreboard.update(score)
        self.score = self.scoreboard.score
        if items:
            self.item_counter.add_items(items)

    def blit(self):
        """Blit all score related displays to the screen"""
        self.scoreboard.blit()
        self.item_counter.blit()

    def init_high_scores(self):
        """Read saved high scores from local storage"""
        try:
            with open('score_data.json', 'r') as file:
                self.high_scores = json.load(file)
                self.high_scores.sort(reverse=True)
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError) as e:
            print(e)
            self.high_scores = [0, 0, 0, 0, 0]

    def save_high_scores(self):
        """Save high scores to the disk"""
        for i in range(len(self.high_scores)):
            if self.score >= self.high_scores[i]:
                self.high_scores[i] = self.score
                break
        with open('score_data.json', 'w') as file:
            json.dump(self.high_scores, file)
