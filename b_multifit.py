import numpy as np
import pandas as pd
from sklearn import linear_model
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
import mytools

# 导入并裁剪数据
data = pd.read_excel("/Users/wlt/Desktop/Q/C/Data2.xls")
data = data.replace("水", 0) # 用0浓度代替水
data = data.fillna(method="pad", axis=0) # 填充浓度的省略部分
data = np.array(data)
data = data[:,1:7]
data = np.vstack([data[0:5, :], data[6:9, :], data[10:14, :], data[15:18, :],\
                  data[19:22, :], data[23:26, :], data[27:, :]])

# 通过浓度对数据进行排序
data = data[data[:, 0].argsort()]

# 把相同浓度的实验结果分为一类
groupedData = mytools.group_by_concentration(data)

# 画出蓝、绿、红三维图像
mytools.plot_BGR(groupedData, title="Sulphur Dioxide")

# 制作机器学习的训练集与预测真实值
data = np.append(data, [[1] for i in range(data.shape[0])], 1)
data = np.append(data, data[:, 1:4]**2, 1)
X = np.append(data[:, 1:4], data[:, 6:], 1)
y = data[:, 0, None]

# 多元多次回归（注意这里的Linear Regression并不代表该回归是线性回归）
reg = linear_model.LinearRegression()
reg.fit(X, y)

# 试预测训练数据
predict = reg.predict(np.append(data[:, 1:4], data[:, 6:], 1))
predict = np.round(predict, 2)
print("训练的数据：\n" + str(np.round(y, 2)))
print("预测训练的数据：\n" + str(predict) + '\n')

# 计算拟和成本
cost = float(sum((predict - y) ** 2) / (2*predict.shape[0]))
print("拟和成本："+str(cost))

# 输出模型表达式
coeffList = [str(round(i, 2)) for i in reg.coef_[0]]
varList = [" * Red", " * Green", " * Blue", " * Red^2", " * Green^2", " * Blue^2"]
print("c = ("+") + (".join([coeffList[3], coeffList[0]+varList[0], coeffList[1]+varList[1],\
                           coeffList[2]+varList[2], coeffList[4]+varList[3],\
                           coeffList[5]+varList[4], coeffList[6]+varList[5]]) + ")")
