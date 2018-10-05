import pygame
from event_loop import EventLoop
from maze import Maze


class PacManPortalGame:
    """Contains the main logic and methods
    for the running and updating of the PacMan portal game"""

    BLACK_BG = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (800, 600)
        )
        pygame.display.set_caption('PacMan Portal')
        self.clock = pygame.time.Clock()
        self.maze = Maze(screen=self.screen, maze_map_file='maze_map.txt')

    def update_screen(self):
        """Update the game screen"""
        self.screen.fill(PacManPortalGame.BLACK_BG)
        self.maze.blit()
        pygame.display.flip()

    def run_game(self):
        """Run the game's event loop, using an EventLoop object"""
        e_loop = EventLoop(loop_running=True)

        while e_loop.loop_running:
            self.clock.tick(60)  # 60 fps limit
            e_loop.check_events()
            self.update_screen()


if __name__ == '__main__':
    game = PacManPortalGame()
    game.run_game()
