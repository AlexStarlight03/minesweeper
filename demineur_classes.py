
from dem_classes import Grid, Mines, PlayerInput, Fore


def place_flag(grid: list, info: PlayerInput) -> list:
    flag_pos = grid[info.row][info.col]
    if flag_pos == "?":
        if info.flags <= 0:
            print(Fore.RED + "Vous n'avez plus de drapeaux disponibles." + Fore.RESET)
            return
        flag_pos = "F"
        info.flags -= 1
    elif flag_pos == "F":
        flag_pos = "?"
        info.flags += 1
    grid[info.row][info.col] = flag_pos
    return


def eight_reveal(player: list, answer: list, size: int, Input: PlayerInput) -> list: 
    mines_to_tag = int(player[Input.row][Input.col])
    wrong_flag = 0
    for r in range(-1, 2):
        rows = Input.row + r
        if rows < 0 or rows >= size:
            continue
        for c in range(-1, 2):
            cols = Input.col + c
            if cols < 0 or cols >= size or (r == 0 and c == 0):
                continue
            if player[rows][cols] == "F":
                 mines_to_tag -= 1
            if answer[rows][cols] == "F" and player[rows][cols] != "F":
                wrong_flag += 1
    if wrong_flag > 0 and mines_to_tag == 0:
        Input.exploded = True
    if mines_to_tag == 0 and not Input.exploded:
        for r in range(-1, 2):
            rows = Input.row + r
            if rows < 0 or rows >= size:
                continue
            for c in range(-1, 2):
                cols = Input.col + c
                if cols < 0 or cols >= size or (r == 0 and c == 0):
                    continue
                if answer[rows][cols] != "F" and player[rows][cols] == "?":
                        player[rows][cols] = answer[rows][cols]
    return


def reveal(player: list, answer: list, size: int, row: int, col: int) -> list:
    if answer[row][col] != "F":
        player[row][col] = answer[row][col]
    if answer[row][col] == "0":
        for r in range(-1, 2):
            rows = row + r
            if rows < 0 or rows >= size:
                continue
            for c in range(-1, 2):
                cols = col + c
                if cols < 0 or cols >= size or (r == 0 and c == 0):
                    continue
                if player[rows][cols] == "?":
                    reveal(player, answer, size, rows, cols)
    return player


def check_end(Game: Grid, GameMines: Mines, Input: PlayerInput) -> bool:
    if ((GameMines.grid[Input.row][Input.col] == "F" and Game.grid[Input.row][Input.col] != "F") or Input.exploded is True) and Input.actions != "F": #THIS WORKS BUT UGLY
        print(Fore.RED + "💥 BOOM ! Vous avez touché une mine. Fin de la partie.")
        GameMines.print_grid("💥")
        return True
    if Game.grid == GameMines.grid:
        print(Fore.LIGHTGREEN_EX + "Vous avez gagné !" + Fore.RESET)
        Game.print_grid("💣")
        return True
    return False


def init_game():
    print("Entrez 'exit' ou 'quit' à tout moment pour quitter.")
    while True:
        size = input("Taille de la grille entre 3 et 25 (ex. 10 pour 10x10) : ").strip().lower()
        if PlayerInput.check_exit(size):
            return None, None
        try:
            size = int(size)
            if size < 3 or size > 25:
                raise ValueError
            break
        except ValueError:
            print(f"La taille de la grille doit être un nombre entre 3 et 25.")
    while True:
        nb_mines = input("Nombre de mines : ").strip().lower()
        if PlayerInput.check_exit(nb_mines):
            return None, None
        try:
            nb_mines = int(nb_mines)
            if nb_mines <= 0 or nb_mines >= size * size:
                raise ValueError
            break
        except ValueError:
            print(f"Le nombre de mines doit être un nombre plus grand que 0 et inférieur à {size * size}.")
    return Grid(size), PlayerInput(0, 0, nb_mines)


def main():
    print("Bienvenue dans le jeu du démineur!")
    while True:
        Game, Input = init_game()
        if Game is None:
            return
        GameMines = None
        while True:
            Game.print_grid("🚩")
            print("Vous avez", Input.flags, "drapeaux restants.")
            if Input.get_action(Game) is True:
                return
            if GameMines is None: # Grille réponse créé aprés la première action car le premier clic ne doit jamais être une mine.
                GameMines = Mines(Game.size, Input)
            if Game.grid[Input.row][Input.col].isnumeric():
                eight_reveal(Game.grid, GameMines.grid, Game.size, Input)
            if Input.actions == "F":
                place_flag(Game.grid, Input)
            else:
                reveal(Game.grid, GameMines.grid, Game.size, Input.row, Input.col)
            if check_end(Game, GameMines, Input):
                break
        again = input("Voulez-vous jouer à nouveau ? (o/n) : ").strip().lower()
        if Input.check_exit(again):
            return

if __name__ == "__main__":
    main()
