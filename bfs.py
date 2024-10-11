from simulator import Maze_bot
from visualisation import Visualisation
import matplotlib.pyplot as plt

class BFS(Maze_bot):

    def __init__(self, token):
        super().__init__(token)
        self.queue = []
        self.add_queue()
        self.visited = set()
        self.visual = Visualisation(self)
        self.prev_draw = 0

    def add_queue(self):
        res = self.get_sensor_data_converted()
        x = res["position_x"]
        y = res["position_y"]
        walls   = res["current_wall_config"]
        """if walls == [1, 1, 1, 1]:
            walls = [0, 0, 0, 0]"""
        #with open("data_raw_log.txt","a") as f:
            #data = self.sensor_data
            #f.write(f"{data['position_x']},{data['position_y']},{data['current_wall_config'],{data['yaw']}} \n")
        self.queue.append((x, y, walls))

    def move_robot_forward(self):
        # print("NORTH")
        self.move_forward()

    def move_robot_right(self):
        # print("EAST")
        self.turn_right()
        self.move_forward()
        self.turn_left()

    def move_robot_backward(self):
        # print("SOURTH")
        # self.move_backward()
        self.turn_right()
        self.turn_right()
        self.move_forward()
        self.turn_left()
        self.turn_left()

    def move_robot_left(self):
        # print("WEST")
        self.turn_left()
        self.move_forward()
        self.turn_right()

    def algo(self):
        while len(self.visited) != 256:
            # if len(self.visited) % 10 == 0 and not self.prev_draw:
            #     self.visual.draw()
            #     self.prev_draw = 1
            # else:
            #     self.prev_draw = 0
            # self.visual.draw()

            current_x, current_y, current_direction = self.queue[-1]
            # self.map[current_x][current_y] = current_direction

            self.visited.add((current_x, current_y))

            # print("Current coordinates: " + str((current_x, current_y)))
            # print("quere: " + str(self.queue))
            # print("visited: " + str(self.visited))
            
            # Добавление соседних клеток в очередь и их прохождение 
            if (current_x, current_y - 1) not in self.visited and current_direction[0] == 0:
                self.move_robot_forward()
                self.add_queue()
                continue

            if (current_x + 1, current_y) not in self.visited and current_direction[1] == 0:
                self.move_robot_right()
                self.add_queue()
                continue

            if (current_x, current_y + 1) not in self.visited and current_direction[2] == 0:
                self.move_robot_backward()
                self.add_queue()
                continue

            if (current_x - 1, current_y) not in self.visited and current_direction[3] == 0:
                self.move_robot_left()
                self.add_queue()
                continue

            # # Текущая клетка
            # Текущую клетку надо удалить из self.queue
            self.queue.pop()
            # # Предыдущая клетка
            # Предыдущую надо оставить
            prev_x, prev_y, prev_direction = self.queue[-1]
            # print("quere: " + str(self.queue))
            # Идем в предыдущую клетку
            if  current_y - prev_y == 1:
                self.move_robot_forward()
                continue

            if  prev_x - current_x == 1:
                self.move_robot_right()
                continue

            if  prev_y - current_y == 1:
                self.move_robot_backward()
                continue

            if  current_x - prev_x:
                self.move_robot_left()
                continue

            # print('------------------------------------------------------')
        #print('--------------------------queu----------------------------')
        #print(self.queue)
        #print('--------------------------map----------------------------')
        #print(self.map)
        return self.encode_map()
        
        #self.visual.draw()
        #plt.show(block=True)

token = "5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3"
alg = BFS(token)
alg.restart()
res = alg.algo()
print(res)
