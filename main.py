from app.controllers.ViewHandler import *


class Main:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_caption(App().Config.name)
        self.screen = pygame.display.set_mode((App().Config.screen_width, App().Config.screen_height), 0, 32)
        self.run()

    @staticmethod
    def run():
        ## Set the view the game when it is first ran.
        ViewHandler().set_current_view("tasks_1_blank")


Main().run()
