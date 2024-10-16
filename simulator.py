import requests 
import json

token = "5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3"

maze_dict = {0:[1,1,1,1],1:[1,1,1,0]}#МЫШЬ СМОТРИТ НА СЕВЕР!!!!!!!!
class Maze_bot():
    def __init__(self,token):
        self.token = token
        self.position_x = 0
        self.position_y = 15
        self.central_point = [7,8]
        self.map_encoder_dict = {
            "[0, 0, 0, 0]":0,
            "[0, 0, 0, 1]":1,
            "[1, 0, 0, 0]":2,
            "[0, 1, 0, 0]":3,
            "[0, 0, 1, 0]":4,
            "[0, 0, 1, 1]":5,
            "[0, 1, 1, 0]":6,
            "[1, 1, 0, 0]":7,
            "[1, 0, 0, 1]":8,
            "[0, 1, 0, 1]":9,
            "[1, 0, 1, 0]":10,
            "[1, 1, 1, 0]":11,
            "[1, 1, 0, 1]":12,
            "[1, 0, 1, 1]":13,
            "[0, 1, 1, 1]":14,
            "[1, 1, 1, 1]":15,
        }
        
        self.map = [[[1,1,1,1] for _ in range(16)] for _ in range(16)]#задаем изначальное состояние карты - все клетки отмечены как непосещенные
        self.route = []

    def restart(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/restart?token={self.token}")
        return response.content
    def move_forward(self):#Движение вперед
        wall_config = self.sensor_data["current_wall_config"]
        yaw = self.sensor_data["yaw"]
        if wall_config[0] == 0:
            response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/forward?token={self.token}")
            moving = [0,-1]
            rotated_moving = self.rotate_movement_vector(yaw,moving)
            self.position_x+=rotated_moving[0]
            self.position_y+=rotated_moving[1]
            self.route.append([self.position_x,self.position_y])
        self.sensor_data  = self.get_sensor_data_converted()
        
    def move_backward(self):#движение назад
        wall_config = self.sensor_data["current_wall_config"]
        yaw = self.sensor_data["yaw"]
        if wall_config[3] == 0:
            requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/backward?token={self.token}")
            moving = [0,1]
            rotated_moving = self.rotate_movement_vector(yaw,moving)
            self.position_x+=rotated_moving[0]
            self.position_y+=rotated_moving[1]
            self.route.append([self.position_x,self.position_y])
        self.sensor_data  = self.get_sensor_data_converted()
        
    def turn_left(self):#Поворот налево
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/left?token={self.token}")
        self.sensor_data  = self.get_sensor_data_converted()
    def turn_right(self):#поворот направо
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/right?token={self.token}")
        self.sensor_data  = self.get_sensor_data_converted()
    def get_sensor_data(self):#получить сырые данные с сенсора
        response = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token={self.token}")
        return json.loads(response.content)
    def get_sensor_data_converted(self):#функция которая возвращает sensor_data относительно ячееки матрицы info_mode просто возращает значения но не изменяют соответтвующее поле объекта
        data = self.get_sensor_data()
        data_dist = [data["front_distance"],data["right_side_distance"],data["back_distance"],data["left_side_distance"]]
        converted_data_dist = []
        for dist in data_dist:
            converted_data_dist.append(round((dist-5)/16.6))
        yaw = data["rotation_yaw"]
        current_wall_config_north,current_wall_config=self.get_current_wall_config(converted_data_dist,yaw)

        offset_x = self.central_point[0]-self.position_x
        offset_y = self.central_point[1]-self.position_y
        converted_data = {"position_x":self.position_x,"position_y":self.position_y,"offset_x":offset_x,"offset_y":offset_y,"current_wall_config":current_wall_config,"current_wall_config_north":current_wall_config_north,"yaw": yaw}
        self.sensor_data  = converted_data
        return converted_data


    def rotate_movement_vector(self,yaw,moving):
        # Определяем сдвиг вектора движения в зависимости от yaw
        shift = int(yaw) // 90

        # Создаем список направлений движения
        directions = [moving, [-moving[1], 0], [0, -moving[1]], [moving[1], 0]]

        return directions[shift]

    def get_current_wall_config(self,data_dist,yaw):#функция возвращающая положение стен в текущей конфигурации
        wall_config = []
        for distance in data_dist:
            if distance < 1:#там где расстояние равно 0 стена
                wall_config.append(1)
            else:
                wall_config.append(0)

        #повораиваем данные относительно севера
        rotated_config = self.rotate_wall_config(wall_config, yaw)
        self.map[self.position_x][self.position_y] = rotated_config
        return rotated_config,wall_config#Возращаем конфигурацию стен относительно севера и относительно робота
        
    def rotate_wall_config(self,wall_config, yaw):
        # Определяем, на сколько позиций нужно сдвинуть конфигурацию стен
        shift = int(yaw) // 90
        # Если угол поворота больше 180 градусов, сдвигаем элементы в обратном направлении
        #if yaw > 180:
        shift = 4 - shift
        # Циклически сдвигаем элементы списка на указанное число позиций
        #print(shift)
        #print(wall_config[shift:])
        rotated_config = wall_config[shift:]+wall_config[:shift]
        return rotated_config
    def encode_map(self):
        encoded_map = [[15 for _ in range(16)] for _ in range(16)]
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                encoded_map[x][y] = self.map_encoder_dict[str(self.map[x][y])]
        return encoded_map

    

def iter_test(controller,method):
    method()
    data = controller.get_sensor_data_converted()
    return data


if False:
    controller = Maze_bot(token)
    config =[0,0,1,0]
    yaw = 270
    print(controller.rotate_wall_config(config,yaw))

    controller.restart()

    print('------------------------------------------------------')
    print('Начало испытания')
    res = controller.get_sensor_data_converted()
    print(res)
    print('------------------------------------------------------')
    print('Направо')
    res = iter_test(controller,controller.turn_right)
    print(res)
    print('------------------------------------------------------')
    print('Вперед')
    res = iter_test(controller,controller.move_forward)
    print(res)
    print('------------------------------------------------------')
    print('Вперед')
    res = iter_test(controller,controller.move_forward)
    print(res)
    print('------------------------------------------------------')
    print('Вперед')
    res = iter_test(controller,controller.move_forward)
    print(res)
    print("Result")
    print('------------------------------------------------------')
    print(controller.route)
    #print(controller.map)
