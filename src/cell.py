from graphics import Line, Point

class Cell:
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.top_left_point = None
        self.top_right_point = None
        self.bot_left_point = None
        self.bot_right_point = None

        self.center_point = None

        self.win = window

    def draw(self, x1, y1, x2, y2):
        #setting points of the cell up
        self.top_left_point = Point(x1, y1)
        self.top_right_point = Point(x2, y1)
        self.bot_left_point = Point(x1, y2)
        self.bot_right_point = Point(x2, y2)

        #drawing walls if they exist
        if self.has_left_wall:
            left_wall = Line(self.top_left_point, self.bot_left_point)
            self.win.draw_line(left_wall)
        if self.has_top_wall:
            top_wall = Line(self.top_left_point, self.top_right_point)
            self.win.draw_line(top_wall)
        if self.has_right_wall:
            right_wall = Line(self.top_right_point, self.bot_right_point)
            self.win.draw_line(right_wall)
        if self.has_bottom_wall:
            bot_wall = Line(self.bot_left_point ,self.bot_right_point)
            self.win.draw_line(bot_wall)

    def draw_move(self, to_cell, undo = False):
        half_length1 = abs(self.top_right_point.x - self.top_left_point.x) // 2
        x_center1 = half_length1 + self.top_left_point.x
        y_center1 = half_length1 + self.top_left_point.y

        half_length2 = abs(to_cell.top_right_point.x - to_cell.top_left_point.x) // 2
        x_center2 = half_length2 + to_cell.top_left_point.x
        y_center2 = half_length2 + to_cell.top_left_point.y

        self.center_point = Point(x_center1, y_center1)
        to_cell.center_point = Point(x_center2, y_center2)

        c2c_line = Line(self.center_point, to_cell.center_point)
        fill_color = "red"
        if undo:
            fill_color = "gray"
        self.win.draw_line(c2c_line, fill_color)