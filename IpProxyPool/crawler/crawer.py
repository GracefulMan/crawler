'''
author：马鸿英
这个文件为爬虫初始化以及中心调度逻辑块
'''


import sys
import threading
import hashlib
import random
import requests
import queue
import time
from pybloom_live import ScalableBloomFilter
sys.path.append("../../")
from IpProxyPool.config import crawler,proxy_Ip
from IpProxyPool.crawler.parserHTML import Parser
from IpProxyPool.crawler.UrlExtractPool import urlPool
from IpProxyPool.storage.saveIp import SaveData as SqlSave
def getHtml():
    global urlQueue,textQueue,visited,contentDir,count,mutex
    while not urlQueue.empty():
        urlInfo = urlQueue.get().split()
        source,url = urlInfo[0],urlInfo[1]
        print("deal with url:%s %s"%(source,url))
        headers = crawler['headers']
        if not url in visited:
            try:
                mutex.acquire()
                visited.add(url)
                count+=1
                if count%100==0:
                    print("\ncurrent crawling URL number is: "+str(count))
                mutex.release()
                r = requests.get(url=url,headers=headers,timeout=30)
                r.encoding =r.apparent_encoding
                #建立urltext队列，以字典的形式储存
                md5 = hashlib.md5()
                md5.update(url.encode('utf-8'))
                key = str(md5.hexdigest())
                contentDir[key]=[source,r.text]
                textQueue.put(key)
                if count%200==0:
                    myParser()
            except:
                print("error:",url)

def urlParser(key,url):
    global urlPool
    result = urlPool.urlExtract(key,url)
    return result

def dispatcher():
    global urlQueue
    for key,value in proxy_Ip.items():
        for url in value:
            tempUrl=key+" "+url
            res = urlParser(key,url)
            for url in res:
                urlQueue.put(key+" "+url)
            urlQueue.put(tempUrl)
            print("add source: %s,total add url number:%s"%(tempUrl,len(res)))
def myParser():
    global textQueue,Parser,count,urlQueue,contentDir
    SaveToSQL = SqlSave()
    while textQueue.empty():
        time.sleep(random.randint(20,40))
    while not textQueue.empty():
        key =textQueue.get()
        nextDeal =contentDir[key]
        contentDir.pop(key)
        source,html = nextDeal[0],nextDeal[1]
        #获得解析后的结果，返回结果为列表
        res = Parser.parser(source,html)
        #储存数据到数据库里面
        if res!=[]:
            for item in res:
                SaveToSQL.parser(source,item)
            print("Save to SQL for key "+key)





if __name__=="__main__":
    global urlQueue,textQueue,visited,contentDir,Parser,urlPool,count,mutex
    #实例化一个parser.Parser类
    Parser = Parser()
    mutex=threading.Lock()
    #url计数器
    count=0
    urlPool = urlPool()
    contentDir = {}
    visited = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
    urlQueue = queue.Queue()
    textQueue = queue.Queue()
    dispatcher()
    threads = []
    for i in range(crawler['threadsNum']):
        threads.append(threading.Thread(target=getHtml))
        threads.append(threading.Thread(target=myParser))
    for i in range(2*crawler['threadsNum']):
        threads[i].setDaemon(False)
        threads[i].start()
    for i in range(2*crawler['threadsNum']):
        threads[i].join()
    if not textQueue.empty():
        for i in range(crawler['threadsNum']):
            threads.append(threading.Thread(target=myParser()))
        for i in range(crawler['threadsNum']):
            threads[i].setDaemon(False)
            threads[i].start()
        for i in range(2 * crawler['threadsNum']):
            threads[i].join()



