import pygame
import project.characters as characters

class KeyboardInput:
    def __init__(self):
        self.events_queue = []

    def process_events(self, events):
        for event in characters.Player.keys:
            if events[event]:
                self.events_queue.append(event)

        return self.events_queue

    def empty_queue(self):
        self.events_queue.clear()


class MouseInput:
    def __init__(self):
        pass

    @classmethod
    def check_quit(cls, events, state):
        for event in events:
            if event.type == pygame.QUIT:
                state = 'Quit'
        return state

    def process_events(self, events):
        pass
