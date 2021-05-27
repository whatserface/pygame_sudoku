from pygame import Rect, draw, init, font, transform, Surface, display, image, key, event, QUIT, MOUSEBUTTONUP, KEYDOWN, mouse, K_BACKSPACE
from random import randrange, choice, randint
import time
from collections import Counter
class Sudoku():
    def __init__(self):
        self.i = 0
        self.field = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                               [4, 5, 6, 7, 8, 9, 1, 2, 3],
                               [7, 8, 9, 1, 2, 3, 4, 5, 6],
                               [2, 3, 4, 5, 6, 7, 8, 9, 1],
                               [5, 6, 7, 8, 9, 1, 2, 3, 4],
                               [8, 9, 1, 2, 3, 4, 5, 6, 7],
                               [3, 4, 5, 6, 7, 8, 9, 1, 2],
                               [6, 7, 8, 9, 1, 2, 3, 4, 5],
                               [9, 1, 2, 3, 4, 5, 6, 7, 8]]  # создания поля
        self.mix_funcs()
        self.start_game()
    def transpose(self):
        self.field = list(map(list, zip(*self.field))) # значения столбцов и значения рядов меняются местами
    def swapping_rows_in_area(self):
        rect = randrange(3) # случайный квадрат
        row1 = randrange(3) # ряд квадрата
        index1 = rect*3 + row1
        row2 = randrange(3) # ряд для обмена
        while row2 == row1: # на случай, если ряд один и тот же
            row2 = randrange(3)
        index2 = rect*3 + row2
        self.field[index1], self.field[index2] = self.field[index2], self.field[index1]
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
            self.field[index1], self.field[index2] = self.field[index2], self.field[index1]
    def swapping_big_columns(self): # обмен 3-мя квадрата по столбцам
        self.transpose()
        self.swapping_big_rows()
        self.transpose()
    def mix_funcs(self): # рандомайзер функций
        methods = dir(self)[-5:]
        for i in range(randint(5, 20)):
            method = choice(methods)
            eval('self.' + method + '()')
    def start_game(self):
        self.i += 1
        print(f"I've done {self.i} iterations to generate puzzle")
        self.player_area = [[0 for i in range(9)] for i in range(9)] # то что будет видеть игрок
        elements = []
        for i in range(randint(30, 35)):
            row, collumn = randrange(0, 9, randint(1, 3)), randrange(0, 9, randint(1, 3))
            while (row, collumn) in elements:
                row, collumn = randint(0, 8), randint(0, 8)
            elements.append((row, collumn))
            self.player_area[row][collumn] = self.field[row][collumn]
        if not self.check_sudoku(): # если решений судоку больше одного - всё заполнить заново
            self.start_game()
    def check_sudoku(self):
        self.grid = self.player_area
        self.possible_solutions = set()
        zv = 0
        def possible(self, r, c, n):  # r - row, c - collumn, n - number
            if n in self.grid[r]:
                return False
            for i in range(9):
                if n == self.grid[i][c]:
                    return False
            r0 = r // 3 * 3
            c0 = c // 3 * 3
            for i in range(3):
                for j in range(3):
                    if n == self.grid[r0 + i][c0 + j]:
                        return False
            return True
        def solve_sudoku(self):
            nonlocal zv
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == 0:
                        for n in range(1, 10):
                            if possible(self, i, j, n):
                                self.grid[i][j] = n
                                solve_sudoku(self)
                                self.grid[i][j] = 0
                        return
            self.possible_solutions.add(tuple(map(tuple, self.grid)))
            if len(self.possible_solutions) > 1:
                zv += 1
                return
        for i in range(20):
            solve_sudoku(self)
            self.i += 1
            if zv >= 1:
                return False
            self.grid = self.player_area
        return True
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
    for i, tup in enumerate(players_numbers): #i = 0, tup = (0, 1)
        if grid.field[players_indexes[i][0]][players_indexes[i][1]] != tup[1]:
            red_surface = Surface((51, 51))
            players_mistakes.append((red_surface, players_indexes[i]))
    if len(players_mistakes) == 0 and len(players_numbers) == remained_cells:
        playing = 0
def init_grid():
    global indexes, ints, players_numbers, players_indexes, players_mistakes, row, collumn, show
    screen.blit(generating_sign, (514, 115))
    grid.__init__()
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
if __name__ == '__main__':
    init()
    grid = Sudoku()
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
    grid_pic = transform.scale(image.load('empty_sudoku_field.png'), (501, 499))
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
    generating_sign, show, once, kostil = fnt.render('Generating...', True, blue), False, False, 0
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
                if (row, collumn) == i[1] and passing == 0:
                    players_mistakes.remove(i)
                    continue
                i[0].fill(red)
                screen.blit(i[0], (numbers[1][i[1][1]], numbers[0][i[1][0]]))
        for i in range(len(ints)):
            screen.blit(ints[i], (numbers[1][indexes[i][1]], numbers[0][indexes[i][0]]))
        for mmmi in range(len(players_numbers)):
            if len(players_numbers) != 0:
                screen.blit(players_numbers[mmmi][0], (numbers[1][players_indexes[mmmi][1]], numbers[0][players_indexes[mmmi][0]]))
        draw.rect(screen, rect_color, check_button)
        draw.rect(screen, blue, start_button)
        screen.blit(check_lable, check_coords)
        screen.blit(start_lable, start_coords)
        if not playing:
            screen.blit(win1, win1_coords)
            screen.blit(win2, win2_coords)
        if show:
            screen.blit(generating_sign, (514, 115))
            kostil += 1
        if kostil > 1:
            init_grid()
            kostil = 0
        for e in event.get():
            if e.type == QUIT:
                game = 0
            if e.type == MOUSEBUTTONUP: #если он кликает ЛКМом на ячейку сетки
                mouse_pos = mouse.get_pos()
                if playing: # координаты мышки игрока
                    if grid_pic_rect.collidepoint(mouse_pos) and screen.get_at(mouse_pos)[:3] != black:
                        x0, y0 = mouse_pos
                        collumn, row = (x0//55), ((y0-1)//55) # определить какая эта ячейка
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
                    #init_grid()
                    passing = 1
            if e.type == KEYDOWN:
                if passing == 0 and playing and e.key == K_BACKSPACE:
                    fill_cell('0', row, collumn)
                if passing == 0 and playing:
                    if e.unicode.isdigit():
                        fill_cell(e.unicode, row, collumn)
        display.update()
        if show and kostil > 0:
            kostil += 1