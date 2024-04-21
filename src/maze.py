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
        self._reset_cells_visited()
    
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

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def is_wall_between(self, cell_coord, i, j):
        cur_cell = self._cells[i][j]
        #left from cur
        if cell_coord[0] < i:
            return cur_cell.has_left_wall
        #up from cur
        if cell_coord[1] < j:
            return cur_cell.has_top_wall
        #right from cur
        if cell_coord[0] > i:
            return cur_cell.has_right_wall
        #down from cur
        if cell_coord[1] > j:
            return cur_cell.has_bottom_wall

    def solve(self):
        if self._solve_r(0,0) == True:
            print("You've Reached the Finish!")
            return True
        else:
            return False
    
    def _solve_r(self,i,j):
        self._animate()
        cur_cell = self._cells[i][j]
        cur_cell.visited = True
        end_cell = self._cells[self._num_cols-1][self._num_rows-1]

        if cur_cell == end_cell:
            return True
        else:
            cells_to_move_to = []
            directions = []
            coords= []
            #load possible directions and their coords in the grid
            if i-1 >= 0: 
                directions.append("left")
                cells_to_move_to.append(self._cells[i-1][j])
                coords.append((i-1, j))
            if  j-1 >= 0:
                directions.append("up")
                cells_to_move_to.append(self._cells[i][j-1])
                coords.append((i, j-1))
            if i+1 <= self._num_cols-1:
                directions.append("right")
                cells_to_move_to.append(self._cells[i+1][j])
                coords.append((i+1, j))
            if j+1 <= self._num_rows-1:
                directions.append("down")
                cells_to_move_to.append(self._cells[i][j+1])
                coords.append((i, j+1))

            cell_coord = ()
            if len(directions) != 0:
                #for each direction
                for to_cell in cells_to_move_to:
                    cell_coord = coords.pop(0)
                    direction = directions.pop(0)
                    #no wall and the cell hasnt been visited
                    if self.is_wall_between(cell_coord, i, j) == False and to_cell.visited == False:
                        #draw a move
                        cur_cell.draw_move(to_cell)
                        #move with to the cell
                        #is the desitination a dead end?
                        if self._solve_r(cell_coord[0], cell_coord[1]) == False:
                            dead_end_cell = self._cells[cell_coord[0]][cell_coord[1]]
                            dead_end_cell.draw_move(cur_cell, True) 
                        else:
                            return True
                #no directions were successful, mark cur_cell as not visited and return False to show that cur_cell is a dead end?
                cur_cell.visited = False
                return False
                
            
