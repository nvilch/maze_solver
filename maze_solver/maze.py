from time import sleep
from cell import Cell
import random

class Maze:
    def __init__(
            self
            ,x1
            ,y1
            ,num_rows
            ,num_cols
            ,cell_size_x
            ,cell_size_y
            ,win=None
            ,seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    
    def _create_cells(self):
        for i in range(self._num_cols):
            self._cells.append([]) 
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x_position = self._x1 + self._cell_size_x * i
        y_position = self._y1 + self._cell_size_y * j
        x2_position = x_position + self._cell_size_x
        y2_position = y_position + self._cell_size_y
        self._cells[i][j].draw(x_position, y_position, x2_position, y2_position)
        self._animate()

    def _break_entrance_and_exit(self):
        # Remove the top from the top-left cell
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        # Remove the bottom wall from the right-bottom cell
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            to_visit_count = 0

            # move to the left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append([i - 1, j])
                to_visit_count += 1

            # move to the right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append([i + 1, j])
                to_visit_count += 1

            # move up
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append([i, j - 1])
                to_visit_count += 1
            
            # move down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append([i, j + 1])
                to_visit_count += 1
            
            # if the to_visit list is empty then there are no other cells that can be moved into
            if not to_visit: 
                self._draw_cell(i, j)
                return
            
            next_cell_ind = random.randint(0, len(to_visit) - 1)

            # break wall to the left of current cell
            if to_visit[next_cell_ind][0] < i:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            # break wall to the right of current cell
            if to_visit[next_cell_ind][0] > i:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            # break wall that is above cell
            if to_visit[next_cell_ind][1] < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # break wall that is below of current cell
            if to_visit[next_cell_ind][1] > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            self._break_walls_r(to_visit[next_cell_ind][0], to_visit[next_cell_ind][1])


    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.000000000005)


    def _reset_cells_visited(self):
        # Resets all the visited cells back to false
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        solved = self._solve_r(i=0, j=0)
        return solved
    
    def _solve_r(self, i, j):
        # Implement a BFS algorithm to find a solution to the maze
        self._animate()
        self._cells[i][j].visited = True
        if (i == self._num_cols - 1) and (j == self._num_rows - 1):
            return True

        # check if cell above is feasible
        if (j > 0) and (not self._cells[i][j - 1].visited) and (not self._cells[i][j].has_top_wall) and (not self._cells[i][j - 1].has_bottom_wall):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            can_move_to_cell = self._solve_r(i, j - 1)
            if can_move_to_cell:
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # check if cell below is feasible
        if (j < self._num_rows - 1) and (not self._cells[i][j + 1].visited) and (not self._cells[i][j].has_bottom_wall) and (not self._cells[i][j + 1].has_top_wall):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            can_move_to_cell = self._solve_r(i, j + 1)
            if can_move_to_cell:
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        # check if cell to the left is feasible
        if (i > 0) and (not self._cells[i - 1][j].visited) and (not self._cells[i][j].has_left_wall) and (not self._cells[i - 1][j].has_right_wall):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            can_move_to_cell = self._solve_r(i - 1, j)
            if can_move_to_cell:
                return True 
            self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
        
        # check if cell to the right is feasible
        if (i < self._num_cols - 1) and (not self._cells[i + 1][j].visited) and (not self._cells[i][j].has_right_wall) and (not self._cells[i + 1][j].has_left_wall):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            can_move_to_cell = self._solve_r(i + 1, j)
            if can_move_to_cell:
                return True 
            self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
        
        # if none of the cells around are feasible to move into then return false
        return False