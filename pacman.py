import pygame
from spritesheet import extract_images


class PacMan(pygame.sprite.Sprite):
    """Represents the player character 'PacMan' and its related logic/control"""
    PAC_YELLOW = (255, 255, 0)

    def __init__(self, screen, maze):
        super().__init__()
        self.screen = screen
        self.radius = 5
        self.maze = maze
        s_sheet = extract_images('pacman.png', [(0, 0, 191, 191), (192, 0, 191, 191),
                                                (0, 192, 191, 191), (192, 192, 192, 192)])
        s_sheet = [pygame.transform.scale(img, (self.maze.block_size, self.maze.block_size)) for img in s_sheet]
        self.spawn_info = self.maze.player_spawn[1]
        self.tile = self.maze.player_spawn[0]
        self.direction = None
        self.speed = maze.block_size / 4    # move one brick at a time
        # self.image = pygame.Surface((self.maze.block_size, self.maze.block_size), pygame.SRCALPHA, 32)
        self.images = s_sheet
        self.image_index = 0
        self.image = s_sheet[self.image_index]
        # self.image = pygame.Surface.convert_alpha(self.image)   # ensure the background is invisible
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.spawn_info   # screen coordinates for spawn
        # pygame.draw.circle(self.image, PacMan.PAC_YELLOW,
        #                    (self.maze.block_size // 2, self.maze.block_size // 2), self.radius)

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

    def get_nearest_col(self):
        """Get the current column location on the maze map"""
        return (self.rect.x - (self.screen.get_width() // 5)) // self.maze.block_size

    def get_nearest_row(self):
        """Get the current row location on the maze map"""
        return (self.rect.y - (self.screen.get_height() // 12)) // self.maze.block_size

    def is_blocked(self):
        """Check if PacMan is blocked by any maze barriers, return True if blocked, False if clear"""
        if self.direction is not None:
            if self.direction == 'u':
                test = self.rect.move((0, -self.speed))
            elif self.direction == 'l':
                test = self.rect.move((-self.speed, 0))
            elif self.direction == 'd':
                test = self.rect.move((0, self.speed))
            else:
                test = self.rect.move((self.speed, 0))

            for wall in self.maze.maze_blocks:
                if wall.colliderect(test):
                    return True
            for wall in self.maze.shield_blocks:
                if wall.colliderect(test):
                    return True
        return False

    def update(self):
        """Update PacMan's position in the maze if moving, and if not blocked"""
        if self.direction:  # TODO: convert direction to utilize tiles for AI
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            if not self.is_blocked():
                if self.direction == 'u':
                    self.rect.centery -= self.speed
                elif self.direction == 'l':
                    self.rect.centerx -= self.speed
                elif self.direction == 'd':
                    self.rect.centery += self.speed
                elif self.direction == 'r':
                    self.rect.centerx += self.speed
            self.tile = (self.get_nearest_row(), self.get_nearest_col())

    def blit(self):
        """Blit the PacMan sprite to the screen"""
        self.screen.blit(self.image, self.rect)

    def eat(self):
        """Eat pellets from the maze and return the score accumulated"""
        score = 0
        fruit_count = 0
        pellets_left = []
        fruit_left = []
        for pellet in self.maze.pellets:
            if not pellet.colliderect(self.rect):
                pellets_left.append(pellet)
            else:
                score += 10
        for fruit in self.maze.fruits:
            if not fruit.colliderect(self.rect):
                fruit_left.append(fruit)
            else:
                score += 20
                fruit_count += 1
        self.maze.pellets = pellets_left
        self.maze.fruits = fruit_left
        return score, fruit_count
