import pandas as pd

##1. 读入源文件
filename = 'lng2.csv'
name = ["MMSI","Time","State","Speed","Longitude","Latitude","Draft"]
my_path = "clean_lng2.csv"
df = pd.read_csv(filename,sep=' ',names=name)

##2. 去除不可用数据
df = df.dropna() #删除空的表项
df = df.drop(df[(df["State"]!=0) & (df["State"]!=1) & (df["State"]!=5) & (df["State"]!=8)].index)#去除不需要的行驶状态
df = df.drop(df[df["Draft"]==0].index) #删除吃水深度为0的数据
df.reset_index(drop=True, inplace=True) #重置索引
print(df.head(5))#输出中间结果
print(df.shape[0])

##3. 等间隔抽样
new_df = pd.DataFrame(columns = name)
print(new_df.shape[0])
i = 1; j=0
df_list = df.values.tolist() #转化为list，增加循环速度
new_df_list = new_df.values.tolist()
while i<len(df_list):
    if (df_list[i][1]>(df_list[j][1]+3600*6)) or (df_list[i][0]!=df_list[j][0]):
        new_df_list.append(df_list[i])
        j = i
    i = i + 1
new_df = pd.DataFrame(new_df_list,columns=name) #转化回dataframe
print(new_df.head(5))#输出中间结果
print(new_df.shape[0])

##4. 将清洗后的数据输出到文件
new_df.to_csv(my_path,index=False)