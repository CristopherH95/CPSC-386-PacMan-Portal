import pygame
from image_manager import ImageManager
from random import randrange


class Block(pygame.sprite.Sprite):
    """Represents a generic block in the maze"""
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image


class Maze:
    """Represents the maze displayed to the screen"""

    NEON_BLUE = (25, 25, 166)
    WHITE = (255, 255, 255)

    def __init__(self, screen, maze_map_file):
        self.screen = screen
        self.map_file = maze_map_file
        self.block_size = 20
        self.block_image = pygame.Surface((self.block_size, self.block_size))
        self.block_image.fill(Maze.NEON_BLUE)
        self.shield_image = pygame.Surface((self.block_size, self.block_size // 2))
        self.shield_image.fill(Maze.WHITE)
        self.pellet_image = pygame.Surface((self.block_size // 4, self.block_size // 4))
        pygame.draw.circle(self.pellet_image, Maze.WHITE,
                           (self.block_size // 8, self.block_size // 8), self.block_size // 8)
        self.fruit_image, _ = ImageManager('cherry.png', resize=(self.block_size // 2, self.block_size // 2)).get_image()
        with open(self.map_file, 'r') as file:
            self.map_lines = file.readlines()
        self.maze_blocks = pygame.sprite.Group()
        self.shield_blocks = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.player_spawn = None
        self.ghost_spawn = []
        self.build_maze()

    def build_maze(self):
        """Build the maze layout based on the maze map text file"""
        if self.maze_blocks:
            self.maze_blocks.empty()
        y_start = self.screen.get_height() // 12
        y = 0
        for i in range(len(self.map_lines)):
            line = self.map_lines[i]
            x_start = self.screen.get_width() // 5
            x = 0
            for j in range(len(line)):
                co = line[j]
                if co == 'x':
                    self.maze_blocks.add(Block(x_start + (x * self.block_size),
                                               y_start + (y * self.block_size),
                                               self.block_size, self.block_size,
                                               self.block_image))
                elif co == '*':
                    if randrange(0, 100) > 1:
                        self.pellets.add(Block(x_start + (self.block_size // 3) + (x * self.block_size),
                                               y_start + (self.block_size // 3) + (y * self.block_size),
                                               self.block_size, self.block_size,
                                               self.pellet_image))
                    else:
                        self.fruits.add(Block(x_start + (self.block_size // 4) + (x * self.block_size),
                                              y_start + (self.block_size // 4) + (y * self.block_size),
                                              self.block_size, self.block_size,
                                              self.fruit_image))
                elif co == 's':
                    self.shield_blocks.add(Block(x_start + (x * self.block_size),
                                                 y_start + (y * self.block_size),
                                                 self.block_size // 2, self.block_size // 2,
                                                 self.shield_image))
                elif co == 'o':
                    self.player_spawn = [(i, j), (x_start + (x * self.block_size) + (self.block_size // 2),
                                         y_start + (y * self.block_size) + (self.block_size // 2))]
                elif co == 'g':
                    self.ghost_spawn.append(((i, j), (x_start + (x * self.block_size) + (self.block_size // 2),
                                            y_start + (y * self.block_size) + (self.block_size // 2))))
                x += 1
            y += 1

    def remove_shields(self):
        """Remove any shields from the maze"""
        self.shield_blocks.empty()

    def blit(self):
        """Blit all maze blocks to the screen"""
        self.maze_blocks.draw(self.screen)
        self.pellets.draw(self.screen)
        self.fruits.draw(self.screen)
        self.shield_blocks.draw(self.screen)
