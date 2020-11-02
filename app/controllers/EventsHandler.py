import re
import sys
import pygame
from app.App import *

class FindEvent:
    def __init__(self, app, event_name, event_args=None, level_args=None):
        self.event_name = event_name
        self.event_args = event_args
        self.level_args = level_args  ## Sometimes we can't get what to do next, so ask what level to continue too.
        self.app = app

    def run(self):
        if self.event_name == "register_user":
            RegisterUserEvent(self.app, self.event_args, self.level_args).register()
        elif self.event_name == "change_lvl":
            ChangeLevelEvent(self.app, self.event_args).change()
        elif self.event_name == "continue_user":
            ContinueUserEvent(self.app, self.event_args).do()
        elif self.event_name == "check_answer":
            CheckAnswer(self.app, self.event_args).check()
        elif self.event_name == "quit_game":
            pygame.quit()
            sys.exit()


class CheckAnswer:
    def __init__(self, app, text):
        self.app = app
        self.level = self.app.bag['current_level']
        self.text = text

    def check(self):
        if self.level['tasks']:
            correct_answer = self.level['task']['answer']
            if self.text.lower() == correct_answer.lower():
                ## Give 10 points to the user.
                UpdateUserEvent(self.app).add_score(10)
                ChangeLevelEvent(self.app, self.level['task']['return_success']).change()
            else:
                ## Minus a life from the user.
                UpdateUserEvent(self.app).minus_life(1)
                ChangeLevelEvent(self.app, self.level['task']['return_fail']).change()


class ChangeLevelEvent:
    def __init__(self, app, level):
        self.level = level
        self.app = app

    def change(self):
        from app.controllers.ViewHandler import ViewHandler
        self.app.bag['previous_level_name'] = self.app.bag['current_level_name']
        self.app.bag['previous_level'] = self.app.bag['current_level']
        string = re.search("{(.*?)}", self.level)
        if string:
            for i in string.groups():
                self.level = self.level.replace("{" + i + "}", str(eval(i)), 3)
        ## Save level to authenticated user
        UpdateUserEvent(self.app).update_level(self.level)
        ViewHandler(self.app).set_current_view(self.level)


class UpdateUserEvent:
    def __init__(self, app):
        self.user = []
        self.app = app
        self.cwd = os.path.dirname(os.path.abspath(__file__))

    def update_level(self, level):
        try:
            self.user = self.app.bag['user']
            self.user['stage'] = level
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def minus_life(self, amount):
        try:
            self.user = self.app.bag['user']
            self.user['lives'] = self.user['lives'] - int(amount)
            self.commit_changes()

            ## Check if user is dead
            if self.user['lives'] < 1:
                ChangeLevelEvent(self.app, 'dead_menu').change()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def add_life(self, amount):
        try:
            self.user = self.app.bag['user']
            self.user['lives'] = self.user['lives'] + int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def add_score(self, amount):
        try:
            self.user = self.app.bag['user']
            self.user['score'] = self.user['score'] + int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def minus_score(self, amount):
        try:
            self.user = self.app.bag['user']
            self.user['score'] = self.user['score'] - int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def login(self, username):
        self.app.bag['user'] = getattr(App().Users, username)
        with open(os.path.join(self.cwd, '../users.json')) as data:
            Users = type("Users", (), json.load(data))

    def commit_changes(self):
        with open(os.path.join(self.cwd, '../users.json'), 'r+') as data:
            J_Users = json.load(data)
            J_Users[self.user['name']] = self.user
            data.seek(0)
            data.truncate(0)
            json.dump(J_Users, data)
            data.close()


class ContinueUserEvent:
    def __init__(self, app, username):
        self.app = app
        self.username = username

    def do(self):
        try:
            UpdateUserEvent(self.app).login(self.username)
            ChangeLevelEvent(self.app, self.app.bag['user']['stage']).change()
        except Exception as e:
            print(e)
            ChangeLevelEvent(self.app, "menu").change()


class RegisterUserEvent:
    def __init__(self, app, username, level):
        self.username = username
        self.level = level
        self.app = app
        self.cwd = os.path.dirname(os.path.abspath(__file__))

    def register(self):
        ## Currently overwrites user, when continue feature maybe ask user?
        with open(os.path.join(self.cwd, '../users.json'), 'r+') as data:
            J_Users = json.load(data)
            J_Users[self.username] = {"name": self.username, "lives": 3, "score": 0, "stage": ""}
            data.seek(0)
            data.truncate(0)
            json.dump(J_Users, data)

        UpdateUserEvent(self.app).login(self.username)
        ChangeLevelEvent(self.app, self.level).change()
