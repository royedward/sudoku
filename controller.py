import json
from random import shuffle
from tkinter.messagebox import showinfo
from winsound import Beep


class Controller:
    num_of_games = 51

    def __init__(self):
        self.nums = None
        self.json_info = None
        self.game_started = False
        self.correct_count = 0
        self.master_numbers = None

        self.visible_nums = ['' for _ in range(0, 81)]

        self.game_index = list(range(1, Controller.num_of_games))

        shuffle(self.game_index)

    def popup_you_won(self):
        showinfo("Congratulations!", "You Won The Game - Play Another Game")

    def read_json_file(self, path):
        with open(path) as file:
            data = file.read()
            return json.loads(data)

    def write_entry_values(self):
        for i in range(0, 81):
            d = self.master_numbers[i]

            if len(d) == 2:
                d = d[:1]
                self.nums[i].set(d)
                self.visible_nums[i] = d
                self.correct_count += 1

    def setup_game(self):
        self.master_numbers = None
        self.correct_count = 0

        if len(self.game_index) == 0:
            self.game_index = list(range(1, self.num_of_games))
            shuffle(self.game_index)

        game_num = str(self.game_index.pop())
        d = self.json_info['game' + game_num]

        string = ''

        for i in range(0, 9):
            string += d[i] + ','

        self.master_numbers = string.split(',')
        self.write_entry_values()
        self.game_started = True

    def clear_entries(self):
        for i in range(0, 81):
            self.nums[i].set('')
            self.visible_nums[i] = ''

    def new_game(self):
        self.game_started = False
        self.clear_entries()
        self.setup_game()
        self.game_started = True

    def trace(self, position, dummy_1, dummy_2):
        if not self.game_started:
            return

        pos = int(position[6:])
        number_entered = self.nums[pos].get()
        correct_number = self.master_numbers[pos]

        if number_entered != correct_number:
            if self.visible_nums[pos] == '':
                self.nums[pos].set('')
                Beep(1000, 100)
            else:
                self.nums[pos].set(self.visible_nums[pos])

        else:

            self.correct_count += 1
            self.visible_nums[pos] = number_entered

            if self.correct_count == 81:
                self.popup_you_won()
                self.new_game()

    def start_controller(self, nums):
        self.nums = nums
        self.json_info = self.read_json_file('./sudoku.json')
        self.setup_game()
