
from constants.config import rand_tetrimino
from constants.tetri_mino import *


class Environment:
    def __init__(self, reset=False) -> None:
        super().__init__()
        # Initial values
        self.game_process_counter = 1
        self.best_score = 0
        self.reset(reset)

    def reset(self, start=False):
        self.start = start
        self.done = False
        self.game_over = False
        self.boundaries = [0] * 10
        self.max_bp = 0
        self.previous_boundaries = [0] * 10
        self.previous_max_bp = 0

        self.score = 0
        self.level = 1
        self.goal = self.level * 5
        self.bottom_count = 0
        self.hard_drop = False

        self.dx, self.dy = 3, 0  # Minos location status
        self.rotation = 0  # Minos rotation status

        self.mino = rand_tetrimino()  # Current mino ## TODO : randint(1,4)
        self.next_mino = rand_tetrimino()  # Next mino ## TODO : randint(1,4)

        self.hold = False  # Hold status
        self.hold_mino = -1  # Holded mino

        self.width = 10  # Board width
        self.height = 20  # Board height
        self.matrix = [[0] * (self.height + 1) for _ in range(self.width)]  # Board matrix

        self.tetri_mino = TetriMino()
        self.erase_count = 0

    def next(self):
        self.game_process_counter += 1
        if self.score > self.best_score:
            self.best_score = self.score

    def scale_boundaries(self, boundaries):
        maxBoundary = self.max_bp
        if maxBoundary > 4:
            for count, value in enumerate(boundaries):
                new_boundary = boundaries[count] - maxBoundary + 4
                boundaries[count] = new_boundary if new_boundary >= 0 else 0
        return boundaries

    def get_boundaries(self):
        boundaries = []
        for y in self.matrix:
            boundary = 0
            for xkey, x in enumerate(y):
                if x > 0:
                    boundary = len(y) - xkey
                    break

            boundaries.append(boundary)

        self.boundaries = boundaries
        self.max_bp = max(boundaries)
        return boundaries

    # Returns true if mino is at bottom
    def is_bottom(self, x, y, mino, r):
        grid = self.tetri_mino.mino_map[mino - 1][r]['GRID']

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    if (y + i + 1) > 20:
                        return True
                    elif self.matrix[x + j][y + i + 1] != 0 and self.matrix[x + j][y + i + 1] != 8:
                        return True

        return False

    # Returns true if mino is at the left edge
    def is_leftedge(self, x, y, mino, r):
        grid = self.tetri_mino.mino_map[mino - 1][r]['GRID']

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    if (x + j - 1) < 0:
                        return True
                    elif self.matrix[x + j - 1][y + i] != 0:
                        return True

        return False

    # Returns true if mino is at the right edge
    def is_rightedge(self, x, y, mino, r):
        grid = self.tetri_mino.mino_map[mino - 1][r]['GRID']

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    if (x + j + 1) > 9:
                        return True
                    elif self.matrix[x + j + 1][y + i] != 0:
                        return True

        return False

    # Returns true if turning right is possible
    def is_turnable_r(self, x, y, mino, r):
        if r != (len(self.tetri_mino.mino_map[mino - 1]) - 1):
            grid = self.tetri_mino.mino_map[mino - 1][r + 1]['GRID']
        else:
            grid = self.tetri_mino.mino_map[mino - 1][0]['GRID']

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                        return False
                    elif self.matrix[x + j][y + i] != 0:
                        return False

        return True

    # Returns true if turning left is possible
    def is_turnable_l(self, x, y, mino, r):
        # simplifiable avec modulo
        if r != 0:
            grid = self.tetri_mino.mino_map[mino - 1][r - 1]['GRID']
        else:
            grid = self.tetri_mino.mino_map[mino - 1][len(self.tetri_mino.mino_map[mino - 1]) - 1]['GRID']

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                        return False
                    elif self.matrix[x + j][y + i] != 0:
                        return False

        return True

    # Returns true if new block is drawable
    def is_stackable(self, mino):
        grid = self.tetri_mino.mino_map[mino - 1][0]['GRID']

        for i in range(4):
            for j in range(4):
                # print(grid[i][j],  self.matrix[3 + j][i])
                if grid[i][j] != 0 and self.matrix[3 + j][i] != 0:
                    return False

        return True

    # Draw a tetrimino
    def draw_mino(self, x, y, mino, r):
        grid = TetriMino.mino_map[mino - 1][r]['GRID']

        # Draw mino
        try:
            for i in range(4):
                for j in range(4):
                    if grid[i][j] != 0:
                        self.matrix[x + j][y + i] = grid[i][j]
        except:
            pass

    def draw_ghost(self, x, y, mino, r):
        grid = TetriMino.mino_map[mino - 1][r]['GRID']
        tx, ty = x, y
        while not self.is_bottom(tx, ty, mino, r):
            ty += 1

        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    self.matrix[tx + j][ty + i] = 8

    # Erase a tetrimino
    def erase_mino(self, x, y, mino, r):
        grid = TetriMino.mino_map[mino - 1][r]['GRID']
        for i in range(4):
            for j in range(4):
                if x + j > 9:
                    j = 0

                if grid[i][j] != 0:
                    self.matrix[x + j][y + i] = 0

    def erase_ghost(self):
        self.matrix = [[0 if j == 8 else j for j in i] for i in self.matrix]

    def is_lines_cleared(self):
        return self.erase_count != 0

    def bumpiness(self):
        total = 0

        for index, col in enumerate(self.matrix):
            total += self.calcul_column_height(index) - self.calcul_column_height(index + 1)

        return total

    def holes_created_count(self):
        max_grid_bp = self.max_bp
        radar = 4
        if max_grid_bp < 4:
            radar = max_grid_bp

        count = 0

        for col in range(len(self.matrix)):
            block = False
            row_start = (max_grid_bp - 21) * -1
            row_end = (max_grid_bp - 21) * -1 + radar
            for row in range(row_start, row_end):
                if self.matrix[col][row] > 0:
                    block = True
                elif self.matrix[col][row] == 0 and block is True:
                    count += 1

        return count

    def is_blockade_created(self):
        max_grid_bp = self.max_bp
        radar = 4
        if max_grid_bp < 4:
            radar = max_grid_bp
        count = 0
        for col in range(len(self.matrix)):
            row_start = (max_grid_bp - 21) * -1
            row_end = (max_grid_bp - 21) * -1 + radar
            for row in range(row_start, row_end):
                if self.matrix[col][row] == 0 and self.matrix[col][row - 1] and self.matrix[col][row - 1] != 0 and \
                        self.matrix[col][row - 2] and self.matrix[col][row - 2] != 0:
                    count += 1
        # print("blockade", count)

        return count

    def is_bumpiness_increased_by(self, previous, current):
        delta = self.max_bp - self.previous_max_bp
        if delta > 0:
            # print("bumpiness detected", delta)
            return delta
        return 0

    def is_bumpiness_increased(self):
        return self.previous_max_bp == self.max_bp

    def is_touching_the_floor(self, previous, current):
        if min(previous) == 0:
            for i in range(previous):
                if previous[i] == 0 and current[i] != 0:
                    return 1
        return 0

    def set_previous_boundaries(self):
        self.previous_max_bp = self.max_bp
        boundaries = self.get_boundaries()
        self.previous_boundaries = self.get_boundaries()

    def try_erase_line(self):
        self.erase_count = 0
        for j in range(21):
            is_full = True
            for i in range(10):
                if self.matrix[i][j] == 0:
                    is_full = False
            if is_full:
                self.erase_count += 1
                k = j
                while k > 0:
                    for i in range(10):
                        self.matrix[i][k] = self.matrix[i][k - 1]
                    k -= 1
        if self.erase_count == 1:
            self.score += 50 * self.level
        elif self.erase_count == 2:
            self.score += 150 * self.level
        elif self.erase_count == 3:
            self.score += 350 * self.level
        elif self.erase_count == 4:
            self.score += 1000 * self.level
