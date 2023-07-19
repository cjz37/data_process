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

## 1.北京数据自带惯导轨迹
f = open("datas/odometry_loc_bj-or-ins.txt", encoding="utf-8")

data_line = f.readline()
datas1 = []
while data_line:
    d = data_line.replace('\n', '').split()
    datas1.append(d)
    data_line = f.readline()
    # print(data_line)

euler1 = []
for i in range(len(datas1)):
    temp_q = [float(datas1[i][4]), float(datas1[i][5]), float(datas1[i][6]), float(datas1[i][7])]
    r = R.from_quat(temp_q)
    temp_euler = r.as_euler('xyz', degrees=True)
    euler1.append(temp_euler)


## 2.北京数据使用我们的惯导算法出的轨迹
f = open("datas/odometry_loc_bj-cg-ins.txt", encoding="utf-8")

data_line = f.readline()
datas2 = []
while data_line:
    d = data_line.replace('\n', '').split()
    datas2.append(d)
    data_line = f.readline()
    # print(data_line)

euler2 = []
for i in range(len(datas2)):
    temp_q = [float(datas2[i][4]), float(datas2[i][5]), float(datas2[i][6]), float(datas2[i][7])]
    r = R.from_quat(temp_q)
    temp_euler = r.as_euler('xyz', degrees=True)
    euler2.append(temp_euler)


## 3. 52
f = open("/home/crange/dev/calib_ws/datas/calib_data_52/odometry_loc.txt", encoding="utf-8")
line3 = 0

data_line = f.readline()
datas3 = []
while data_line:
    d = data_line.replace('\n', '').split()
    datas3.append(d)
    data_line = f.readline()
    # print(data_line)

euler3 = []
for i in range(len(datas3)):
    temp_q = [float(datas3[i][4]), float(datas3[i][5]), float(datas3[i][6]), float(datas3[i][7])]
    r = R.from_quat(temp_q)
    temp_euler = r.as_euler('xyz', degrees=True)
    euler3.append(temp_euler)


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

x3 = []
y3 = []
for i in range(len(datas3)):
    x3.append(float(datas3[i][1]))
    y3.append(float(datas3[i][2]))

## odometry
# plt.title('odom')
# plt.scatter(x1, y1, 1, 'red', label="BJ->INS")
# plt.show()

x = []
ty1 = []
ty2 = []
ty3 = []
ty_ = []
k = 8
a = 90
for i in range(min(len(euler1), len(euler2)) - k):
    x.append(i + 1)
    ty1.append(euler1[i][2] % 360)
    ty2.append((a - euler2[i+k][2]) % 360)
    # ty3.append(euler2[i][2] % 360)
    ty_.append(euler1[i][2] % 360 - (a - euler2[i+k][2]) % 360)
plt.title('BJ-INS&MATLAB')
plt.plot(x, ty1, 1, color='green', label='BJ-INS')
plt.plot(x, ty2, 1, color='red', label='BJ-MATLAB')
# plt.plot(x, ty3, 1, color='blue', label='52-MATLAB')
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.show()

# plt.plot(x, ty_)
# plt.show()


# bag_file = "/mnt/data/UbuntuData/intron_datas/bagfiles/0219_02_calib_data_intensity-float/0219_02_new.bag"

# bag = rosbag.Bag(bag_file)
# imu = []

# for topic, msg, t in bag.read_messages():
#     if topic == "/camera/imu":
#         imu.append(msg)


# x = []
# wx = []
# wy = []
# wz = []
# ax = []
# ay = []
# az = []
# for i in range(len(imu)):
#     x.append(i + 1)
#     wx.append(imu[i].angular_velocity.x)
#     wy.append(imu[i].angular_velocity.y)
#     wz.append(imu[i].angular_velocity.z)
#     ax.append(imu[i].linear_acceleration.x)
#     ay.append(imu[i].linear_acceleration.y)
#     az.append(imu[i].linear_acceleration.z)

# plt.plot(x, wz, linewidth=0.5)
# plt.show()

