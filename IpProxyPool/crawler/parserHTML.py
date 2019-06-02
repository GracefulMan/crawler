from IpProxyPool.config import proxy_Ip,crawler
from lxml import etree
import requests
class Parser:
    def __init__(self):
        self.__parser = {
            "wuyou":self.__parserWuyou,
            "66":self.__parser66,
            "xici":self.__parserxici
        }
    def __parserWuyou(self,content):
        html = etree.HTML(content)
        #result = etree.tostring(html,encoding='utf-8')
        result = html.xpath('/html/body/div[5]/ul/li[2]//li//text()')
        length = len(result)
        gap = 9
        res = []
        for i in range(gap,length,gap):
            temp ={}
            temp['ip'] =result[i]
            temp['port']=result[i+1]
            #匿名：1，透明：0
            if result[i+2]!='透明':
                temp['anonymous'] =1
            else:
                temp['anonymous']=0
            #type：0：http，1：https
            if result[i+3]=='http':
                temp['type']=0
            else:
                temp['type']=1
            temp['location']=result[i+4]
            temp['validation']=result[i+8]
            res.append(temp)
        return res
    def __parser66(self,content):
        html = etree.HTML(content)
        result = html.xpath("/html/body/div[@class='container']//table//text()")
        gap = 5
        res = []
        result=result[7:]
        length = len(result)-1
        for i in range(0,length,gap):
            temp={}
            temp['ip'] =result[i]
            temp['port']=result[i+1]
            temp['location'] =result[i+2]
            if result[i+3]=='高匿代理':
                temp['anonymous']=1
            else:
                temp['anonymous']=0
            temp['validation'] = result[i+4][:14]
            res.append(temp)
        return res
    def __parserxici(self,content):
        html = etree.HTML(content)
        result = html.xpath('//table[@id="ip_list"]//text()')
        result=result[22:]
        print(result)
        res = []
        for i in range(len(result)):
            res.append(result[i])
            if '\n      ' not in result[i] :
                res.append(result[i])
        for i in range(0,len(res),31):
            print(res[i:i+31])
        exit(0)
        temp=[]
        for i in range(len(result)-1):
            if '\n    ' not in  result[i]:
                temp.append(result[i])
        temp = temp[10:]
        length = len(temp)
        gap =7
        for i in range(0,length,gap):
            print(temp[i:i+gap])

    def parser(self,source,content):
        try:
            if source in self.__parser:
                return self.__parser[source](content)
            else:
                print('error in Parser HtmlPool:no parser function for source:%s'%source)
                return []
        except:
            print("ERROR in paserHTML:paser for source %s"%source)
            return []
    #自己定制html解析函数
    def add(self,name,function):
        self.__parser[name] = function

parser = Parser()
host = '66'
r= requests.get(url=proxy_Ip[host][0],headers=crawler['headers'])
r.encoding =r.apparent_encoding
content = r.text
print(
    parser.parser(host,content=content)
)
