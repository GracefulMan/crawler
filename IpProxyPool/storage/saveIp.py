from IpProxyPool.storage.MYSQLlib import MySqlQuery as SQL
from datetime import datetime
import time
import re
class SaveData:
    def __init__(self):
        self.__connection = SQL()
        self.__function={
            "wuyou": self.__saveWuyou,
            "66": self.__save66,
            "xici": self.__saveXici
        }
    def __saveWuyou(self,dictionary):
        _sql = "INSERT INTO ip_information(ip,port,location,anonymous,ip_type,validation)VALUES(%(ip)s,%(port)s,%(location)s,%(anonymous)s,%(ip_type)s,%(validation)s)"
        validTime = dictionary['validation']
        if "秒" in validTime:
            validTime=int(int(validTime.split('秒')[0])/60)
        elif "分" in validTime:
            validTime=int(validTime.split('分')[0])
        value = {
            'ip':dictionary['ip'],
            'port':dictionary['port'],
            'location':dictionary['location'],
            'anonymous':dictionary['anonymous'],
            'ip_type':dictionary['type'],
            'validation':validTime
        }
        return self.__connection.sql(_sql,value)
    def __save66(self,dictionary):
        _sql = "INSERT INTO ip_information(ip,port,location,anonymous,ip_type,validation)VALUES(%(ip)s,%(port)s,%(location)s,%(anonymous)s,%(ip_type)s,%(validation)s)"
        validTime = dictionary['validation']
        year,month,day,hour = validTime[:4],validTime[5:7],validTime[8:10],validTime[11:13]
        timeDifference =(datetime.now()-datetime(int(year),int(month),int(day),int(hour))).seconds
        gaptime = int(timeDifference/60)
        value = {
            'ip': dictionary['ip'],
            'port': dictionary['port'],
            'location': dictionary['location'],
            'anonymous': dictionary['anonymous'],
            'validation': gaptime,
            'ip_type':0
        }
        return self.__connection.sql(_sql,value)
    def __saveXici(self):
        pass
    def parser(self,source,data):
        if source in self.__function:
            return self.__function[source](data)
        else:
            print("error in Parser saveIp:no parser function for source:%s"%source)
            return False

temp = SaveData()
dic = {"ip":"101.1.1","port":3306,"location":"china","anonymous":1,"type":1,"validation":"2分钟前"}
print(temp.parser('wuyou',dic))




