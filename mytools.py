import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot_concentration_v(dataArray, title=""):
    """
    画出浓度—V图像
    仅对(a)问有效，因为该问数据格式为BGR
    """
    blue = dataArray[:, 1]
    green = dataArray[:, 2]
    red = dataArray[:, 3]
    concentration = list(dataArray[:, 0])
    v = 0.615*red - 0.515*green - 0.100*blue
    
    theta = np.polyfit(concentration, v, 1)
    h = np.poly1d(theta)
    new_x = np.linspace(min(concentration), max(concentration))
    cost = sum((h(concentration) - v) ** 2) / (2*len(concentration))
    
    plt.scatter(concentration, v, color="blue")
    plt.plot(new_x, h(new_x), color="green")
    plt.title("V-Concentration Graph of " + str(title) +"        "+\
              "Cost: %.2f"%cost + "\nv = " + str(h).lstrip().replace('x', 'c'))
    plt.xlabel("Concentration / ppm")
    plt.ylabel("V")
    plt.show()

def plot_BGR(groupedData, title=""):
    """
    画出蓝、绿、红三维图像
    """
    fig = plt.figure()
    ax = Axes3D(fig)
    sumPointSize = 0
    for tempArray in groupedData:
        sumPointSize += np.array(np.matrix(tempArray)[:, 0].sum())
    avgPointSize = sumPointSize /\
                   sum([tempArray.shape[0] for tempArray in groupedData])
    for dataArray in groupedData:
        pointSize = np.array(np.matrix(dataArray)[0, 0])
        pointSize = pointSize * 100 / avgPointSize
        blue = np.array(np.matrix(dataArray)[:, 1])
        green = np.array(np.matrix(dataArray)[:, 2])
        red = np.array(np.matrix(dataArray)[:, 3])
        ax.scatter(blue, green, red, s=pointSize)
    ax.set_xlabel('Blue')
    ax.set_ylabel('Green')
    ax.set_zlabel('Red')
    plt.title("Blue Green Red Graph of "+str(title))
    plt.show()

def group_by_concentration(dataArray):
    """
    把相同浓度的实验结果分为一类
    """
    groupedData = [] # list of arrays
    tempArray = np.array([dataArray[0]])
    for row in dataArray[1:]:
        if row[0] != np.matrix(tempArray)[0, 0]: # 找到了新的浓度类
            groupedData.append(tempArray)
            tempArray = np.array(row)
        else: # 仍为当前浓度
            tempArray = np.vstack((tempArray, row))
    else:
        groupedData.append(tempArray)
    return groupedData

def calc_avg_BGR(groupedData):
    """
    计算一类浓度的平均蓝、绿、红数值
    """
    avgBGR = []
    for row in groupedData:
        BGR = np.array(np.matrix(row)[:, 0:4]) # Blue Green Red
        avg = sum(BGR)/BGR.shape[0]
        avgBGR.append(avg)
    return avgBGR

def calc_sd(groupedData):
    """
    计算组内标准差
    """
    sdList = []
    for row in groupedData:
        BGR = np.array(np.matrix(row)[:, 1:4]) # Blue Green Red
        avg = sum(BGR)/BGR.shape[0]
        variance = (((BGR - avg)**2).sum()) / BGR.shape[0]
        sdList.append(variance**0.5)
    return sdList

def calc_inter_dist(avgBGR, dataArray):
    """
    计算组间距离
    """
    rowGroup = [(i, j) for i in avgBGR for j in avgBGR if id(i) != id(j)]
    sumDist = 0
    for a,b in rowGroup:
        dist = ((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2)**0.5
        dist = dist / abs(a[0] - b[0])
        sumDist += dist
    avgDist = sumDist / dataArray.shape[0]
    return avgDist
