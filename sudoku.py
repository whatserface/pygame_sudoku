from pygame import Rect, draw, init, font, transform, Surface, display, image, key, event, QUIT, MOUSEBUTTONUP, KEYDOWN, mouse, K_BACKSPACE
from random import randrange, randint, choices, shuffle
from time import time
import numpy as np

class Sudoku():
    def __init__(self):
        self.field = np.array([
                      [1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [4, 5, 6, 7, 8, 9, 1, 2, 3],
                      [7, 8, 9, 1, 2, 3, 4, 5, 6],
                      [2, 3, 4, 5, 6, 7, 8, 9, 1],
                      [5, 6, 7, 8, 9, 1, 2, 3, 4],
                      [8, 9, 1, 2, 3, 4, 5, 6, 7],
                      [3, 4, 5, 6, 7, 8, 9, 1, 2],
                      [6, 7, 8, 9, 1, 2, 3, 4, 5],
                      [9, 1, 2, 3, 4, 5, 6, 7, 8]], dtype=int)  # создания поля
        self.random_numbers = np.arange(81)
        shuffle(self.random_numbers)
        self.shuffle_field()
        self.player_area = self.field.copy()
        self.test_grid = self.field.copy()
        self.generate_field(0)

    def transpose(self):
        self.field = np.array(list((map(list, zip(*self.field))))) # значения столбцов и значения рядов меняются местами

    def swapping_rows_in_area(self):
        random_rect = randrange(3)
        row1 = randrange(3) # ряд квадрата
        index1 = random_rect*3 + row1
        row2 = randrange(3) # ряд для обмена
        while row2 == row1: # на случай, если ряд один и тот же
            row2 = randrange(3)
        index2 = random_rect*3 + row2
        self.field[[index1, index2]] = self.field[[index2, index1]]

    def swapping_small_columns(self): # обмен значений столбцов
        self.transpose()
        self.swapping_rows_in_area()
        self.transpose()

    def swapping_big_rows(self): # обмен 3-мя квадратами по рядам
        area1 = randrange(3) # 3 квадрата
        area2 = randrange(3) # другие два квадрата
        while area2 == area1:
            area2 = randrange(3)
        for i in range(3):
            index1, index2 = area1*3 + i, area2*3 + i
            self.field[[index1, index2]] = self.field[[index2, index1]]

    def swapping_big_columns(self): # обмен 3-мя квадратами по столбцам
        self.transpose()
        self.swapping_big_rows()
        self.transpose()

    def shuffle_field(self):
        methods = [self.swapping_big_rows, self.swapping_rows_in_area, self.swapping_big_columns, self.swapping_small_columns, self.transpose]
        shuffled_methods = choices(methods, k=randint(10, 30))
        for method in shuffled_methods:
            method()

    def generate_field(self, index):
        if index >= 81:
            return
        row, col = divmod(self.random_numbers[index], 9)
        if self.player_area[row][col] != 0:
            self.test_grid = self.player_area.copy()
            self.test_grid[row][col] = 0
            solutions = self.amount_of_solutions(0, 0)
            if solutions == 1:
                self.player_area[row][col] = 0
        self.generate_field(index+1)


    def possible_values(self, row, col):
        start_row = row // 3 * 3
        start_col = col // 3 * 3
        return {1, 2, 3, 4, 5, 6, 7, 8, 9} - set(self.test_grid[start_row:start_row + 3, start_col:start_col + 3].flat) - set(self.test_grid[row, :]) - set(self.test_grid[:, col])

    def amount_of_solutions(self, number, possible_solutions: int):
        if possible_solutions > 1:
            return possible_solutions
        if number >= 81:
            possible_solutions += 1
            return possible_solutions
        row, col = divmod(number, 9)
        if self.test_grid[row][col] > 0:
            possible_solutions = self.amount_of_solutions(number + 1, possible_solutions)
        else:
            values = list(self.possible_values(row, col))
            shuffle(values)
            for value in values:
                self.test_grid[row][col] = value
                possible_solutions = self.amount_of_solutions(number + 1, possible_solutions)
                self.test_grid[row][col] = 0
        return possible_solutions


def fill_cell(number, row, collumn):
    if number == '0':
        if (row, collumn) in players_indexes:
            ind = players_indexes.index((row, collumn))
            del players_numbers[ind], players_indexes[ind]
    else:
        text = fnt.render(number, True, orange)
        if not (row, collumn) in players_indexes:
            players_numbers.append((text, int(number)))
            players_indexes.append((row, collumn))
        else:
            players_numbers[players_indexes.index((row, collumn))] = (text, int(number))

def check():
    global players_mistakes, remained_cells, playing
    players_mistakes = []
    for i, tup in enumerate(players_numbers):
        if grid.field[players_indexes[i][0]][players_indexes[i][1]] != tup[1]:
            red_surface = Surface((51, 51))
            players_mistakes.append((red_surface, players_indexes[i]))
    if len(players_mistakes) == 0 and len(players_numbers) == remained_cells:
        playing = 0

def init_grid():
    global indexes, ints, players_numbers, players_indexes, players_mistakes, row, collumn, show
    screen.blit(generating_sign, (514, 115))
    print('Generating sudoku, it may take some time')
    generate_time = time()
    grid.__init__()
    print(f'Mesh was generated in {round(time() - generate_time, 2)} seconds')
    indexes = []
    ints = []
    players_numbers, players_indexes, players_mistakes = [], [], []
    row, collumn = None, None
    for i in range(len(grid.player_area)):
        for j in range(len(grid.player_area[i])):
            if grid.player_area[i][j] != 0:
                text = fnt.render(str(grid.player_area[i][j]), True, black)
                indexes.append((i, j))
                ints.append(text)
    show = False

if __name__ == "__main__":
    init()
    print('Generating sudoku, it may take some time')
    generate_time = time()
    grid = Sudoku()
    print(f'Mesh was generated in {round(time() - generate_time, 2)} seconds')
    indexes = []
    ints = []
    fnt = font.SysFont('calibri', 40)
    small_fnt = font.SysFont('calibri', 28)
    FPS, white, grey, black, rect_color, red, orange, blue = 60, (255, 255, 255), (197, 199, 201), (0, 0, 0), (163, 212, 255), (255, 0, 0), (255, 162, 33), (0, 148, 255)
    for i in range(len(grid.player_area)):
        for j in range(len(grid.player_area[i])):
            if grid.player_area[i][j] != 0:
                text = fnt.render(str(grid.player_area[i][j]), True, black)
                indexes.append((i, j))
                ints.append(text)
    players_numbers, players_indexes, players_mistakes = [], [], []
    row, collumn = None, None
    remained_cells = 81 - len(ints)
    screen = display.set_mode((800, 600))
    display.set_caption('Sudoku')
    grid_coords = (0, 0)
    grid_pic = transform.scale(image.load(r'empty_sudoku_field.png'), (501, 499))
    grid_pic_rect = grid_pic.get_rect()
    chosen_cell = Surface((51, 51))
    check_lable = fnt.render("ПРОВЕРИТЬ", True, orange)
    start_lable = small_fnt.render("Начать новую игру", True, white)
    check_button = Rect(100, 515, 335, 75)
    start_button = Rect(515, 475, 265, 75)
    check_coords = (160, 535)
    start_coords = (538, 500)
    game, playing = 1, 1
    win1, win2, win1_coords, win2_coords = fnt.render('''You've solved''', True, orange), fnt.render('sudoku!', True, orange), (520, 65), (570, 105)
    generating_sign, show, once, still = fnt.render('Generating...', True, blue), False, False, 0
    numbers = [[7, 59, 114, 171, 225, 279, 337, 389, 444], [7, 60, 114, 170, 223, 277, 335, 387, 442]]  # (Y, X) - (ROW, COLLUMN)координаты вообще, но пусть будут numbers
    passing = 1
    while game:
        keys_pressed = key.get_pressed()
        screen.fill(white)
        screen.blit(grid_pic, grid_coords)
        if passing == 0:
            chosen_cell.fill(grey)
            screen.blit(chosen_cell, element)
        for i in players_mistakes:
            if len(players_numbers) != 0:
                if (row, collumn) == i[1] and p2assing == 0:
                    players_mistakes.remove(i)
                    continue
                i[0].fill(red)
                screen.blit(i[0], (numbers[1][i[1][1]], numbers[0][i[1][0]]))
        for i in range(len(ints)):
            screen.blit(ints[i], (numbers[1][indexes[i][1]], numbers[0][indexes[i][0]]))
        for mmmi in range(len(players_numbers)):
            if len(players_numbers) != 0:
                screen.blit(players_numbers[mmmi][0],
                            (numbers[1][players_indexes[mmmi][1]], numbers[0][players_indexes[mmmi][0]]))
        draw.rect(screen, rect_color, check_button)
        draw.rect(screen, blue, start_button)
        screen.blit(check_lable, check_coords)
        screen.blit(start_lable, start_coords)
        if not playing:
            screen.blit(win1, win1_coords)
            screen.blit(win2, win2_coords)
        if show:
            screen.blit(generating_sign, (514, 115))
            still += 1
        if still > 1:
            init_grid()
            still = 0
        for e in event.get():
            if e.type == QUIT:
                game = 0
            if e.type == MOUSEBUTTONUP:
                mouse_pos = mouse.get_pos()
                if playing:
                    if grid_pic_rect.collidepoint(mouse_pos) and screen.get_at(mouse_pos)[:3] != black:
                        x0, y0 = mouse_pos
                        collumn, row = (x0 // 55), ((y0 - 1) // 55)  # определить какая эта ячейка
                        if (row, collumn) not in indexes and not (row, collumn) == (None, None):
                            element = (numbers[1][collumn], numbers[0][row])
                            passing = 0
                        else:
                            passing = 1
                    else:
                        passing = 1
                    if check_button.collidepoint(mouse_pos):
                        check()
                        passing = 1
                if start_button.collidepoint(mouse_pos):
                    show = True
                    passing = 1
            if e.type == KEYDOWN:
                if passing == 0 and playing and e.key == K_BACKSPACE:
                    fill_cell('0', row, collumn)
                if passing == 0 and playing:
                    if e.unicode.isdigit():
                        fill_cell(e.unicode, row, collumn)
        display.update()
        if show and still > 0:
            still += 1
    print('Exit')
