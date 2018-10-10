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
        self.rect.centerx, self.rect.centery = maze.ghost_spawn.pop()
        self.destination = None
        self.direction = None
        self.speed = 4

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

    def get_new_direction(self):
        """Figure out a new direction to move in based on the target and walls"""
        options = self.get_direction_options()
        if self.target.rect.y < self.rect.y and 'u' in options:
            return 'u'
        if self.target.rect.x > self.rect.x and 'r' in options:
            return 'r'
        if self.target.rect.x < self.rect.x and 'l' in options:
            return 'l'
        if self.target.rect.y > self.rect.y and 'd' in options:
            return 'd'
        return None

    def update(self):
        """Update the ghost position"""
        self.direction = self.get_new_direction()
        if self.direction:
            if self.direction == 'u':
                self.rect.top -= self.speed
            elif self.direction == 'l':
                self.rect.left -= self.speed
            elif self.direction == 'd':
                self.rect.bottom += self.speed
            elif self.direction == 'r':
                self.rect.right += self.speed

    def blit(self):
        """Blit ghost image to the screen"""
        self.screen.blit(self.image, self.rect)
