import pygame
from event_loop import EventLoop
from ghost import Ghost
from maze import Maze
from pacman import PacMan
from score import ScoreController


class PacManPortalGame:
    """Contains the main logic and methods
    for the running and updating of the PacMan portal game"""

    BLACK_BG = (0, 0, 0)
    START_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (800, 600)
        )
        pygame.display.set_caption('PacMan Portal')
        self.clock = pygame.time.Clock()
        self.score_keeper = ScoreController(screen=self.screen,
                                            sb_pos=((self.screen.get_width() // 5),
                                                    (self.screen.get_height() * 0.95)),
                                            items_image='cherry.png',
                                            itc_pos=(int(self.screen.get_width() * 0.6),
                                                     self.screen.get_height() * 0.95))
        self.maze = Maze(screen=self.screen, maze_map_file='maze_map.txt')
        self.player = PacMan(screen=self.screen, maze=self.maze)
        self.ghosts = pygame.sprite.Group()
        self.spawn_ghosts()
        self.actions = {PacManPortalGame.START_EVENT: self.init_ghosts}

    def init_ghosts(self):
        """Remove the maze shields and kick start the ghost AI"""
        self.maze.remove_shields()
        for g in self.ghosts:
            g.enable()

    def spawn_ghosts(self):
        """Create all ghosts at their starting positions"""
        files = ['ghost-red.png', 'ghost-lblue.png', 'ghost-orange.png', 'ghost-pink.png']
        idx = 0
        while len(self.maze.ghost_spawn) > 0:
            spawn_info = self.maze.ghost_spawn.pop()
            self.ghosts.add(Ghost(screen=self.screen, maze=self.maze, target=self.player,
                                  spawn_info=spawn_info, ghost_file=files[idx]))
            idx = (idx + 1) % len(files)

    def update_score(self):
        """Check if PacMan has eaten pellets that increase the score"""
        n_score, n_fruits = self.player.eat()
        self.score_keeper.add_score(score=n_score, items=n_fruits if n_fruits > 0 else None)

    def update_screen(self):
        """Update the game screen"""
        self.screen.fill(PacManPortalGame.BLACK_BG)
        self.update_score()
        self.maze.blit()
        self.ghosts.update()
        for g in self.ghosts:
            g.blit()
        self.player.update()
        self.player.blit()
        self.score_keeper.blit()
        pygame.display.flip()

    def run_game(self):
        """Run the game's event loop, using an EventLoop object"""
        e_loop = EventLoop(loop_running=True, actions={**self.player.event_map, **self.actions})
        pygame.time.set_timer(PacManPortalGame.START_EVENT, 5000)  # Signal game start in 5 seconds

        while e_loop.loop_running:
            self.clock.tick(60)  # 60 fps limit
            e_loop.check_events()
            self.update_screen()


if __name__ == '__main__':
    game = PacManPortalGame()
    game.run_game()
