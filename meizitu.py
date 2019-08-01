# encoding=utf-8
# !/usr/bin/env python
# @Author:Markxu
# @CreateTime:2019/7/31 下午10:59
# @ProjectName:PyCharm


import requests
from lxml import etree
import random
import threading
import os
import time


class meizitu(object):
    def __init__(self, url):
        self.headersPool = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36']
        self.headers = {'User-Agent': random.choice(self.headersPool)}
        self.url = url
        res = requests.get(self.url, headers=self.headers)
        self.html = res.content.decode('utf-8')
        self.root = etree.HTML(self.html)


    #获取总的页数
    def getPageNumb(self):
        sumPage = self.root.xpath("/html/body/div[2]/div[1]/div[2]/nav/div/a[position()=last()-1]/text()")
        #print(sumPage)
        return int(sumPage[0])

    #处理相册,获取此页面所有相册的地址
    def Page(self):
        titleUrls=self.root.xpath('//*[@id="pins"]/li/a/@href')
        #print(titleUrls[0])
        return titleUrls

    def downloadPic(self,url):
        res=requests.get(url,headers=self.headers)
        resp=res.content.decode('utf-8')
        root=etree.HTML(resp)
        imgTitle = root.xpath('//*[@class="main-title"]/text()')[0]
        print(imgTitle)
        os.mkdir(imgTitle)
        numb = root.xpath('//*[@class="pagenavi"]/a[position()=last()-1]/span/text()')[0]
        numb=int(numb)

        for i in range(numb):
            nowurl=url+'/'+str(i+1)
            print(imgTitle,':','第',i+1,'页下载',nowurl)

            nowhtml=requests.get(nowurl,headers=self.headers).content.decode("utf-8")
            now=etree.HTML(nowhtml)
            imgUrl = now.xpath('//*[@class="main-image"]/p/a/img/@src')[0]

            header = {}
            header['User-Agent'] = random.choice(self.headersPool)
            header['Referer'] = nowurl
            res = requests.get(imgUrl, headers=header)


            with open(imgTitle+'/'+str(i+1)+'.jpg','wb') as f:
                f.write(res.content)

            time.sleep(random.randint(0,3))



    def getHtml(self,url):
        res=requests.get(url,headers=self.headers)
        content=res.content.decode('utf-8')
        return content


    #下载单页面所有图集
    def go(self):
        sumPageNumb=self.getPageNumb()
        print('总共有{}页'.format(sumPageNumb))
        count=0
        albumList=self.Page()
        time.sleep(8)
        for url in albumList:
            print('正在下载第{}页'.format(count+1))
            count+=1
            threading.Thread(target=self.downloadPic, args=(url,)).start()
            time.sleep(random.randint(2,6))







if __name__ == '__main__':
    url = 'https://www.mzitu.com'
    m=meizitu(url)
    m.go()