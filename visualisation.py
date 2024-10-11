import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos
import numpy as np
from simulator import Maze_bot
from array import array

class Visualisation():

    def __init__(self, robot:Maze_bot):
        self.robot = robot

        self.x = [i[0] for i in robot.route] * 166
        self.y = [i[1] for i in robot.route] * 166

        # Размер клетки и толщина границы
        self.cell_size = 156
        self.border_width = 10

        # Размеры лабиринта
        self.rows = 16
        self.cols = 16

        self.map = robot.map

        # plt.ion()
        plt.show(block=False)

    def max_data(self):
        print("max x: " + str(max(self.x)))
        print("max y: " + str(max(self.y)))

    def min_data(self):
        print("min x: " + str(min(self.x)))
        print("min y: " + str(min(self.y)))

    def draw_left_border(self, i, j, image):
        x = j * self.cell_size + (j) * self.border_width
        y = i * self.cell_size + (i + 1) * self.border_width
        image[y:y + self.cell_size + self.border_width, x:x + self.border_width] = 1

    def draw_right_border(self, i, j, image):
        x = (j + 1) * self.cell_size + (j + 1) * self.border_width
        y = i * self.cell_size + (i + 1) * self.border_width
        image[y:y + self.cell_size + self.border_width, x:x + self.border_width] = 1

    def draw_up_border(self, i, j, image):
        x = j * self.cell_size + (j + 1) * self.border_width
        y = i * self.cell_size + (i + 1) * self.border_width
        image[y:y + self.border_width, x:x + self.cell_size + self.border_width] = 1

    def draw_down_border(self, i, j, image):
        x = j * self.cell_size + (j + 1) * self.border_width
        y = (i + 1) * self.cell_size + (i + 1) * self.border_width
        image[y:y + self.border_width, x:x + self.cell_size + self.border_width] = 1

    def draw_maze(self):
        # Размер изображения с учетом границ
        image_size = (self.rows * self.cell_size + (self.rows + 1) * self.border_width,
                    self.cols * self.cell_size + (self.cols + 1) * self.border_width)
        # print(image_size)
        # Создание изображения с белым фоном
        image = np.zeros(image_size)

        # Рисование границ клеток черным цветом
        for i in range(self.rows):
            for j in range(self.cols):
                n = i
                m = j + 1
                if self.map[i][j][0] == 1:
                    self.draw_up_border(m, n, image)
                if self.map[i][j][1] == 1:
                    self.draw_right_border(m, n, image)
                if self.map[i][j][2] == 1:
                    self.draw_down_border(m, n, image)
                if self.map[i][j][1] == 1:
                    self.draw_left_border(m, n, image)
        
        plt.imshow(image, cmap='binary', interpolation='nearest')

    def draw(self):
        self.x = [(i[0] - self.robot.route[0][0]) * 166 + 83 for i in self.robot.route]
        self.y = [(i[1] - self.robot.route[0][1] + 16) * 166 - 83 for i in self.robot.route]
        self.draw_maze()
        if len(self.x) > 0:
            plt.plot(self.x, self.y, marker='o', color='r', linewidth=1.5)
        # plt.draw()
        plt.pause(0.001)

    def find_delta(self):
        delta_average = 0
        count = 0
        for i in range(1, len(self.data)):
            delta = max(abs(self.x[i] - self.x[i-1]), abs(self.y[i] - self.y[i-1]))
            if delta != 0:
                delta_average += delta
                count += 1
                print(delta)
        delta_average = delta_average / count
        print("Среднее значение передвижения робота: " + str(delta_average))
