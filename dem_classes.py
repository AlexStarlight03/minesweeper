
import random
from colorama import Fore

class Grid(list):

    def __init__(self, size: int):
        self.size = size
        self.cases = size * size
        self.grid = self.create_grid(size)

    def create_grid(self, size: int) -> list:
        grid = []
        for line in range(size):
            new_line = []
            for colonne in range(size):
                new_line.append("?")
            grid.append(new_line)
        return grid

    def print_grid(self, img = None) -> None:
        print()
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == "F":
                    print(img, end=" ") if img else print(str(self.grid[row][col]), end="  ")
                elif self.grid[row][col] == "?":
                    print(Fore.WHITE + str(self.grid[row][col]), end="  ")
                else:
                    print(Fore.CYAN + str(self.grid[row][col]), end="  ")
            print()
        print(Fore.RESET) #  reset to default color or use '\033[39m' which is the default color code


class PlayerInput:
    def __init__(self, row: int, col: int, nb_mines: int):
        self.row = row
        self.col = col
        self.nb_mines = nb_mines
        self.actions = None
        self.exploded = False
        self.flags = nb_mines

    def get_action(self, Game: Grid):
        while True:
            self.actions = input("Écrivez F pour placer ou enlever un drapeau suivis des coords; ou seulement les coord  (Ex: f 4 7 ou 4 7): ").strip().lower().split(" ")
            if self.check_exit(self.actions[0]):
                return True
            if len(self.actions) > 3 or len(self.actions) < 2:
                print("Veuillez entrer une action valide.")
                continue
            self.row = int(self.actions[-2]) - 1
            self.col = int(self.actions[-1]) - 1
            if self.row < 0 or self.row >= Game.size or self.col < 0 or self.col >= Game.size:
                print("Les coordonnées doivent être comprises entre 1 et", Game.size)
                continue
            if self.actions[0] == "f":
                self.actions = "F"
                return
            if Game.grid[self.row][self.col] == "F":
                print(Fore.RED + "Vous ne pouvez pas révéler une case marquée d'un drapeau." + Fore.RESET)
                continue
            else:
                break
        return
    
    @staticmethod
    def check_exit(input_str: str) -> bool:
        if input_str in ["exit", "quit", "q", "no", "n", "non"]:
            print(Fore.CYAN + "Oki byeeeeee!" + Fore.RESET)
            return True
        return False
    

class Mines(Grid):
    
    def __init__(self, size: int, Input: PlayerInput):
        super().__init__(size)
        self.nb_mines = Input.nb_mines
        self.all_positions = tuple(range(self.cases))
        self.mine_positions = random.sample(self.minus_first(self.all_positions, Input.row, Input.col), self.nb_mines)
        self = self.place_mines("F")
        # print(self.grid) # DEBUG: pour voir la grille avec les mines placées lors de l'initialisation

    def minus_first(self, all_positions: list, row: int, col: int) -> list:
        first_click = row * self.size + col
        new_all = list(all_positions)
        new_all.remove(first_click)
        return new_all

    def place_mines(self, img) -> list:
        for i in range(len(self.mine_positions)):
            row = self.mine_positions[i] // self.size
            col = self.mine_positions[i] % self.size
            self.grid[row][col] = img
        self.grid = self.populate_grid(self.grid, img)
        return self

    def populate_grid(self, AGrid: Grid, img: str) -> Grid:
        for i in range(len(self.all_positions)):
            if self.all_positions[i] in self.mine_positions:
                continue
            row = self.all_positions[i] // self.size
            col = self.all_positions[i] % self.size
            count = 0
            for r in range(-1, 2):
                for c in range(-1, 2):
                    if row+r < 0 or row+r >= self.size or col+c < 0 or col+c >= self.size:
                        continue
                    if self.grid[row+r][col+c] == img:          
                        count +=1
            self.grid[row][col] = str(count)
        return self.grid
    