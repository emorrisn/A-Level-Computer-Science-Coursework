from app.controllers.ViewHandler import *


class Main:
    def __init__(self):
        pygame.init()
        self.app = App()
        self.c = self.app.Config
        self.screen = pygame.display.set_mode((self.c.screen_width, self.c.screen_height), self.c.render_flags, self.c.colour_depth)
        self.run()

    def run(self):
        ## Set the view the game when it is first ran.
        ViewHandler().set_current_view(self.c.starting_screen)


Main().run()
