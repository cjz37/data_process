import rosbag
import scipy.io as sio
import matplotlib.pyplot as plt


bag_file = "datas/2023-07-13-14-19-21.bag"

bag = rosbag.Bag(bag_file)
bno055_imu_raw = []
xsense_imu_raw = []

for topic, msg, t in bag.read_messages():
    if topic == "/bno055_imu/raw":
        bno055_imu_raw.append(msg)
    elif topic == "/imu/data":
        xsense_imu_raw.append(msg)

print(len(bno055_imu_raw), len(xsense_imu_raw))

xsense = []
bno055 = []
x = []
j = 0
for i in range(len(bno055_imu_raw)):
    x.append(i)
    bno055.append([i, 
                   bno055_imu_raw[i].angular_velocity.x, bno055_imu_raw[i].angular_velocity.y, bno055_imu_raw[i].angular_velocity.z])
    xsense.append([i, 
                   xsense_imu_raw[j].angular_velocity.x, xsense_imu_raw[j].angular_velocity.y, xsense_imu_raw[j].angular_velocity.z])
    j += 2

# 1:x; 2:y; 3:z
t = 1

y1 = []
y2 = []
for i in range(len(bno055)):
    y1.append(float(xsense[i][t]))
    y2.append(float(bno055[i][t]))
if 1 == t:
    plt.title("x angular velocity")
elif 2 == t:
    plt.title("y angular velocity")
elif 3 == t:
    plt.title("z angular velocity")
plt.plot(x, y1, label="xsense", linewidth=0.5)
plt.plot(x, y2, label="bno055", linewidth=0.5)
plt.legend()
plt.show()
