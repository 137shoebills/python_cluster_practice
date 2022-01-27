import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import seaborn as sns
import folium 
import folium.plugins
from sklearn import metrics
from math import radians
from math import tan,atan,acos,sin,cos,asin,sqrt

##计算两点之间距离函数
def harversine(lonlat1, lonlat2):
    lon1,lat1 = lonlat1
    lon2,lat2 = lonlat2
    lon1,lat1,lon2,lat2=map(radians,[lon1,lat1,lon2,lat2])
    dlon =lon2 -lon1
    dlat =lat2 -lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371 #地球半径(公里)
    return c * r * 1000

##1. 读入数据
filename = "clean_lng2.csv"
df = pd.read_csv(filename)
print(df.head(5))
data = np.array(pd.DataFrame(df,columns=["Longitude","Latitude"]))
print(data[:5])

##2. DBSCAN聚类算法
# 用经纬度算距离 db = DBSCAN(eps=0.03,min_samples=30,metric=lambda a,b: harversine(a,b))
db = DBSCAN(eps=0.03,min_samples=70) #欧氏距离DBSCAN
labels = db.fit_predict(data) #每个点的分类

n_ratio = len(labels[labels[:] == -1]) / len(labels) #噪声比
print(n_ratio)
cluster_num = len(set(labels)) - (1 if -1 in labels else 0) #簇的数量
min_label=1000 #labels最小值
max_label=-1 #labels最大值
for i in range(len(labels)):
    if min_label>labels[i]:
        min_label=labels[i]
    if max_label<labels[i]:
        max_label=labels[i]
print(cluster_num)
df["label"] = labels;
data2 = pd.DataFrame(df,columns=["Longitude","Latitude","label"])


#输出聚类图
#sns.lmplot(x="Longitude", y="Latitude",hue='label',palette='CMRmap',data=df,fit_reg=False)
#plt.show()

#将数据按聚类分类
clu_result = data2.groupby("label")

#建立一个地图
my_map = folium.Map(control_scale=True,attr='default')#生成一个地图

#对每类kmeans找出中心点
i = min_label
while i <= max_label:
    xy = np.array(pd.DataFrame(clu_result.get_group(i),columns=["Longitude","Latitude"]))
    #print(i,' ',len(xy))
    km = KMeans(n_clusters=1).fit(xy)
    res = km.cluster_centers_
    #将每个中心点放入地图中
    print(res[0][1],res[0][0])
    folium.Marker(location=[res[0][1],res[0][0]],
              popup=i,
    icon=folium.Icon(color='orange', icon='heart') ).add_to(my_map)#将每个中心点放入地图中
    i = i+1
#my_map1.save("my_map1.html")# 输出地图

#生成一个配色方案
from random import randint
colors = []
for i in range(cluster_num + 2): 
    colors.append("#%06X" % randint(0, 0xFFFFFF))

#my_map = folium.Map(control_scale=True,attr='default')#生成一个地图

#把每个点放入标记簇，最后将标记簇放入地图
marker_cluster = folium.plugins.MarkerCluster().add_to(my_map)
for i in range(len(data)):
    if(labels[i] >= 0):
        folium.CircleMarker(location=[data[i][1],data[i][0]],
                    radius=4,
                    color=colors[labels[i]],fill=True,
                    fill_color=colors[labels[i]]).add_to(marker_cluster)
    else:
        folium.CircleMarker(location=[data[i][1],data[i][0]],
                    radius=4,
                    color=colors[cluster_num+1],fill=True,
                    fill_color=colors[cluster_num+1]).add_to(marker_cluster)
marker_cluster = folium.plugins.MarkerCluster().add_to(my_map)
my_map.add_child(folium.LatLngPopup()) #添加点击显示经纬度
my_map.save("my_map.html")# 输出地图
