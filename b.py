import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
制作二氧化硫的C--V图，并计算拟合成本
"""

# 导入并裁剪数据
data = pd.read_excel("/Users/wlt/Desktop/Q/C/Data2.xls")
data = data.replace("水", 0) # 用0浓度代替水
data = data.fillna(method="pad", axis=0) # 填充浓度的省略部分
data = np.array(data)
data = data[:,1:7]

# 计算V值
red, green, blue = data[:,1],data[:,2],data[:,3]
concentration = data[:,0]
v = 0.615*red - 0.515*green - 0.100*blue

# 线性拟合，并计算拟合成本
theta = np.polyfit(v, concentration, 1)
h = np.poly1d(theta)
new_x = np.linspace(min(v), max(v))
cost = sum((h(v) - concentration) ** 2) / (2*len(concentration))

# 画出图像并标明信息
plt.scatter(v, concentration, color="blue", s = 10)
plt.plot(new_x, h(new_x), color="green")
plt.title("Concentration--V Graph of Sulphur Dioxide        " +\
          "Cost: %.2f"%cost + "\nc = " + str(h).lstrip().replace('x','v'))
plt.xlabel("V")
plt.ylabel("Concentration / ppm")
plt.show()
