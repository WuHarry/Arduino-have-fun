# -*- coding: utf8 -*-
__author__ = 'Harry Wu'
from Tkinter import *
import urllib2
import sys, time
import winsound


class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding
    def write(self, s):
        if type(s) == str:
            s = s.decode("utf-8")
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)


#从配置文件读取ip列表
ip_list=[]
for line in open("ip.config"):
    line=line.strip('\n')
    ip_list.append(line)
#从配置文件读取ip对应名称
ip_list_name=[]
for line in open("name.config"):
    line=line.strip('\n')
    ip_list_name.append(line)

#ip_1 = raw_input("请输入ip地址: ")
Temp_1 = input("请输入温度安全值(纯数字可带小数): ")
Humi_1 = input("请输入湿度安全值(纯数字可带小数): ")

ip_head="http://"

url=[]
for x in range(0, len(ip_list)):
    url.append(ip_head+ip_list[x])

#url=ip_head+ip_1
#初始化列表 ip_response, cont, ip_humi, ip_temp
initialvalue = ''
list_length=len(url)
ip_humi=[initialvalue]*list_length
ip_temp=[initialvalue]*list_length
ip_response_temp=urllib2.urlopen(url[0])
cont_temp=ip_response_temp.read()
ip_response=[ip_response_temp]*list_length
cont=[cont_temp]*list_length

while True:

    for x in range(0, list_length):
        ip_response[x]=urllib2.urlopen(url[x])
        cont[x]=ip_response[x].read()

    #ip1_response = urllib2.urlopen(url[0])
    #cont1 = ip1_response.read()

    key1='Humidity:'
    key2='Temperture:'
    key3='<br />'
    # key1='<head>'
    # key2='</head>'
    # key3='</body>'

    for x in range(0, list_length):
        pa=cont[x].find(key1)
        pt=cont[x].find(key2,pa)
        #Humidity str
        ip_humi[x]=cont[x][pa:pt]
        ip_humi[x]=ip_humi[x][9:]
        pa=cont[x].find(key2)
        pt=cont[x].find(key3,pa)
        #Temperature str
        ip_temp[x]=cont[x][pa:pt]
        ip_temp[x]=ip_temp[x][11:]
    #pa=cont.find(key1)
    #pt=cont.find(key2,pa)
    #ip1_humi=cont[pa:pt]
    #Humidity str
    #ip1_humi=ip1_humi[9:]
    #pa=cont.find(key2)
    #pt=cont.find(key3,pa)
    #ip_temp=cont[pa:pt]
    #Temperature str
    #ip_temp=ip_temp[11:]

    if __name__ == '__main__':
        for x in range(0, list_length):
            sys.stdout.write(ip_list_name[x]+" "+"湿度: "+ip_humi[x]+"  温度: "+ip_temp[x]+"                "+"\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
            if (float(ip_humi[x])>Humi_1):
                root = Tk()
                w = Label(root, text=ip_list[x]+"  湿度超标！")
                w.pack()
                winsound.Beep(600,1000)
                root.mainloop()
                time.sleep(10)
            if (float(ip_temp[x])>Temp_1):
                root = Tk()
                w = Label(root, text=ip_list[x]+"  温度超标！")
                w.pack()
                winsound.Beep(600,1000)
                root.mainloop()
                time.sleep(10)
            time.sleep(2)