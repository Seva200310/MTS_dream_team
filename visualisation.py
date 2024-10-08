import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos

data = pd.read_csv("data.csv", delimiter=",", decimal='.')
x = data["down_x_offset"]
y = data["down_y_offset"]

dist_left = data["left_side_distance"]
dist_right = data["right_side_distance"]

rot = data["rotation_yaw"]

walls_left_x = []
walls_left_y = []
walls_right_x = []
walls_right_y = []

for i in range(len(data)):
    walls_left_x.append(x[i] - cos(rot[i])*dist_left[i])
    walls_right_x.append(x[i] + cos(rot[i])*dist_right[i])
    walls_left_y.append(y[i] + sin(rot[i])*dist_left[i])
    walls_right_y.append(y[i] - sin(rot[i])*dist_right[i])

plt.ylim(-150, 150)
plt.xlim(-150, 150)

plt.plot(x, y, marker='o', color='r', linewidth=1.5)
plt.plot(walls_left_x, walls_left_y, color='g', linewidth=1.5)
plt.plot(walls_right_x, walls_right_y, color='g', linewidth=1.5)
