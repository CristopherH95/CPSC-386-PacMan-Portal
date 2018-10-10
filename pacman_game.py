import pygame
from event_loop import EventLoop
from ghost import Ghost
from maze import Maze
from pacman import PacMan
from scoreboard import ScoreBoard


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
        self.scoreboard = ScoreBoard(screen=self.screen,
                                     pos=((self.screen.get_width() // 5),
                                          (self.screen.get_height() * 0.95)))
        self.maze = Maze(screen=self.screen, maze_map_file='maze_map.txt')
        self.player = PacMan(screen=self.screen, maze=self.maze)
        self.ghosts = []
        self.spawn_ghosts()
        self.actions = {PacManPortalGame.START_EVENT: self.init_ghosts}

    def init_ghosts(self):
        """Remove the maze shields and kick start the ghost AI"""
        self.maze.remove_shields()
        for g in self.ghosts:
            g.direction = g.get_chase_direction()

    def spawn_ghosts(self):
        """Create all ghosts at their starting positions"""
        while len(self.maze.ghost_spawn) > 0:
            self.ghosts.append(Ghost(screen=self.screen, maze=self.maze, target=self.player))

    def update_score(self):
        """Check if PacMan has eaten pellets that increase the score"""
        n_score = self.player.eat_pellets()
        self.scoreboard.update(n_score)

    def update_screen(self):
        """Update the game screen"""
        self.screen.fill(PacManPortalGame.BLACK_BG)
        self.update_score()
        self.maze.blit()
        for g in self.ghosts:
            g.update()
            g.blit()
        self.player.update()
        self.player.blit()
        self.scoreboard.blit()
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
