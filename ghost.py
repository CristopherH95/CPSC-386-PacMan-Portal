import pygame


class Ghost:
    """Represents the enemies of PacMan which chase him around the maze"""
    def __init__(self, screen, maze, target):
        self.screen = screen
        self.maze = maze
        self.target = target
        self.width, self.height = 10, 5
        self.image = pygame.Surface((self.height, self.width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = maze.ghost_spawn.pop()

    def blit(self):
        """Blit ghost image to the screen"""
        self.screen.blit(self.image, self.rect)
