from random import randint
from tetri_mino import *


class Environment:
    def __init__(self) -> None:
        super().__init__()
        # Initial values
        self.game_process_counter = 1
        self.best_score = 0
        self.reset()

    def reset(self, start=False):
        self.blink = False
        self.start = start
        self.pause = False
        self.done = False
        self.game_over = False

        self.score = 0
        self.level = 1
        self.goal = self.level * 5
        self.bottom_count = 0
        self.hard_drop = False

        self.dx, self.dy = 3, 0  # Minos location status
        self.rotation = 0  # Minos rotation status

        self.mino = randint(1, 7)  # Current mino ## TODO : randint(1,7)
        self.next_mino = randint(1, 7)  # Next mino ## TODO : randint(1,7)

        self.hold = False  # Hold status
        self.hold_mino = -1  # Holded mino

        self.name_location = 0
        self.name = [65, 65, 65]

        self.width = 10  # Board width
        self.height = 20  # Board height
        self.matrix = [[0 for y in range(self.height + 1)] for x in range(self.width)]  # Board matrix

        self.tetri_mino = TetriMino()
        self.erase_count = 0
        self.previous_boundaries = [0,0,0,0,0,0,0,0,0,0]


    def next(self):
        self.game_process_counter += 1
        if self.score > self.best_score:
            self.best_score = self.score

    def get_boundaries(self):
        boundaries = []
        for key, y in enumerate(self.matrix):
            boundary = 0
            for xkey, x in enumerate(y):
                if x > 0:
                    boundary = len(y) - xkey
                    break

            boundaries.append(boundary)

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
        if r != 3:
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
        #simplifiable avec modulo
        if r != 0:
            grid = self.tetri_mino.mino_map[mino - 1][r - 1]['GRID']
        else:
            grid = self.tetri_mino.mino_map[mino - 1][3]['GRID']

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
                # print(grid[i][j], matrix[3 + j][i])
                if grid[i][j] != 0 and self.matrix[3 + j][i] != 0:
                    return False

        return True

    # Draw a tetrimino
    def draw_mino(self, x, y, mino, r):
        grid = TetriMino.mino_map[mino - 1][r]['GRID']

        tx, ty = x, y
        while not self.is_bottom(tx, ty, mino, r):
            ty += 1

        # Draw ghost
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    self.matrix[tx + j][ty + i] = 8

        # Draw mino
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    self.matrix[x + j][y + i] = grid[i][j]

    # Erase a tetrimino
    def erase_mino(self, x, y, mino, r):
        grid = TetriMino.mino_map[mino - 1][r]['GRID']

        # Erase ghost
        for j in range(21):
            for i in range(10):
                if self.matrix[i][j] == 8:
                    self.matrix[i][j] = 0

        # Erase mino
        for i in range(4):
            for j in range(4):
                if grid[i][j] != 0:
                    self.matrix[x + j][y + i] = 0
    def is_lines_cleared(self):
        return self.erase_count != 0


    def bumpiness(self):
        total = 0

        for index, col in enumerate(self.matrix):
            total += self.calcul_column_height(index) - self.calcul_column_height(index+1)

        return total

    # def rec_get_holes_count(self, matrix, final_count, sticky_count, pos_x, pos_y, sticky, full):
    #
    #     if pos_x >= 0 or pos_x <= 9 and pos_y >= 0 or pos_y <= 21 :
    #         is_wall_left = pos_x - 1 < 0
    #         is_wall_right = pos_x + 1 == 9
    #         is_wall_bottom = pos_y + 1 == 21
    #         is_wall_top = pos_y - 1 == 0
    #         is_block_top = matrix[pos_y-1] and  matrix[pos_y-1] != 0
    #         is_block_bottom = matrix[pos_y + 1] and matrix[pos_y + 1] != 0
    #         is_block_left = matrix[pos_y][pos_x-1] and matrix[pos_y][pos_x-1] != 0
    #         is_block_right = matrix[pos_y][pos_x+1] and matrix[pos_y][pos_x+1] != 0
    #         is_sticky_top = matrix[pos_y-1] and  matrix[pos_y-1] == 0
    #         is_sticky_bottom = matrix[pos_y + 1] and matrix[pos_y + 1] == 0
    #         is_sticky_left = matrix[pos_y][pos_x-1] and matrix[pos_y][pos_x-1] == 0
    #         is_sticky_right = matrix[pos_y][pos_x+1] and matrix[pos_y][pos_x+1] == 0
    #
    #         is_sticky = is_sticky_top or is_sticky_bottom or is_sticky_left or is_sticky_right
    #
    #         is_left_blocked = is_wall_left or is_block_left
    #         is_right_blocked = is_wall_right or is_block_right
    #         is_bottom_blocked = is_wall_bottom or is_block_bottom
    #         is_top_blocked = is_wall_top or is_block_top
    #         blocked_count = [is_left_blocked, is_right_blocked, is_top_blocked, is_bottom_blocked].count(True)
    #         temp_sticky_count = [is_sticky_left, is_sticky_left, is_sticky_top, is_sticky_bottom].count(True)
    #
    #         if is_top_blocked or is_wall_top:
    #             if islef
    #
    #
    #         if blocked_count == 3:
    #             sticky = False
    #             final_count += 1
    #             sticky_count = 0
    #         elif blocked_count == 2 and 0 < temp_sticky_count > 2:
    #             sticky = True
    #             final_count += 1
    #             sticky_count = 0
    #         elif
    #
    #         if is_wall_top or is_block_top or is_sticky_top:
    #             final_count += 1
    #             sticky_count += 1
    #             sticky = True
    #         elif not is_sticky
    #
    #     if sticky is True and full is True:
    #         cou

    def holes_created_count(self):
        max_grid_bp = max(self.get_boundaries())
        radar = 4
        if max_grid_bp < 4:
            radar = max_grid_bp


        count = 0

        for col in range(len(self.matrix)):
            block = False
            row_start = (max_grid_bp-21)*-1
            row_end = (max_grid_bp-21)*-1+radar
            for row in range(row_start, row_end):
                if self.matrix[col][row] > 0:
                    block = True
                elif self.matrix[col][row] == 0 and block is True:
                    count += 1

        return count


    def is_blockade_created(self):
        pass

    def is_bumpiness_increased(self):
        return max(self.previous_boundaries) == max(self.get_boundaries())

    def set_previous_boundaries(self):
        self.previous_boundaries = self.get_boundaries()

    def try_erase_line(self, ui_configuration=None):
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
            if ui_configuration is not None:
                ui_configuration.single_sound.play()
            self.score += 50 * self.level
        elif self.erase_count == 2:
            if ui_configuration is not None:
                ui_configuration.double_sound.play()
            self.score += 150 * self.level
        elif self.erase_count == 3:
            if ui_configuration is not None:
                ui_configuration.triple_sound.play()
            self.score += 350 * self.level
        elif self.erase_count == 4:
            if ui_configuration is not None:
                ui_configuration.tetris_sound.play()
            self.score += 1000 * self.level
