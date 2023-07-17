## enu_to_wgs84
# trans_enu_to_wgs84 = Transformer.from_crs(enu_crs, wgs84_crs)

# enu_x = 500.0
# enu_y = 1000.0
# enu_z = 200.0

# wgs84_lon, wgs84_lat, wgs84_alt = trans_enu_to_wgs84.transform(enu_x, enu_y, enu_z)

# print("WGS84经度: ", wgs84_lon)
# print("WGS84纬度: ", wgs84_lat)
# print("WGS84高程: ", wgs84_alt)

## wgs84_to_enu
# load gps info: lat lon alt


from pyproj import CRS, Transformer
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import math

enu_crs = CRS.from_string("+proj=utm +zone=50 +ellps=GRS80 +units=m +no_defs")
wgs84_crs = CRS.from_string("+proj=longlat +datum=WGS84 +no_defs")

te = 1e+9
theta = 0
rotation_z = np.mat([[math.cos(theta), math.sin(theta), 0],
                     [-math.sin(theta), math.cos(theta), 0],
                     [0, 0, 1]])

bno055_savepath = "/home/crange/dev/python/output/bno055.mat"
gps_savepath = "/home/crange/dev/python/output/gps.mat"


load_gps = sio.loadmat(gps_savepath)
load_imu = sio.loadmat(bno055_savepath)

gps = [load_gps["Longitude"][0], load_gps["Latitude"][0], load_gps["Altitude"][0]]

trans_wgs84_to_enu = Transformer.from_crs(wgs84_crs, enu_crs)

enu_x_base , enu_y_base, enu_z_base = trans_wgs84_to_enu.transform(gps[0][0], gps[1][0], gps[2][0])
enu_x = []
enu_y = []
enu_z = []
for i in range(len(gps[0])):
	## lon lat alt
    temp_enu_x , temp_enu_y, temp_enu_z = trans_wgs84_to_enu.transform(gps[0][i], gps[1][i], gps[2][i])
    enu_x.append(temp_enu_x - enu_x_base)
    enu_y.append(temp_enu_y - enu_y_base)
    enu_z.append(temp_enu_z - enu_z_base)

acc = rotation_z * load_imu[""]

# axes = plt.axes()
# axes.xaxis.set_visible(False)
# axes.yaxis.set_visible(False)
plt.scatter(enu_x, enu_y)
plt.show()





