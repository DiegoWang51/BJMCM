import pandas as pd
import numpy as np
import mytools

# 导入并裁剪数据
data = pd.read_excel("/Users/wlt/Desktop/Q/C/Data1.xls")
data = data.replace("水", 0) # 用0浓度代替水
data = data.fillna(method="pad", axis=0) # 填充物质与浓度的省略部分
data = np.array(data)
za = data[0:10, 1:7] # 组胺
xsj = data[12:22, 1:7] # 溴酸钾
gyj = data[24:31, 1:7] # 工业碱
lslj = data[34:70, 1:7] # 硫酸铝钾
nzns = data[72:87, 1:7] # 奶中尿素

# 写出物质列表
substanceListEN = ["Histamine", "Potassium Bromate", "Industrial Base",\
                   "Aluminum Potassium Sulfate", "Urea in Milk"]
substanceListCH = ["组胺", "溴酸钾", "工业碱", "硫酸铝钾", "奶中尿素"]
substanceName = 0

for dataArray in [za, xsj, gyj, lslj, nzns]:

    # 画出浓度—V图像
    mytools.plot_concentration_v(dataArray, title=substanceListEN[substanceName])

    # 通过浓度对数据进行排序
    dataArray = dataArray[dataArray[:, 0].argsort()]

    # 把相同浓度的实验结果分为一类
    groupedData = mytools.group_by_concentration(dataArray)

    # 画出蓝、绿、红三维图像
    mytools.plot_BGR(groupedData, title=substanceListEN[substanceName])

    # 计算组内标准差
    sd = mytools.calc_sd(groupedData)
    print(substanceListCH[substanceName] + "的组内标准差:",\
          *[str(round(i, 2)) + '\t' for i in sd])

    # 计算一类浓度的平均BGR
    avgBGR = mytools.calc_avg_BGR(groupedData)

    # 计算组间距离
    avgDist = mytools.calc_inter_dist(avgBGR, dataArray)
    print(substanceListCH[substanceName] + "的组间距离:",\
          str(round(avgDist, 2)))

    substanceName += 1
    print()
