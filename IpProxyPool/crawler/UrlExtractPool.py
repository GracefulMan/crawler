# extract url from source Url.
import queue
import requests
from IpProxyPool.config import crawler
import lxml
from lxml import etree
class urlPool:
    def __init__(self):
        self.__function={
            '66':self.__66,
            "xici":self.__xici
        }
    def __parserHTML(self,url):
        try:
            r= requests.get(url=url,headers =crawler['headers'],timeout = crawler['timeOut'])
            r.encoding =r.apparent_encoding
            return r.text
        except e:
            print('error in UrlExtractPool:URL %s,reason:%s'%(self.__Url,e))
    def __66(self,url):
        pages = 100
        html = self.__parserHTML(url)
        html =etree.HTML(html)
        result = html.xpath('//*[@id="PageList"]/a[12]//text()')
        print("result",result)
        if len(result)!=0:
            last_Page = int(result[0])+1
            urlList = []
            for i in range(2,last_Page):
                urlList.append(url+str(i)+".html")
            for i in range(1,35):
                for j in range(1,pages):
                    url = url+"areaindex_"+str(i)+"/"+str(j)+".html"
                    urlList.append(url)
                    url = ''
            return urlList
        else:
            return result

    def __xici(self,url):
        urlList = []
        for i in range(1,100):
            urlList.append(url+str(i))
        return urlList



    def urlExtract(self,source,url):
        if source in self.__function:
            return self.__function[source](url)
        else:
            print('error in UrlExtractPool:no parser function for source:%s'%source)
            return []
    def add(self,source,function):
        self.__function[source] = function

myPool = urlPool()
print(myPool.urlExtract('xici','https://www.xicidaili.com/wt/'))
