from grid import Line, Point

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.visited = False
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, 'white')

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, 'white')

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, 'white')

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, 'white')

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return 
        
        line_color = "red"
        if undo:
            line_color = "gray"
        
        current_cell_x_midpoint = (self._x2 + self._x1)/2
        current_cell_y_midpoint = (self._y2 + self._y1)/2

        to_cell_x_midpoint = (to_cell._x2 + to_cell._x1)/2
        to_cell_y_midpoint = (to_cell._y2 + to_cell._y1)/2

        # Moving to the left
        if self._x1 > to_cell._x1:
            line = Line(Point(self._x1, current_cell_y_midpoint), Point(current_cell_x_midpoint, current_cell_y_midpoint))
            self._win.draw_line(line, line_color)
            line = Line(Point(to_cell_x_midpoint, to_cell_y_midpoint), Point(to_cell._x2, to_cell_y_midpoint))
            self._win.draw_line(line, line_color)
        # Moving to the right
        elif self._x1 < to_cell._x1:
            line = Line(Point(current_cell_x_midpoint, current_cell_y_midpoint), Point(to_cell._x1, to_cell_y_midpoint))
            self._win.draw_line(line, line_color)
            line = Line(Point(to_cell._x1, to_cell_y_midpoint), Point(to_cell_x_midpoint, to_cell_y_midpoint))
            self._win.draw_line(line, line_color)
        # Moving down
        elif self._y1 < to_cell._y1:
            line = Line(Point(current_cell_x_midpoint, current_cell_y_midpoint), Point(current_cell_x_midpoint, to_cell._y1))
            self._win.draw_line(line, line_color)
            line = Line(Point(to_cell_x_midpoint, to_cell_y_midpoint), Point(to_cell_x_midpoint, to_cell._y1))
            self._win.draw_line(line, line_color)
        # Moving up
        elif self._y1 > to_cell._y1:
            line = Line(Point(current_cell_x_midpoint, current_cell_y_midpoint), Point(current_cell_x_midpoint, to_cell._y2))
            self._win.draw_line(line, line_color)
            line = Line(Point(to_cell_x_midpoint, to_cell._y2), Point(to_cell_x_midpoint, to_cell_y_midpoint))
            self._win.draw_line(line, line_color)


