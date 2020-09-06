from datetime import datetime
import json
import locale


class App:
    def __init__(self):
        self.Levels = ""
        self.Users = ""
        self.Fonts = ""
        self.Config = ""
        self.Colours = ""
        self.load_all()

    def load_all(self):
        self.load_Colours()
        self.load_Config()
        self.load_Fonts()
        self.load_Levels()
        self.load_Users()

    def load_Levels(self):
        with open('app/levels.json') as data:
            self.Levels = type("Levels", (), json.load(data))

    def load_Users(self):
        with open('app/users.json') as data:
            self.Users = type("Users", (), json.load(data))

    def load_Fonts(self):
        with open('app/details.json') as data:
            self.Fonts = type("Fonts", (), json.load(data)['fonts'])

    def load_Config(self):
        with open('app/details.json') as data:
            self.Config = type("Config", (), json.load(data)['config'])

    def load_Colours(self):
        with open('app/details.json') as data:
            self.Colours = type("Colours", (), json.load(data)['colours'])


class Helpers:

    @staticmethod
    def number_format(number):
        locale.setlocale(locale.LC_ALL, 'en_US')
        return locale.format("%d", number, grouping=True)

    @staticmethod
    def current_time():
        return datetime.now().strftime('%I:%M %p')
