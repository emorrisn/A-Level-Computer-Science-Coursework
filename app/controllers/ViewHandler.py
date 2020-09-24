from app.controllers.ComponentsHandler import *
from app.controllers.EventsHandler import *
from app.controllers.MemoryHandler import *


class ViewHandler:

    def __init__(self, memory=None):
        self.t, self.b, self.r, self.i = "", "", "", ""
        self.rectangles, self.max_images, self.images, self.max_rectangles = 0, 0, 0, 0
        self.fullscreen, self.typing_started = False, False
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.animations = True
        if memory:
            self.memory = memory
        else:
            self.memory = MemoryHandler()
        self.memory.bag['inputs'] = []
        self.memory.bag['current_level'] = ""
        self.memory.bag['user'] = getattr(App().Users, "user")  ## TODO remove in production (testing purposes only.)

    ## Translates JSON to a displayed level
    def set_current_view(self, view):
        self.setup_view(view)

        ## Loop for the entire view
        while True:
            ## Draw all components of the view
            self.draw_images()
            self.draw_rectangles()
            self.draw_text()
            self.draw_buttons()
            self.animations = False

            ## Deal with events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.typing_started = True
                    if event.key == pygame.K_F10:
                        if not self.fullscreen:
                            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.fullscreen = True
                        else:
                            pygame.display.set_mode((App().Config.screen_width, App().Config.screen_height), 0, 32)
                            self.fullscreen = False
                        self.set_current_view(view)
                self.component_event(event)

            ## Update inputs
            if len(self.memory.bag['inputs']) > 0:
                for ix, inputx in enumerate(self.memory.bag['inputs']):
                    if inputx:
                        self.i = self.memory.bag['current_level']['contents']['inputs'][str(ix + 1)]
                        inputx.update(events)
                        self.screen.blit(inputx.get_surface(), (self.i["position_x"], self.i["position_y"]))

            pygame.display.update()
            self.clock.tick(App().Config.fps)

        ## TODO: Tasks

    def draw_images(self):
        if "images" in self.memory.bag['current_level']['contents']:
            if self.images < self.max_images:
                for image in self.memory.bag['current_level']['contents']['images']:
                    self.i = self.memory.bag['current_level']['contents']['images'][image]
                    Image(self.i['source'], self.i['x'], self.i['y'], self.i['resize_x'], self.i['resize_y']).draw()
                    self.images += 1

    def draw_rectangles(self):
        if "rectangles" in self.memory.bag['current_level']['contents']:
            if self.rectangles < self.max_rectangles:
                for rectangle in self.memory.bag['current_level']['contents']['rectangles']:
                    self.r = self.memory.bag['current_level']['contents']['rectangles'][rectangle]
                    Rectangle(self.r['position_x'], self.r['position_y'], self.r['width'], self.r['height'],
                              self.r['bg_colour'], self.r['animation_delay'], self.animations).draw()
                    self.rectangles += 1
                    pygame.display.flip()

    def draw_text(self):
        if "text" in self.memory.bag['current_level']['contents']:
            for text in self.memory.bag['current_level']['contents']['text']:
                self.t = self.memory.bag['current_level']['contents']['text'][text]
                if self.t['animation_delay'] != 0:
                    Text(self.memory, self.t['label'], self.t['label_font'], self.t['label_size'], self.t['position_x'],
                         self.t['position_y'], self.t['colour'], self.t['animation_delay'], self.animations).draw()
                    pygame.display.flip()
                else:
                    Text(self.memory, self.t['label'], self.t['label_font'], self.t['label_size'], self.t['position_x'],
                         self.t['position_y'], self.t['colour'], self.t['animation_delay'], self.animations).draw()

    def draw_buttons(self):
        for button in self.memory.bag['current_level']['contents']['buttons']:
            self.b = self.memory.bag['current_level']['contents']['buttons'][button]
            Button(self.memory, self.b['id'], self.b['label'], self.b['label_font'], self.b['label_size'],
                   self.b['colour'],
                   self.b['position_x'],
                   self.b['position_y'], self.b['bg_colour_inactive'], self.b['bg_colour_active'],
                   self.b['width'], self.b['height'], self.b['actions']['hover'],
                   self.b['animation_delay'], self.animations).draw()
            pygame.display.flip()

    def draw_inputs(self):
        if "inputs" in self.memory.bag['current_level']['contents']:
            for input in self.memory.bag['current_level']['contents']['inputs']:
                self.i = self.memory.bag['current_level']['contents']['inputs'][input]
                self.memory.bag['inputs'].append(
                    Input(input, self.i['actions']['submit_on'], self.i['starting_text'], self.i['colour'],
                          self.i['bg_colour'], self.i['label_font'], self.i['label_size']))

    def component_event(self, event):
        """
        Every time the event loop is ran, this gives the categories each component type events for them to check.

        Parameters:
            event (obj): PyGame event object

        """
        if event.type == pygame.USEREVENT:
            if event.etype == "button":
                for button in self.memory.bag['current_level']['contents']['buttons']:
                    if event.id[0] == int(button):

                        ## Deal with inputs that are linked to buttons
                        if "inputs" in self.memory.bag['current_level']['contents']:
                            for i in self.memory.bag['current_level']['contents']['inputs']:
                                ## check if input is linked to a button
                                if self.memory.bag['current_level']['contents']['inputs'][i]['actions'][
                                    'linked_to'] == int(
                                    button):
                                    FindEvent(
                                        self.memory,
                                        self.memory.bag['current_level']['contents']['inputs'][i]['actions']['event'],
                                        self.memory.bag['inputs'][int(i) - 1].get_text().strip()).run()

                        # Deal with Buttons that are not linked to anything
                        action_details = self.memory.bag['current_level']['contents']['buttons'][button]['actions'][
                            'action_details']
                        string = re.search("{(.*?)}", action_details)
                        if string:
                            for i in string.groups():
                                action_details = action_details.replace("{" + i + "}", str(eval(i)), 3)
                        FindEvent(self.memory,
                                  self.memory.bag['current_level']['contents']['buttons'][button]['actions']['action'],
                                  action_details).run()
            elif event.etype == "input":
                if "inputs" in self.memory.bag['current_level']['contents']:
                    for i in self.memory.bag['current_level']['contents']['inputs']:
                        if event.id[0] == i:
                            if self.memory.bag['current_level']['contents']['inputs'][i]['actions']['linked_to'] == 0:
                                FindEvent(
                                    self.memory,
                                    self.memory.bag['current_level']['contents']['inputs'][i]['actions']['event'],
                                    self.memory.bag['inputs'][int(i) - 1].get_text().strip(),
                                    self.memory.bag['current_level']['contents']['inputs'][i]['actions']['level']).run()

    def setup_view(self, view):
        """
        When a new view is requested, this sets variables, ensures objects are not drawn when it's not necessary.

        Parameters:
            view (str): Name of the view / level

        """
        self.memory.bag['current_level'] = getattr(App().Levels, view)
        self.rectangles = 0
        self.memory.bag['inputs'] = []
        pygame.display.set_caption(App().Config.name + self.memory.bag['current_level']['screen_title'])
        self.screen.fill(self.memory.bag['current_level']['background_colour'])
        self.animations = True

        if "rectangles" in self.memory.bag['current_level']['contents']:
            self.max_rectangles = len(self.memory.bag['current_level']['contents']['rectangles'])
        else:
            self.max_rectangles = 0

        if "images" in self.memory.bag['current_level']['contents']:
            self.max_images = len(self.memory.bag['current_level']['contents']['images'])
        else:
            self.max_images = 0

        self.draw_inputs()
