import pandas as pd

class Pandas_loger():
    def __init__(self):
        self.data = pd.DataFrame(columns = ['down_x_offset','down_y_offset','left_side_distance','right_side_distance','rotation_yaw'])
    def add_row(self,row):
        #self.data.append(sensor_data)
        self.data = pd.concat([self.data, pd.DataFrame(row, index=[0])], ignore_index=True)
    def save_csv(self):
        self.data.to_csv("route_log.csv")

if __name__ == 'main':
    loger = Pandas_loger()
    row = {'down_x_offset':-90,'down_y_offset':10,'left_side_distance':22,'right_side_distance':-9,'rotation_yaw':10}
    loger.add_row(row)
    row = {'down_x_offset':-90,'down_y_offset':10,'left_side_distance':22,'right_side_distance':-9,'rotation_yaw':10}
    loger.add_row(row)
    row = {'down_x_offset':-90,'down_y_offset':10,'left_side_distance':22,'right_side_distance':-9,'rotation_yaw':10}
    loger.add_row(row)
    row = {'down_x_offset':-90,'down_y_offset':10,'left_side_distance':22,'right_side_distance':-9,'rotation_yaw':10}
    loger.add_row(row)
    #row = [90,10,22,9,10]
    loger.save_csv()
