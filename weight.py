# -*- coding: cp936 -*-
import arcpy
import numpy as np
import pandas as pd

path='data/gd.shp'
#ListFields����field�������
fields=arcpy.ListFields(path)

def GetTable():
    '''��arcpy����Ϊpandas��������ϲ��pandasЩ~'''
    table=[]
    fieldname=[field.name for field in fields]
    #�α꼯�ϣ���for ѭ��һ�κ�û�취ѭ���ڶ���!һ���α�ʵ��ֻ��ѭ��һ��
    data=arcpy.SearchCursor(path)
    for row in data:
        #Shape�ֶ��е�Ҫ����һ��������
        r=[]
        for field in fields:
            r.append(row.getValue(field.name))
        table.append(r)
    return pd.DataFrame(table,columns=fieldname)

def getdistance(point1,point2,sparef):
    '''������ľ���'''
    #���㹹��һ����
    l=arcpy.Polyline(arcpy.Array([point1,point2]),sparef)
    #���߳�
    return l.getLength()

data=GetTable()
#�ռ�����ͶӰ����
#����ȡһ��shape������ø�ͼ��Ŀռ�ͶӰ
sparef=data['Shape'][0].spatialReference
print '������ϵΪ:'sparef.name
#��������centre
#Shape�ֶ�����һ��geometry object����,���������ĵ������ȹ���
#ò����centroid������ĵ�û�пռ�ͶӰ����,
#����data['centre'][0].spatialReference���ᱨ��
data['centre']=[d.centroid for d in data['Shape']]

#����ŷ����Ȩ�ؾ���
weight=[]
for i in data['centre']:
    row=[]
    for j in data['centre']:
        row.append(getdistance(i,j,sparef))
    weight.append(row)
weight=pd.DataFrame(weight,index=data['FID'],columns=data['FID'])
#���csv
weight.to_csv(path_or_buf='weight.csv',sep=',')

    
