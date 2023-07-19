import math
import csv
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import rosbag
from sensor_msgs.msg import Imu, NavSatFix
import scipy.io as sio
import numpy as np
from collections import OrderedDict

data_path = '/home/crange/dev/calib_ws/datas/calib_data_52_best'

## 1.ins
f = open(data_path + '/odometry_loc_ori.txt', encoding="utf-8")

data_line = f.readline()
datas1 = []
while data_line:
    d = data_line.replace('\n', '').split("\t")
    datas1.append(d)
    data_line = f.readline()
    # print(data_line)

euler1 = []
for i in range(len(datas1)):
    temp_q = [float(datas1[i][4]), float(datas1[i][5]), float(datas1[i][6]), float(datas1[i][7])]
    r = R.from_quat(temp_q)
    temp_euler = r.as_euler('xyz', degrees=True)
    euler1.append(temp_euler)


## 2.lidar_slam
f = open(data_path + '/lidar_slam_pose.txt', encoding="utf-8")

data_line = f.readline()
datas2 = []
while data_line:
    d = data_line.replace('\n', '').split("\t")
    datas2.append(d)
    data_line = f.readline()
    # print(data_line)

euler2 = []
for i in range(len(datas2)):
    temp_q = [float(datas2[i][4]), float(datas2[i][5]), float(datas2[i][6]), float(datas2[i][7])]
    r = R.from_quat(temp_q)
    temp_euler = r.as_euler('xyz', degrees=True)
    euler2.append(temp_euler)

x1 = []
y1 = []
for i in range(len(datas1)):
    x1.append(float(datas1[i][1]))
    y1.append(float(datas1[i][2]))

x2 = []
y2 = []
for i in range(len(datas2)):
    x2.append(float(datas2[i][1]))
    y2.append(float(datas2[i][2]))

x = []
ty1 = []
ty2 = []
k = 0
a = 0
for i in range(min(len(euler1), len(euler2)) - k):
    x.append(i + 1)
    ty1.append((a + euler1[i+k][2]))
    ty2.append(euler2[i][2])
plt.title('INS&Lidar_SLAM')
plt.scatter(x, ty1, 0.2, color='green', label='INS')
plt.scatter(x, ty2, 0.2, color='red', label='Lidar_SLAM')
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.show()

# plt.plot(x, ty_)
# plt.show()

