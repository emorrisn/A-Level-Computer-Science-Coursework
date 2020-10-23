from app.controllers.EventsHandler import *


class Text:
    def __init__(self, app, label, label_font, label_size, pos_x, pos_y, colour, animation_delay, animations):
        self.app, self.label, self.pos_x, self.pos_y, self.colour, self.animation_delay, self.animations = app, label, pos_x, pos_y, colour, animation_delay, animations
        self.label_font = pygame.font.Font('resources/fonts/' + getattr(self.app.Fonts, label_font), label_size)

    def draw(self):
        text_surface = self.label_font.render(Helpers.smart_translate(self, self.label), True, self.colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.pos_x, self.pos_y)
        if self.animations:
            pygame.time.delay(self.animation_delay)
        self.app.screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, app, id, label, font_name, font_size, colour, pos_x, pos_y, bg_colour_inactive, bg_colour_active,
                 width, height, hover, animation_delay, animations):
        self.app, self.label, self.colour, self.bg_colour_inactive, self.bg_colour_active, self.hover, self.animation_delay, self.animations = app, label, colour, bg_colour_inactive, bg_colour_active, hover, animation_delay, animations
        self.label_font = Helpers.font(app, font_name, font_size)
        self.int_x = int(pos_x)
        self.int_y = int(pos_y)
        self.w = int(width)
        self.h = int(height)
        self.id = id,
        self.surface = pygame.Surface((self.app.Config.screen_width, self.app.Config.screen_height), pygame.SRCALPHA,
                                      32)
        self.mouse = pygame.mouse.get_pos()
        self.x = self.int_x - (self.w / 2)
        self.y = self.int_y - (self.h / 3)

    def draw(self):
        button = pygame.event.Event(pygame.USEREVENT, id=self.id, etype="button")

        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y and self.hover == True:
            pygame.draw.rect(self.surface, self.bg_colour_active, (self.x - 5, self.y - 5, self.w + 10, self.h + 10))
            pygame.draw.rect(self.surface, self.bg_colour_inactive, (self.x, self.y, self.w, self.h))
            pygame.display.update()
        else:
            pygame.draw.rect(self.surface, self.bg_colour_inactive, (self.x - 5, self.y - 5, self.w + 10, self.h + 10))
            pygame.draw.rect(self.surface, self.bg_colour_inactive, (self.x, self.y, self.w, self.h))
            pygame.display.update()
        text_surface = self.label_font.render(Helpers.smart_translate(self, self.label), True, self.colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.int_x, self.int_y)
        if self.animations:
            pygame.time.delay(self.animation_delay)

        self.app.screen.blit(self.surface, (self.surface.get_rect()))
        self.app.screen.blit(text_surface, text_rect)

        if (self.int_x - (self.w / 2)) + self.w > self.mouse[0] > (self.int_x - (self.w / 2)) and (
                self.int_y - (self.h / 3)) + self.h > self.mouse[1] > (self.int_y - (self.h / 3)):
            if (pygame.mouse.get_pressed()[0]) == 1:
                pygame.event.post(button)


class Rectangle:
    def __init__(self, app, position_x, position_y, width, height, bg_colour, animation_delay, animations):
        self.app, self.position_x, self.position_y, self.width, self.height, self.bg_colour, self.animation_delay, self.animations = app, position_x, position_y, width, height, bg_colour, animation_delay, animations
        self.surface = pygame.Surface((self.app.Config.screen_width, self.app.Config.screen_height), pygame.SRCALPHA,32)

    def draw(self):
        pygame.draw.rect(self.surface, self.bg_colour, (self.position_x, self.position_y, self.width, self.height))
        self.app.screen.blit(self.surface, (self.surface.get_rect()))
        if self.animations:
            pygame.time.delay(self.animation_delay)


class Image:
    def __init__(self, app, source, position_x, position_y, resize_x, resize_y):
        self.app, position_x, self.position_y, self.resize_x, self.resize_y, self.source = app, position_x, position_y, resize_x, resize_y, source
        self.image = ""

    def draw(self):
        self.image = pygame.image.load(self.source)
        self.image = pygame.transform.scale(self.image, (self.resize_x, self.resize_y))
        self.app.screen.blit(self.image, (self.position_x, self.position_y))


class Input:
    def __init__(self, app, id, submit_on, initial_string="", text_color=(0, 0, 0), bg_colour=(0, 0, 0), font_name="",
                 font_size="", max_string_length=-1):
        self.app, self.text_color, self.max_string_length, self.input_string, self.bg_colour, self.submit_on, self.id = app, text_color, max_string_length, Helpers.smart_translate(self, initial_string), bg_colour, submit_on, id
        self.font_object = Helpers.font(app, font_name, font_size)
        self.surface = pygame.Surface((1, 1))
        self.kr_counters = {}
        self.cursor_surface = pygame.Surface((int(font_size / 20 + 2), font_size))
        self.cursor_surface.fill(text_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.key_blacklist = [13, 99, 122, 120, 118]

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.kr_counters:
                    self.kr_counters[event.key] = [0, event.unicode]
                if event.key == pygame.K_BACKSPACE:
                    self.input_string = self.input_string.replace('  ', '')
                    self.input_string = (self.input_string[:max(self.cursor_position - 1, 0)] + self.input_string[
                                                                                                self.cursor_position:] + "  ")
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))
                elif event.key == pygame.K_LEFT:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    if event.key not in self.key_blacklist and event.key < 128:
                        self.input_string = (
                                self.input_string[:self.cursor_position] + event.unicode + self.input_string[
                                                                                           self.cursor_position:])
                        self.cursor_position += len(event.unicode)
                if event.key == eval("pygame." + self.submit_on):
                    i = pygame.event.Event(pygame.USEREVENT, id=self.id, etype="input")
                    pygame.event.post(i)
            elif event.type == pygame.KEYUP:
                if event.key in self.kr_counters:
                    del self.kr_counters[event.key]
                self.surface.blit(self.surface, (self.surface.get_width(), 0))

        for key in self.kr_counters:
            self.kr_counters[key][0] += self.app.clock.get_time()
            if self.kr_counters[key][0] >= 400:
                self.kr_counters[key][0] = 365
                event_key, event_unicode = key, self.kr_counters[key][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))
        self.surface = self.font_object.render(self.input_string, False, self.text_color, self.bg_colour)
        if self.cursor_position > 0:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string
