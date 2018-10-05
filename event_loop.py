import pygame
from sys import exit


class EventLoop:
    """Contains the logic for checking events in a game loop"""
    def __init__(self, loop_running=False):
        self.action_map = {pygame.QUIT: exit, }
        self.loop_running = loop_running

    def check_events(self):
        """Check events to see if any match mapped actions"""
        for event in pygame.event.get():
            if event.type in self.action_map:
                self.action_map[event.type]()    # execute events from map
