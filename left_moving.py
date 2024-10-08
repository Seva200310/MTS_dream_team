import requests 
import json
from pandas_loger import Pandas_loger
from simulator import Robot_controller

token = "5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3"


class left_move_algo():
    def __init__(self, length_cell):
        self.controller = Robot_controller(token)
        self.controller.restart()
        self.loger = Pandas_loger()
        self.length_cell = length_cell#ширина ячейки, максимальная величина до стенки после которой невозможно двигаться вперед
    def change_direction(self):# выбор направления следующего шага
        location = self.controller.get_sensor_data()
        #print(location,self.length_cell)
        if (location["left_side_distance"]>self.length_cell):
            return 1
        if (location["front_distance"]>self.length_cell):
            return 2
        if (location["right_side_distance"]>self.length_cell):
            return 3
        if (location["back_distance"]>self.length_cell):
            return 4
    def get_data(self):# получение данных о текущем шаге
        location = self.controller.get_sensor_data()
        row = {"down_x_offset":location["down_x_offset"],
                "down_y_offset":location["down_y_offset"],
                "left_side_distance":location["left_side_distance"],
                "right_side_distance":location["right_side_distance"],
                "rotation_yaw":location["rotation_yaw"]}
        self.loger.add_row(row)
        return 
    def moving(self):#хождение по кругу
        for i in range(50):
            self.get_data()
            #print(self.change_direction())
            if self.change_direction() == 1:
                self.controller.turn_left()
                self.controller.move_forward()
            if self.change_direction() == 2:
                self.controller.move_forward()
            if self.change_direction() == 3:
                self.controller.turn_right()
                self.controller.move_forward()
            if self.change_direction() == 4:
                self.controller.turn_left()
                self.controller.turn_left()
                self.controller.move_forward()
        self.loger.save_csv()

        


        
#left_move_algo(5).moving()
    

#response = requests.post("http://127.0.0.1:8801/api/v1/robot-python/restart?token=5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3")