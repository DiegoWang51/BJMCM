import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
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

# 制作机器学习的训练集与测试集
data = np.append(data, [[1] for i in range(data.shape[0])], 1)
data = np.append(data, data[:, 1:4]**2, 1)
features = np.append(data[:, 1:4], data[:, 6:], 1)
labels = data[:, 0, None]

for percentage in [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:

    # 分割训练集与测试集
    print("训练集占数据的百分比：" + str(percentage) + "\n")
    X_train, X_test, y_train, y_test =\
    train_test_split(features, labels, test_size=(1-percentage), random_state=42)

    # 多元多次回归（注意这里的Linear Regression并不代表该回归是线性回归）
    reg = linear_model.LinearRegression()
    reg.fit(X_train, y_train)

    # 试预测训练数据
    predict = np.round(reg.predict(X_test), 2)
    print("预测的浓度：\n" + str(predict) + '\n')
    print("真实浓度：\n" + str(y_test) + '\n')

    # 计算拟和成本
    cost = float(sum((predict - y_test) ** 2) / predict.shape[0])
    print("拟和成本："+str(cost))

    # 换个行
    print()
