import pygame


class Maze:
    """Represents the maze displayed to the screen"""

    NEON_BLUE = (25, 25, 166)
    SHIELD_WHITE = (255, 255, 255)

    def __init__(self, screen, maze_map_file):
        self.screen = screen
        self.map_file = maze_map_file
        self.block_size = 10
        self.block_image = pygame.Surface((self.block_size, self.block_size))
        self.block_image.fill(Maze.NEON_BLUE)
        self.shield_image = pygame.Surface((self.block_size, self.block_size // 2))
        self.shield_image.fill(Maze.SHIELD_WHITE)
        with open(self.map_file, 'r') as file:
            self.map_lines = file.readlines()
        self.maze_blocks = []
        self.shield_blocks = []
        self.build_maze()

    def build_maze(self):
        """Build the maze layout based on the maze map text file"""
        if self.maze_blocks:
            self.maze_blocks.clear()
        y = 0
        for line in self.map_lines:
            x = 0
            for co in line:
                if co == 'x':
                    self.maze_blocks.append(pygame.Rect(x * self.block_size, y * self.block_size,
                                                        self.block_size, self.block_size))
                elif co == 's':
                    self.shield_blocks.append(pygame.Rect(x * self.block_size, y * self.block_size,
                                                          self.block_size // 2, self.block_size // 2))
                x += 1
            y += 1

    def blit(self):
        """Blit all maze blocks to the screen"""
        for block in self.maze_blocks:
            self.screen.blit(self.block_image, block)
        for block in self.shield_blocks:
            self.screen.blit(self.shield_image, block)
