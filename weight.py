# -*- coding: cp936 -*-
import arcpy
import numpy as np
import pandas as pd

path='data/gd.shp'
#ListFields包含field类的数组
fields=arcpy.ListFields(path)

def GetTable():
    '''将arcpy表单变为pandas表单，还是喜欢pandas些~'''
    table=[]
    fieldname=[field.name for field in fields]
    #游标集合，用for 循环一次后没办法循环第二次!一个游标实例只能循环一次
    data=arcpy.SearchCursor(path)
    for row in data:
        #Shape字段中的要数是一个几何类
        r=[]
        for field in fields:
            r.append(row.getValue(field.name))
        table.append(r)
    return pd.DataFrame(table,columns=fieldname)

def getdistance(point1,point2,sparef):
    '''求两点的距离'''
    #两点构造一条线
    l=arcpy.Polyline(arcpy.Array([point1,point2]),sparef)
    #求线长
    return l.getLength()

data=GetTable()
#空间坐标投影参数
#随便抽取一个shape出来求得该图层的空间投影
sparef=data['Shape'][0].spatialReference
print '坐标体系为:'sparef.name
#计算质心centre
#Shape字段下是一个geometry object对象,其下有中心点和面积等工具
#貌似由centroid抽出来的点没有空间投影属性,
#所以data['centre'][0].spatialReference将会报错
data['centre']=[d.centroid for d in data['Shape']]

#计算欧几里权重矩阵
weight=[]
for i in data['centre']:
    row=[]
    for j in data['centre']:
        row.append(getdistance(i,j,sparef))
    weight.append(row)
weight=pd.DataFrame(weight,index=data['FID'],columns=data['FID'])
#输出csv
weight.to_csv(path_or_buf='weight.csv',sep=',')

    
