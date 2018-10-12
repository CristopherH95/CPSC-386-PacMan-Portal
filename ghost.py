from pygame.sprite import Sprite, spritecollideany
from image_manager import ImageManager


class Ghost(Sprite):
    """Represents the enemies of PacMan which chase him around the maze"""
    def __init__(self, screen, maze, target, spawn_info, ghost_file='ghost-red.png'):
        super().__init__()
        self.screen = screen
        self.maze = maze
        self.internal_map = maze.map_lines
        self.target = target
        self.norm_images = ImageManager(ghost_file, sheet=True, pos_offsets=[(0, 0, 32, 32), (0, 32, 32, 32)],
                                        resize=(self.maze.block_size, self.maze.block_size),
                                        animation_delay=250)
        self.eyes = ImageManager('ghost-eyes.png', sheet=True, pos_offsets=[(0, 0, 32, 32), (32, 0, 32, 32),
                                                                            (0, 32, 32, 32), (32, 32, 32, 32)],
                                 resize=(self.maze.block_size, self.maze.block_size),
                                 keys=['r', 'u', 'd', 'l'])
        self.image, self.rect = self.norm_images.get_image()
        self.curr_eye, _ = self.eyes.get_image(key='r')    # default eye to looking right
        self.image.blit(self.curr_eye, (0, 0))  # combine eyes and body
        self.rect.centerx, self.rect.centery = spawn_info[1]
        self.tile = spawn_info[0]
        self.search = None
        self.direction = None
        self.speed = maze.block_size / 4
        self.enabled = False

    def get_direction_options(self):
        """Check if the ghost is blocked by any maze barriers and return all directions possible to move in"""
        tests = {
            'u': self.rect.move((0, -self.speed)),
            'l': self.rect.move((-self.speed, 0)),
            'd': self.rect.move((0, self.speed)),
            'r': self.rect.move((self.speed, 0))
        }
        remove = []
        original_pos = self.rect

        for d, t in tests.items():
            self.rect = t   # temporarily move self
            if spritecollideany(self, self.maze.maze_blocks) and d not in remove:
                remove.append(d)    # if collision, mark this direction for removal
        for rem in remove:
            del tests[rem]
        remove.clear()
        for d, t in tests.items():
            self.rect = t   # temporarily move self
            if spritecollideany(self, self.maze.shield_blocks) and d not in remove:
                remove.append(d)    # if collision, mark this direction for removal
        for rem in remove:
            del tests[rem]
        self.rect = original_pos    # reset position
        return list(tests.keys())

    def change_eyes(self, look_direction):
        """Change the ghosts' eyes to look in the given direction"""
        self.image, _ = self.norm_images.get_image()
        self.curr_eye, _ = self.eyes.get_image(key=look_direction)
        self.image.blit(self.curr_eye, (0, 0))  # combine eyes and body

    def get_chase_direction(self, options):
        """Figure out a new direction to move in based on the target and walls"""
        pick_direction = None
        target_pos = (self.target.rect.centerx, self.target.rect.centery)
        test = (abs(target_pos[0]), abs(target_pos[1]))
        prefer = test.index(max(test[0], test[1]))
        if prefer == 0:     # x direction
            if target_pos[prefer] < self.rect.centerx:  # to the left
                pick_direction = 'l'
            elif target_pos[prefer] > self.rect.centerx:    # to the right
                pick_direction = 'r'
        else:   # y direction
            if target_pos[prefer] < self.rect.centery:  # upward
                pick_direction = 'u'
            elif target_pos[prefer] > self.rect.centery:    # downward
                pick_direction = 'd'
        if pick_direction not in options:   # desired direction not available
            if 'u' in options:  # pick a direction that is available
                return 'u'
            if 'l' in options:
                return 'l'
            if 'd' in options:
                return 'd'
            if 'r' in options:
                return 'r'
        else:   # desired direction available, return it
            return pick_direction

    def get_nearest_col(self):
        """Get the current column location on the maze map"""
        return (self.rect.x - (self.screen.get_width() // 5)) // self.maze.block_size

    def get_nearest_row(self):
        """Get the current row location on the maze map"""
        return (self.rect.y - (self.screen.get_height() // 12)) // self.maze.block_size

    def is_at_intersection(self):
        """Return True if the ghost is at an intersection, False if not"""
        directions = 0
        self.tile = (self.get_nearest_row(), self.get_nearest_col())
        if self.internal_map[self.tile[0] - 1][self.tile[1]] not in ('x', ):
            directions += 1
        if self.internal_map[self.tile[0] + 1][self.tile[1]] not in ('x', ):
            directions += 1
        if self.internal_map[self.tile[0]][self.tile[1] - 1] not in ('x', ):
            directions += 1
        if self.internal_map[self.tile[0]][self.tile[1] + 1] not in ('x', ):
            directions += 1
        return True if directions > 2 else False

    def enable(self):
        """Initialize ghost AI with the first available direction"""
        options = self.get_direction_options()
        self.direction = options[0]
        self.enabled = True

    def update(self):
        """Update the ghost position"""
        if self.enabled:
            options = self.get_direction_options()
            if self.is_at_intersection():
                self.direction = self.get_chase_direction(options)
            if self.direction == 'u' and 'u' in options:
                self.rect.centery -= self.speed
            elif self.direction == 'l' and 'l' in options:
                self.rect.centerx -= self.speed
            elif self.direction == 'd' and 'd' in options:
                self.rect.centery += self.speed
            elif self.direction == 'r' and 'r' in options:
                self.rect.centerx += self.speed
            self.change_eyes(self.direction)
            self.image = self.norm_images.next_image()

    def blit(self):
        """Blit ghost image to the screen"""
        self.screen.blit(self.image, self.rect)
