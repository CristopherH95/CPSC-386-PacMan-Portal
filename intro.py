import pygame
from image_manager import ImageManager
from score import ScoreBoard


class SimpleAnimation(pygame.sprite.Sprite):
    """A class for presenting a basic animation with little to no special logic"""
    def __init__(self, screen, sprite_sheet, sheet_offsets, pos=(0, 0), resize=None, detail=None, frame_delay=None):
        super().__init__()
        self.screen = screen
        if not resize:
            resize = (self.screen.get_height() // 10, self.screen.get_height() // 10)
        self.image_manager = ImageManager(sprite_sheet, sheet=True, pos_offsets=sheet_offsets,
                                          resize=resize, animation_delay=frame_delay)
        self.image, self.rect = self.image_manager.get_image()
        if detail:
            self.detail_piece = ImageManager(detail, sheet=True, pos_offsets=sheet_offsets,
                                             resize=resize).all_images()[0]     # grab first image in detail sheet
            self.image.blit(self.detail_piece, (0, 0))  # combine detail
        self.rect.centerx, self.rect.centery = pos

    def update(self):
        """Update to the next image in the animation"""
        self.image = self.image_manager.next_image()
        self.image.blit(self.detail_piece, (0, 0))     # combine detail

    def blit(self):
        """Blit the current image to the screen"""
        self.screen.blit(self.image, self.rect)


class TitleCard(pygame.sprite.Sprite):
    """Displays a single line of text as a large title card"""
    def __init__(self, screen, text,  pos=(0, 0), color=ScoreBoard.SCORE_WHITE, size=42):
        super().__init__()
        self.screen = screen
        self.text = text
        self.color = color
        self.font = pygame.font.Font('fonts/LuckiestGuy-Regular.ttf', size)
        self.image = None
        self.rect = None
        self.pos = pos
        self.prep_image()

    def position(self, n_pos=None):
        """set the position of the title card"""
        if not n_pos:
            self.rect.centerx, self.rect.centery = self.pos
        else:
            self.rect.centerx, self.rect.centery = n_pos

    def prep_image(self):
        """Render the text as an image to be displayed"""
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.position()

    def blit(self):
        """Blit the title card to the screen"""
        self.screen.blit(self.image, self.rect)


class GhostIntro:
    """Displays an introduction title card and sprite for a given ghost"""
    def __init__(self, screen, g_file, name):
        self.screen = screen
        self.title_card = TitleCard(screen, name, pos=(screen.get_width() // 2, screen.get_height() // 2))
        self.ghost = SimpleAnimation(screen, g_file, sheet_offsets=[(0, 0, 32, 32), (0, 32, 32, 32)],
                                     pos=(self.title_card.rect.right + self.title_card.rect.width // 2,
                                          screen.get_height() // 2),
                                     detail='ghost-eyes.png',
                                     frame_delay=150)

    def update(self):
        """Update ghost animations in title card"""
        self.ghost.update()

    def blit(self):
        """Blit the components of the ghost intro to the screen"""
        self.title_card.blit()
        self.ghost.blit()


class Intro:
    """Handles the display and continuation of an introductory cut-scene"""
    def __init__(self, screen):
        self.screen = screen
        self.ghost_intros = [
            GhostIntro(screen, 'ghost-red.png', 'Blinky'),
            GhostIntro(screen, 'ghost-pink.png', 'Pinky'),
            GhostIntro(screen, 'ghost-lblue.png', 'Inky'),
            GhostIntro(screen, 'ghost-orange.png', 'Clyde')
        ]
        self.intro_index = 0
        self.last_intro_start = None
        self.intro_time = 5000  # time to display in milliseconds

    def update(self):
        """Progress the intro sequence"""
        if not self.last_intro_start:
            self.last_intro_start = pygame.time.get_ticks()
        elif abs(self.last_intro_start - pygame.time.get_ticks()) > self.intro_time:
            self.intro_index = (self.intro_index + 1) % len(self.ghost_intros)
            self.last_intro_start = pygame.time.get_ticks()
        self.ghost_intros[self.intro_index].update()

    def blit(self):
        """Blit the intro sequence to the screen"""
        self.ghost_intros[self.intro_index].blit()
