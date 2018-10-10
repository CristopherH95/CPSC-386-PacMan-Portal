import pygame


class PacMan(pygame.sprite.Sprite):
    """Represents the player character 'PacMan' and its related logic/control"""
    PAC_YELLOW = (255, 255, 0)

    def __init__(self, screen, maze):
        super().__init__()
        self.screen = screen
        self.radius = 5
        self.maze = maze
        self.direction = None
        self.speed = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.maze.player_spawn
        pygame.draw.circle(self.image, PacMan.PAC_YELLOW, (self.radius, self.radius), self.radius)

        # Keyboard related events/actions/releases
        self.event_map = {pygame.KEYDOWN: self.change_direction, pygame.KEYUP: self.reset_direction}
        self.action_map = {pygame.K_UP: self.set_move_up, pygame.K_LEFT: self.set_move_left,
                           pygame.K_DOWN: self.set_move_down, pygame.K_RIGHT: self.set_move_right}

    def reset_direction(self, event):
        """Reset the movement direction if key-up on movement keys"""
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            self.direction = None

    def change_direction(self, event):
        """Change direction based on the event key"""
        if event.key in self.action_map:
            self.action_map[event.key]()

    def set_move_up(self):
        """Set move direction up"""
        self.direction = 'u'

    def set_move_left(self):
        """Set move direction left"""
        self.direction = 'l'

    def set_move_down(self):
        """Set move direction down"""
        self.direction = 'd'

    def set_move_right(self):
        """Set move direction to right"""
        self.direction = 'r'

    def is_blocked(self):
        """Check if PacMan is blocked by any maze barriers, return True if blocked, False if clear"""
        if self.direction is not None:
            if self.direction == 'u':
                test = self.rect.move((0, -(self.radius * 2)))
            elif self.direction == 'l':
                test = self.rect.move((-(self.radius * 2), 0))
            elif self.direction == 'd':
                test = self.rect.move((0, (self.radius * 2)))
            else:
                test = self.rect.move(((self.radius * 2), 0))

            for wall in self.maze.maze_blocks:
                if wall.colliderect(test):
                    return True
            for wall in self.maze.shield_blocks:
                if wall.colliderect(test):
                    return True
        return False

    def update(self):
        """Update PacMan's position in the maze if moving, and if not blocked"""
        if self.direction:
            if not self.is_blocked():
                if self.direction == 'u':
                    self.rect.top -= self.speed
                elif self.direction == 'l':
                    self.rect.left -= self.speed
                elif self.direction == 'd':
                    self.rect.bottom += self.speed
                elif self.direction == 'r':
                    self.rect.right += self.speed

    def blit(self):
        """Blit the PacMan sprite to the screen"""
        self.screen.blit(self.image, self.rect)

    def eat_pellets(self):
        """Eat pellets from the maze and return the score accumulated"""
        score = 0
        pellets_left = []
        for pellet in self.maze.pellets:
            if not pellet.colliderect(self.rect):
                pellets_left.append(pellet)
            else:
                score += 10
        self.maze.pellets = pellets_left
        return score