import pygame


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
        self.pellet_image = pygame.Surface((self.block_size // 2, self.block_size // 2))
        pygame.draw.circle(self.pellet_image, Maze.WHITE,
                           (self.block_size // 4, self.block_size // 4), self.block_size // 4)
        with open(self.map_file, 'r') as file:
            self.map_lines = file.readlines()
        self.maze_blocks = []
        self.shield_blocks = []
        self.pellets = []
        self.player_spawn = None
        self.ghost_spawn = []
        self.build_maze()

    def build_maze(self):
        """Build the maze layout based on the maze map text file"""
        if self.maze_blocks:
            self.maze_blocks.clear()
        y_start = self.screen.get_height() // 12
        y = 0
        for line in self.map_lines:
            x_start = self.screen.get_width() // 5
            x = 0
            for co in line:
                if co == 'x':
                    self.maze_blocks.append(pygame.Rect(x_start + (x * self.block_size),
                                                        y_start + (y * self.block_size),
                                                        self.block_size, self.block_size))
                elif co == '*':
                    self.pellets.append(pygame.Rect(x_start + (self.block_size // 4) + (x * self.block_size),
                                                    y_start + (self.block_size // 4) + (y * self.block_size),
                                                    self.block_size, self.block_size))
                elif co == 's':
                    self.shield_blocks.append(pygame.Rect(x_start + (x * self.block_size),
                                                          y_start + (y * self.block_size),
                                                          self.block_size // 2, self.block_size // 2))
                elif co == 'o':
                    self.player_spawn = (x_start + (x * self.block_size) + (self.block_size // 2),
                                         y_start + (y * self.block_size) + (self.block_size // 2))
                elif co == 'g':
                    self.ghost_spawn.append((x_start + (x * self.block_size) + (self.block_size // 2),
                                            y_start + (y * self.block_size) + (self.block_size // 2)))
                x += 1
            y += 1

    def remove_shields(self):
        """Remove any shields from the maze"""
        self.shield_blocks.clear()

    def blit(self):
        """Blit all maze blocks to the screen"""
        for block in self.maze_blocks:
            self.screen.blit(self.block_image, block)
        for pellet in self.pellets:
            self.screen.blit(self.pellet_image, pellet)
        for block in self.shield_blocks:
            self.screen.blit(self.shield_image, block)
