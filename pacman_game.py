import pygame
from event_loop import EventLoop
from ghost import Ghost
from maze import Maze
from pacman import PacMan
from lives_status import PacManCounter
from score import ScoreController, LevelTransition
from menu import Menu, HighScoreScreen
from intro import Intro


class PacManPortalGame:
    """Contains the main logic and methods
    for the running and updating of the PacMan portal game"""

    BLACK_BG = (0, 0, 0)
    START_EVENT = pygame.USEREVENT + 1
    REBUILD_EVENT = pygame.USEREVENT + 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (800, 600)
        )
        pygame.display.set_caption('PacMan Portal')
        self.clock = pygame.time.Clock()
        self.score_keeper = ScoreController(screen=self.screen,
                                            sb_pos=((self.screen.get_width() // 5),
                                                    (self.screen.get_height() * 0.965)),
                                            items_image='cherry.png',
                                            itc_pos=(int(self.screen.get_width() * 0.6),
                                                     self.screen.get_height() * 0.965))
        self.maze = Maze(screen=self.screen, maze_map_file='maze_map.txt')
        self.life_counter = PacManCounter(screen=self.screen, ct_pos=((self.screen.get_width() // 3),
                                                                      (self.screen.get_height() * 0.965)),
                                          images_size=(self.maze.block_size, self.maze.block_size))
        self.level_transition = LevelTransition(screen=self.screen, score_controller=self.score_keeper)
        self.game_over = True
        self.player = PacMan(screen=self.screen, maze=self.maze)
        self.ghosts = pygame.sprite.Group()
        self.first_ghost = None
        self.spawn_ghosts()
        self.actions = {PacManPortalGame.START_EVENT: self.init_ghosts,
                        PacManPortalGame.REBUILD_EVENT: self.rebuild_maze}

    def init_ghosts(self):
        """Remove the maze shields and kick start the ghost AI"""
        self.maze.remove_shields()
        for g in self.ghosts:
            g.enable()
        pygame.time.set_timer(PacManPortalGame.START_EVENT, 0)  # disable timer repeat

    def spawn_ghosts(self):
        """Create all ghosts at their starting positions"""
        files = ['ghost-pink.png', 'ghost-lblue.png', 'ghost-orange.png', 'ghost-red.png']
        idx = 0
        while len(self.maze.ghost_spawn) > 0:
            spawn_info = self.maze.ghost_spawn.pop()
            g = Ghost(screen=self.screen, maze=self.maze, target=self.player,
                      spawn_info=spawn_info, ghost_file=files[idx])
            if files[idx] == 'ghost-red.png':
                self.first_ghost = g
                g.enable()  # red ghost is enabled first
            self.ghosts.add(g)
            idx = (idx + 1) % len(files)

    def rebuild_maze(self):
        """Resets the maze to its initial state"""
        if self.life_counter.lives > 0:
            self.maze.build_maze()
            self.player.reset_position()
            for g in self.ghosts:
                g.reset_position()
            if self.player.dead:
                self.player.revive()
            self.first_ghost.enable()
            pygame.time.set_timer(PacManPortalGame.START_EVENT, 5000)  # Signal game start in 5 seconds
        else:
            self.game_over = True
        pygame.time.set_timer(PacManPortalGame.REBUILD_EVENT, 0)    # disable timer repeat

    def check_player(self):
        """Check the player to see if they have been hit by an enemy, or if they have consumed pellets/fruit"""
        n_score, n_fruits, power = self.player.eat()
        self.score_keeper.add_score(score=n_score, items=n_fruits if n_fruits > 0 else None)
        if power:
            for g in self.ghosts:
                g.begin_blue_state()
        ghost_collide = pygame.sprite.spritecollideany(self.player, self.ghosts)
        if ghost_collide and ghost_collide.state['blue']:
            ghost_collide.set_eaten()
            self.score_keeper.add_score(200)
        elif ghost_collide and not (self.player.dead or ghost_collide.state['return']):
            self.life_counter.decrement()
            self.player.set_death()
            for g in self.ghosts:
                g.disable()
            pygame.time.set_timer(PacManPortalGame.REBUILD_EVENT, 4000)  # Signal maze rebuild in 4 seconds
        elif not self.maze.pellets_left():
            self.score_keeper.increment_level()
            self.level_transition.prep_level_msg()
            self.level_transition.show()
            for g in self.ghosts:
                g.disable()
            self.rebuild_maze()

    def update_screen(self):
        """Update the game screen"""
        self.screen.fill(PacManPortalGame.BLACK_BG)
        self.check_player()
        self.maze.blit()
        self.ghosts.update()
        for g in self.ghosts:
            g.blit()
        self.player.update()
        self.player.blit()
        self.score_keeper.blit()
        self.life_counter.blit()
        pygame.display.flip()

    def run(self):
        """Run the game application, starting from the menu"""
        menu = Menu(self.screen)
        hs_screen = HighScoreScreen(self.screen, self.score_keeper)
        intro_seq = Intro(self.screen)
        e_loop = EventLoop(loop_running=True, actions={pygame.MOUSEBUTTONDOWN: menu.check_buttons})

        while e_loop.loop_running:
            e_loop.check_events()
            self.screen.fill(PacManPortalGame.BLACK_BG)
            if not menu.hs_screen:
                intro_seq.update()  # display intro/menu
                intro_seq.blit()
                menu.update()
                menu.blit()
            else:
                hs_screen.blit()    # display highs score screen
                hs_screen.check_done()
            if menu.ready_to_play:
                self.play_game()    # player selected play, so run game
                menu.ready_to_play = False
                self.score_keeper.save_high_scores()    # save high scores only on complete play
            pygame.display.flip()

    def play_game(self):
        """Run the game's event loop, using an EventLoop object"""
        e_loop = EventLoop(loop_running=True, actions={**self.player.event_map, **self.actions})
        pygame.time.set_timer(PacManPortalGame.START_EVENT, 5000)  # Signal game start in 5 seconds
        self.game_over = False

        while e_loop.loop_running:
            self.clock.tick(60)  # 60 fps limit
            e_loop.check_events()
            self.update_screen()
            if self.game_over:
                e_loop.loop_running = False


if __name__ == '__main__':
    game = PacManPortalGame()
    game.run()
