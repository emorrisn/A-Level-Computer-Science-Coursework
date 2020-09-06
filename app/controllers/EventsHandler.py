import re
import sys
import pygame
from app.App import *

class FindEvent:
    def __init__(self, memory, event_name, event_args=None, level_args=None):
        self.event_name = event_name
        self.event_args = event_args
        self.level_args = level_args  ## Sometimes we can't get what to do next, so ask what level to continue too.
        self.memory = memory

    def run(self):
        if self.event_name == "register_user":
            RegisterUserEvent(self.memory, self.event_args, self.level_args).register()
        elif self.event_name == "change_lvl":
            ChangeLevelEvent(self.memory, self.event_args).change()
        elif self.event_name == "pause_game":
            PauseGameEvent(self.memory, self.event_args).pause()
        elif self.event_name == "continue_user":
            ContinueUserEvent(self.memory, self.event_args).do()
        elif self.event_name == "check_answer":
            CheckAnswer(self.memory, self.event_args).check()
        elif self.event_name == "quit_game":
            pygame.quit()
            sys.exit()


class CheckAnswer:
    def __init__(self, memory, text):
        self.memory = memory
        self.level = self.memory.bag['current_level']
        self.text = text

    def check(self):
        if self.level['tasks']:
            correct_answer = self.level['task']['answer']
            if self.text == correct_answer:
                ## Give 10 points to the user.
                UpdateUserEvent(self.memory).add_score(10)
                ChangeLevelEvent(self.memory, self.level['task']['return_success']).change()
            else:
                ## Minus a life from the user.
                UpdateUserEvent(self.memory).minus_life(1)
                ChangeLevelEvent(self.memory, self.level['task']['return_fail']).change()


class ChangeLevelEvent:
    def __init__(self, memory, level):
        self.level = level
        self.memory = memory

    def change(self):
        from app.controllers.ViewHandler import ViewHandler
        self.memory.bag['previous_level'] = self.memory.bag['current_level']
        string = re.search("{(.*?)}", self.level)
        if string:
            for i in string.groups():
                self.level = self.level.replace("{" + i + "}", str(eval(i)), 3)
        ## Save level to authenticated user
        UpdateUserEvent(self.memory).update_level(self.level)
        ViewHandler(self.memory).set_current_view(self.level)


class UpdateUserEvent:
    def __init__(self, memory):
        self.user = []
        self.memory = memory

    def update_level(self, level):
        try:
            self.user = self.memory.bag['user']
            self.user['stage'] = level
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def minus_life(self, amount):
        try:
            self.user = self.memory.bag['user']
            self.user['lives'] = self.user['lives'] - int(amount)
            self.commit_changes()

            ## Check if user is dead
            if self.user['lives'] < 1:
                ChangeLevelEvent(self.memory, 'dead_menu').change()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def add_life(self, amount):
        try:
            self.user = self.memory.bag['user']
            self.user['lives'] = self.user['lives'] + int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def add_score(self, amount):
        try:
            self.user = self.memory.bag['user']
            self.user['score'] = self.user['score'] + int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def minus_score(self, amount):
        try:
            self.user = self.memory.bag['user']
            self.user['score'] = self.user['score'] - int(amount)
            self.commit_changes()
        except Exception as e:
            print("Could not update user. Not logged in? (" + str(e) + ")")

    def login(self, username):
        self.memory.bag['user'] = getattr(App().Users, username)
        with open('app/users.json') as data:
            Users = type("Users", (), json.load(data))

    def commit_changes(self):
        with open('app/users.json', 'r+') as data:
            J_Users = json.load(data)
            J_Users[self.user['name']] = self.user
            data.seek(0)
            data.truncate(0)
            json.dump(J_Users, data)


class PauseGameEvent:
    def __init__(self, memory):
        self.memory = memory
        self.level = self.memory.bag['current_level']

    def pause(self):
        self.memory.bag['pause_continue'] = self.level
        ChangeLevelEvent(self.memory, 'pause_menu').change()


class ContinueUserEvent:
    def __init__(self, memory, username):
        self.memory = memory
        self.username = username
        self.user = ""

    def do(self):
        UpdateUserEvent(self.memory).login(self.username)
        try:
            self.user = self.memory.bag['user_name']
        except Exception as e:
            ChangeLevelEvent(self.memory, "menu").change()
        else:
            ChangeLevelEvent(self.memory, self.user['stage']).change()


class RegisterUserEvent:
    def __init__(self, memory, username, level):
        self.username = username
        self.level = level
        self.memory = memory

    def register(self):
        ## Currently overwrites user, when continue feature maybe ask user?
        with open('app/users.json', 'r+') as data:
            J_Users = json.load(data)
            J_Users[self.username] = {"name": self.username, "lives": 3, "score": 0, "stage": ""}
            data.seek(0)
            data.truncate(0)
            json.dump(J_Users, data)

        UpdateUserEvent(self.memory).login(self.username)
        ChangeLevelEvent(self.memory, self.level).change()
