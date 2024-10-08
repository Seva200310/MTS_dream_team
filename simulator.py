import requests 
import json

token = "5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3"


class Robot_controller():
    def __init__(self,token):
        self.token = token
    def restart(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/restart?token={self.token}")
        return response.content
    def move_forward(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/forward?token={self.token}")
        return response.content
    def move_backward(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/backward?token={self.token}")
        return response.content
    def turn_left(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/left?token={self.token}")
        return response.content
    def turn_right(self):
        response = requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/right?token={self.token}")
        return response.content
    def get_sensor_data(self):
        response = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token={self.token}")
        return json.loads(response.content)

controller = Robot_controller(token)
response = controller.get_sensor_data()
#response = requests.post("http://127.0.0.1:8801/api/v1/robot-python/restart?token=5035d904-c58d-4e7f-a1bd-bcaf5d6c0bbd70b4e88a-2054-47b0-a4c3-d7950f5e4da3")
print(response)