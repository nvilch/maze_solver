from grid import Window
from maze import Maze
import sys

def main():

    window_width = 1200
    window_height = 800
    starting_x = 50
    starting_y = 50
    num_rows = 100
    num_cols = 100
    cell_size_x = (window_width - (starting_x * 2))/num_cols
    cells_size_y = (window_height - (starting_y * 2))/num_rows

    sys.setrecursionlimit(10000)

    window = Window(window_width, window_height)
    maze = Maze(x1=starting_x, y1=starting_y,num_rows=num_rows, num_cols=num_cols, cell_size_x=cell_size_x, cell_size_y=cells_size_y, win=window)

    result = maze.solve()
    print(f"Maze was solved?\n{result}!")

    window.wait_for_close()

main()