from simulator import Maze_bot
class Tremaux(Maze_bot):
    def __init__(self,token):
        super().__init__(token)
        self.cells_visit_map = [[0 for _ in range(16)] for _ in range(16)]#задаем изначальное состояние карты - все клетки отмечены как непосещенные
        self.token = token
    def make_decision(self):

    def mark_cell(self):#Помечаем 
        self.cells_visit_map[self.position_x][self.position_y] +=1
    def check_impass(self):
        pass
    def check_crossroad(self):
        pass
    def find_ways_from_cell(self):
        pass
    


token = "5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3"
alg = Tremaux(token)
