<center><font size=5>Mobile Internet Cource Project</font></center>

**index:**

- demo
    - [Scrapy Crawler Management System](http://mahongying.top:5000)
    - [Mongodb Management System](http://mahongying.top:4321)
    - [ip Proxy](http://mahongying.top:8888/phpmyadmin/)
    - [ip Proxy API](http://mahongying.top:8687/ip/getIp?limit=100)
    - [github repository](https://github.com/GracefulMan/crawler)
    - [slide](http://mahongying.top:8888/mahongying.pdf)
- Introduction to My Project
    - background
    - Project Related Technologies
        - Ip Proxy with multisource 
        - Scrapy-redis
    - Summary
        - what i have done
        - Feature expectations

# Introduction to My Project

**Abstract:**Distributed web crawling is a distributed computing technique whereby Internet search engines employ many computers to index the Internet via web crawling. By spreading the load of these tasks across many computers, costs that would otherwise be spent on maintaining large computing clusters are avoided. i am trying to improve the performance of distributed web crawling and solve some common problems in web crawling.such as how to effectively  anti anti-spider, how to design a high performance spider.

## background

### Why do we use crawler technology?

Distributed web crawling is a distributed computing technique whereby Internet search engines employ many computers to index the Internet via web crawling. By spreading the load of these tasks across many computers, costs that would otherwise be spent on maintaining large computing clusters are avoided. crawler technonlogy has been widely used in follow aspect:

- Build da search engine
- Collect data as dataset
- Networking voting, Online ticket purchase

### Anti-crawl strategy

**why the web page use Anti-crawl strategy?** For a web page, we often want it to be well structured and clear so that search engines can accurately recognize it.In turn, there are some scenarios. We don’t want content to be easily accessible, such as the transaction volume of e-commerce websites, the topics of educational websites, and so on. Because these contents are often the lifeblood of a product, they must be effectively protected.

we usually can see the following form of Anti-crawl strategy:

- User-Agent + Referer detection
- Authentication or Cookie validation
- Verification Code
- IP frequency limit
- Asynchronous loading



## Project Related Technologies



### Ip Proxy with multisource 

A proxy pool manages a large set of proxies. In other words, it is a system that controls the quality of proxies and decides which IPs are going to be included in a set of proxies used by someone.

**the structure of my ip proxy pool:**since i found that when we crawl a web page, the speed of get page content of web page and the speed of parser a web page have big difference. so my structure divided those two parts into two parts and  use cache  and multithreading to balance the speed of two parts.

![](https://ws1.sinaimg.cn/large/006tNc79gy1g3vu3suxifj30mc0hcjsr.jpg)

<center><b>the structure of ip proxy pool</b></center>

when it finished parser the page, the content will be saved into mysql database. in order to validate the data, i design a validation part to periodicly check the effectiveness.since my ip proxy pool is used to provide ip for distributed crawler,so it needs to seed to a lot of server, so i design a part to provide API for servers.

**Technical detail**:

- Spider
    - requests + threading + ScalableBloomFilter + lxml
    - source:xici, wuyou,66,...
    - Parsing and request separation
    - Automatic execution on a regular time
- Storage and Validation
    - Mysql + PhpmyAdmin
    - Automatic check on a regular time whether the proxies are avaiable
- API
    - Koa framework
    - fetch IPs in the form of JSON and separated from spider

**the result:**

we i reqeust the api, i will get the json type's content and by passing the parameter of limit and page, we can get different number of ip.

![](https://ws2.sinaimg.cn/large/006tNc79ly1g3vuars66wj30qo0dztag.jpg)





## Scrapy-redis

**Introduction to Scrapy:**Scrapy is a free and open-source web-crawling framework written in Python. Originally designed for web scraping,it can also be used to extract data using APIs or as a general-purpose web crawler. 

**Crawler web:**
DBLP,IEEE,ACM



**the structure of Scrapy:**

![](https://ws3.sinaimg.cn/large/006tNc79ly1g3vubfxfphj30jg0dqdi2.jpg)



the scrapy engine is a center part of scrapy framework. when we start cralwer, the scrapy engine will inform Scheduler to pass requests into Downloader, and the Downloader download the requests and return the response to Spiders. Spider will paser the response and pass data to Item Pipeline and pass url as new Requests object to Scheduling to do the same things.

**the strucute of scrapy-redis:**

![](https://ws4.sinaimg.cn/large/006tNc79ly1g3vubvkbs7j31250smafm.jpg)



the scrapy-redis increases the center scheduler for url queue and it will determine which url should be pass to a fixed server.

### anti anti-spider

**Problem 1:Routine Problem**

**Solution:**

- *IP frequency limit:* use my ip proxy pool to provide ip.
- *URL redirection:* combine requests with scrapy togother and use requests to process rediction and generate new request object. 
- *Database:*Since scrapy item object is similar to dict object, and for large-scale crawler we need higher read/write speed, Therefore, relational databases are not suitable for saving data.

**Problem 2:Asynchronous loading**

**Solution:**Like Google,Amazon and IEEE such webs, it’s web content uses asynchronous loading and we can’t get content direction, i use two ways to solve those two problem:

- by analyzing the js file to get the target file url or rewrite the web page logic.

![](https://ws1.sinaimg.cn/large/006tNc79ly1g3vuc7iu4bj30pl0d70vo.jpg)



- Loading the brower kernel into scrapy and use blower kernel to simulate the web brower.(Selenium+Headless Firefox)

### Visualization

**Visualization for Scrapy:**

1. combine scrapyd and SpiderKeeper together to start ,create a crawler task and manage the distributed crawler under web page.
2. log analysis and task scheduling.

**Visualization for database:** 

1. use adminmongo to visualize my database ,meanwhile , providing API for data. 

**result:**

![](https://ws2.sinaimg.cn/large/006tNc79ly1g3vucif8swj31400p0an4.jpg)

<center><b>ip proxy pool</b></center>

![](https://ws1.sinaimg.cn/large/006tNc79ly1g3vud05nmuj31400p0k0s.jpg)

<center><b>spiderKeeper</b></center>

![](https://ws1.sinaimg.cn/large/006tNc79ly1g3vud8tkuej31400p07ej.jpg)

<center><b>data</b></center>

## Summary

### what i have done 

- construct ip proxy pool
- construct a distributed crawler by using scrapy-redis 
- do some work on anti anti-spider and made them in my distributed framework 

### Feature expection

- use current koa framework to finish constuction of proxy website.
- anti anti-spider for google search
- research on url scheduling
