import time
import random
from cell import Cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        
        if (seed != None):
            random.seed(seed)
            self._seed = seed
        else:
            self._seed = 0

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
    
    def _create_cells(self):
        for i in range(self._num_cols):
            cells_in_col = []
            for j in range(self._num_rows):
                cells_in_col.append(Cell(self._win))            
            self._cells.append(cells_in_col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        top_left_x = self._x1 + (i * self._cell_size_x)
        top_left_y = self._y1 + (j * self._cell_size_y)
        bot_right_x = top_left_x + self._cell_size_x
        bot_right_y = top_left_y + self._cell_size_y
        
        self._cells[i][j].draw(top_left_x, top_left_y, bot_right_x, bot_right_y)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        bot_right_cell = self._cells[self._num_cols-1][self._num_rows-1]
        top_left_cell.has_top_wall = False
        self._draw_cell(0,0)
        bot_right_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        cur_cell = self._cells[i][j]
        cur_cell.visited = True
        while True:
            #empty list of tuples that contain (i,j)
            to_visit = []
            
            if i-1 >= 0: 
                #check if left is visited
                if self._cells[i-1][j].visited == False:
                    to_visit.append((i-1, j))
            if  j-1 >= 0:
                #check if top is visited
                if self._cells[i][j-1].visited == False:
                    to_visit.append((i, j-1))
            if i+1 <= self._num_cols-1:
                #check if right is visited
                if self._cells[i+1][j].visited == False:
                    to_visit.append((i+1, j))
            if j+1 <= self._num_rows-1:
                #check if bottom is visited
                if self._cells[i][j+1].visited == False:
                    to_visit.append((i, j+1))
            
            if len(to_visit) == 0:
                self._draw_cell(i,j)
                return
            else:
                r_dir = to_visit[random.randrange(len(to_visit))]
                chosen_cell = self._cells[r_dir[0]][r_dir[1]]

            #check the direction of movment to get the walls
                #left from cur
                if r_dir[0] < i:
                    cur_cell.has_left_wall = False
                    chosen_cell.has_right_wall = False
                #up from cur
                if r_dir[1] < j:
                    cur_cell.has_top_wall = False
                    chosen_cell.has_bottom_wall = False
                #right from cur
                if r_dir[0] > i:
                    cur_cell.has_right_wall = False
                    chosen_cell.has_left_wall = False
                #down from cur
                if r_dir[1] > j:
                    cur_cell.has_bottom_wall = False
                    chosen_cell.has_top_wall = False
                #redraw cells
                self._draw_cell(i, j)
                self._draw_cell(r_dir[0],r_dir[1])
                self._break_walls_r(r_dir[0],r_dir[1])
