import pygame
from cell import Cell
from sudoku_generator import SudokuGenerator, generate_sudoku

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, row, col, screen) for col in range(9)] for row in range(9)]
        self.original_board = []
        self.solution_board = []
        self.find_selected_cell = None
        self.selected_cell = None
        if self.difficulty == 'Easy':
            removed_cells = 30
        elif self.difficulty == 'Medium':
            removed_cells = 40
        elif self.difficulty == 'Hard':
            removed_cells = 50

        generator = SudokuGenerator(9, removed_cells)
        self.solution_board, self.original_board = generate_sudoku(9, removed_cells)

        for row in range(9):
            for col in range(9):
                value = self.original_board[row][col]
                self.cells[row][col].set_cell_value(value)

    def draw(self):
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), thickness)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)
        return (row, col)

    def click(self, x, y):
        if x < 540 and y < 540:
            col = x // 60
            row = y // 60
            return (row, col)
        return None

    def clear(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].value == 0:
                self.cells[row][col].set_sketched_value(value)

    def finalize_number(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].sketch_value != 0:
                self.cells[row][col].set_cell_value(self.cells[row][col].sketch_value)
                self.cells[row][col].set_sketched_value(0)
                self.selected_cell = None

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                value = self.original_board[row][col]
                self.cells[row][col].set_cell_value(value)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.original_board[row][col] = self.cells[row][col].value

    def find_empty(self):
        for row in self.cells:
            for cell in row:
                if cell.selected:
                    return (cell.row, cell.col)
        return None

    def is_valid(self, row, col):
        num = self.cells[row][col].value
        if num == 0:
            return False

        # Check row
        for c in range(9):
            if c != col and self.cells[row][c].value == num:
                return False

        # Check column
        for r in range(9):
            if r != row and self.cells[r][col].value == num:
                return False

        # Check 3x3 box
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if (r != row or c != col) and self.cells[r][c].value == num:
                    return False

        return True

    def check_board(self):
        for row in range(9):
            for col in range(9):
                if not self.is_valid(row, col):
                    return False
        return True

    def get_sketch(self, row, col):
        return self.cells[row][col].get_sketched_value()