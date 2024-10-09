import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos

class Visualisation():

    def __init__(self, file):

        self.data = pd.read_csv(file, delimiter=",", decimal='.')
        self.x = self.data["down_x_offset"]
        self.y = self.data["down_y_offset"]

        self.dist_left = self.data["left_side_distance"]
        self.dist_right = self.data["right_side_distance"]

        self.rot = self.data["rotation_yaw"]

    def draw(self):
        walls_left_x = []
        walls_left_y = []
        walls_right_x = []
        walls_right_y = []

        for i in range(len(self.data)):
            walls_left_x.append(self.x[i] - cos(self.rot[i])*self.dist_left[i])
            walls_right_x.append(self.x[i] + cos(self.rot[i])*self.dist_right[i])
            walls_left_y.append(self.y[i] + sin(self.rot[i])*self.dist_left[i])
            walls_right_y.append(self.y[i] - sin(self.rot[i])*self.dist_right[i])

        plt.ylim(-150, 150)
        plt.xlim(-150, 150)

        plt.plot(self.x, self.y, marker='o', color='r', linewidth=1.5)
        plt.plot(walls_left_x, walls_left_y, color='g', linewidth=1.5)
        plt.plot(walls_right_x, walls_right_y, color='g', linewidth=1.5)
