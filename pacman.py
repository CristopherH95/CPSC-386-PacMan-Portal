import pygame
from image_manager import ImageManager


class PacMan(pygame.sprite.Sprite):
    """Represents the player character 'PacMan' and its related logic/control"""
    PAC_YELLOW = (255, 255, 0)

    def __init__(self, screen, maze):
        super().__init__()
        self.screen = screen
        self.radius = 5
        self.maze = maze
        self.horizontal_images = ImageManager('pacman-horiz.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                           (32, 0, 32, 32),
                                                                                           (0, 32, 32, 32),
                                                                                           (32, 32, 32, 32),
                                                                                           (0, 64, 32, 32)],
                                              resize=(self.maze.block_size, self.maze.block_size),
                                              reversible=True)
        self.vertical_images = ImageManager('pacman-vert.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                        (32, 0, 32, 32),
                                                                                        (0, 32, 32, 32),
                                                                                        (32, 32, 32, 32),
                                                                                        (0, 64, 32, 32)],
                                            resize=(self.maze.block_size, self.maze.block_size),
                                            reversible=True)
        self.flip_status = {'use_horiz': True, 'h_flip': False, 'v_flip': False}
        self.spawn_info = self.maze.player_spawn[1]
        self.tile = self.maze.player_spawn[0]
        self.direction = None
        self.speed = maze.block_size / 4
        self.image, self.rect = self.horizontal_images.get_image()
        self.rect.centerx, self.rect.centery = self.spawn_info   # screen coordinates for spawn

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
        if self.direction != 'u':
            self.direction = 'u'
            if self.flip_status['v_flip']:
                self.vertical_images.flip(False, True)
                self.flip_status['v_flip'] = False
            self.flip_status['use_horiz'] = False

    def set_move_left(self):
        """Set move direction left"""
        if self.direction != 'l':
            self.direction = 'l'
            if not self.flip_status['h_flip']:
                self.horizontal_images.flip()
                self.flip_status['h_flip'] = True
            self.flip_status['use_horiz'] = True

    def set_move_down(self):
        """Set move direction down"""
        if self.direction != 'd':
            self.direction = 'd'
            if not self.flip_status['v_flip']:
                self.vertical_images.flip(x_bool=False, y_bool=True)
                self.flip_status['v_flip'] = True
            self.flip_status['use_horiz'] = False

    def set_move_right(self):
        """Set move direction to right"""
        if self.direction != 'r':
            self.direction = 'r'
            if self.flip_status['h_flip']:
                self.horizontal_images.flip()
                self.flip_status['h_flip'] = False
            self.flip_status['use_horiz'] = True

    def get_nearest_col(self):
        """Get the current column location on the maze map"""
        return (self.rect.x - (self.screen.get_width() // 5)) // self.maze.block_size

    def get_nearest_row(self):
        """Get the current row location on the maze map"""
        return (self.rect.y - (self.screen.get_height() // 12)) // self.maze.block_size

    def is_blocked(self):
        """Check if PacMan is blocked by any maze barriers, return True if blocked, False if clear"""
        result = False
        if self.direction is not None:
            original_pos = self.rect
            if self.direction == 'u':
                test = self.rect.move((0, -self.speed))
            elif self.direction == 'l':
                test = self.rect.move((-self.speed, 0))
            elif self.direction == 'd':
                test = self.rect.move((0, self.speed))
            else:
                test = self.rect.move((self.speed, 0))
            self.rect = test    # temporarily move self

            # if any collision, result = True
            if pygame.sprite.spritecollideany(self, self.maze.maze_blocks):
                result = True
            elif pygame.sprite.spritecollideany(self, self.maze.shield_blocks):
                result = True
            self.rect = original_pos    # reset position
        return result

    def update(self):
        """Update PacMan's position in the maze if moving, and if not blocked"""
        if self.direction:  # TODO: convert direction to utilize tiles for AI
            if self.flip_status['use_horiz']:
                self.image = self.horizontal_images.next_image()
            else:
                self.image = self.vertical_images.next_image()
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
        collision = pygame.sprite.spritecollideany(self, self.maze.pellets)
        if collision:
            collision.kill()
            score += 10
        collision = pygame.sprite.spritecollideany(self, self.maze.fruits)
        if collision:
            collision.kill()
            score += 20
            fruit_count += 1
        return score, fruit_count
