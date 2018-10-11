import pygame


class Ghost:
    """Represents the enemies of PacMan which chase him around the maze"""
    def __init__(self, screen, maze, target):
        self.screen = screen
        self.maze = maze
        self.internal_map = maze.map_lines
        self.target = target
        self.width, self.height = 10, 5
        self.image = pygame.Surface((self.height, self.width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        spawn_info = maze.ghost_spawn.pop()
        self.rect.centerx, self.rect.centery = spawn_info[1]
        self.tile = spawn_info[0]
        self.search = None
        self.direction = None
        self.speed = maze.block_size / 4

    def get_direction_options(self):
        """Check if the ghost is blocked by any maze barriers and return all directions possible to move in"""
        tests = {
            'u': self.rect.move((0, -self.rect.height)),
            'l': self.rect.move((-(self.rect.width * 2), 0)),
            'd': self.rect.move((0, self.rect.height)),
            'r': self.rect.move(((self.rect.width * 2), 0))
        }
        remove = []

        for wall in self.maze.maze_blocks:
            for d, t in tests.items():
                if wall.colliderect(t) and d not in remove:
                    remove.append(d)
        for rem in remove:
            del tests[rem]
        remove.clear()
        for wall in self.maze.shield_blocks:
            for d, t in tests.items():
                if wall.colliderect(t) and d not in remove:
                    remove.append(d)
        for rem in remove:
            del tests[rem]
        return tests.keys()

    def get_chase_direction(self):
        """Figure out a new direction to move in based on the target and walls"""
        options = self.get_direction_options()
        if self.target.rect.centery < self.rect.centery and 'u' in options:
            return 'u'  # target is up, and moving up is available
        if self.target.rect.centery < self.rect.centery and 'u' not in options:
            self.search = 'u'   # target is up, but can't move that way, search for next 'up'
            if 'l' in options:
                return 'l'      # try moving left
            if 'r' in options:
                return 'r'      # try moving right
            if 'd' in options:
                return 'd'  # try moving down
        if self.target.rect.centerx > self.rect.centerx and 'r' in options:
            return 'r'  # target is to the right, and moving right is available
        if self.target.rect.centerx > self.rect.centerx and 'r' not in options:
            self.search = 'r'   # target is to the right, but can't move that way, search for next 'right'
            if 'u' in options:
                return 'u'  # try moving up
            if 'd' in options:
                return 'd'  # try moving down
            if 'l' in options:
                return 'l'      # try moving left
        if self.target.rect.centerx < self.rect.centerx and 'l' in options:
            return 'l'  # target is to the left, and moving left is available
        if self.target.rect.centerx < self.rect.centerx and 'l' not in options:
            self.search = 'l'   # target is to the left, but can't move that way, search for next 'left'
            if 'u' in options:
                return 'u'  # try moving up
            if 'd' in options:
                return 'd'  # try moving down
            if 'r' in options:
                return 'r'      # try moving right
        if self.target.rect.centery > self.rect.centery and 'd' in options:
            return 'd'  # target is below, and moving down is available
        if self.target.rect.centery > self.rect.centery and 'd' not in options:
            self.search = 'd'   # target is below, but can't move that way, search for next 'down'
            if 'l' in options:
                return 'l'  # try moving left
            if 'r' in options:
                return 'r'  # try moving right
            if 'u' in options:
                return 'u'  # try moving up
        return None

    def recursive_find_move(self):
        """Recursively search for a path to the target, and return a move forward"""
        

    def get_nearest_col(self):
        """Get the current column location on the maze map"""
        return (self.rect.x - (self.screen.get_width() // 5)) // self.maze.block_size

    def get_nearest_row(self):
        """Get the current row location on the maze map"""
        return (self.rect.y - (self.screen.get_height() // 12)) // self.maze.block_size

    def update(self):
        """Update the ghost position"""
        # self.direction = self.get_chase_direction()
        if self.direction:
            options = self.get_direction_options()
            # print('options: ' + str(options))
            if self.search and self.search in options:
                self.direction = self.search
                self.search = None
            if self.direction == 'u' and 'u' in options:
                self.rect.centery -= self.speed
            elif self.direction == 'l' and 'l' in options:
                self.rect.centerx -= self.speed
            elif self.direction == 'd' and 'd' in options:
                self.rect.centery += self.speed
            elif self.direction == 'r' and 'r' in options:
                self.rect.centerx += self.speed
            else:
                self.direction = self.get_chase_direction()
            self.tile = (self.get_nearest_row(), self.get_nearest_col())

    def blit(self):
        """Blit ghost image to the screen"""
        self.screen.blit(self.image, self.rect)
