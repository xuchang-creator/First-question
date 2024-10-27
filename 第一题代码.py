#导入库
import urllib.request as ur
from lxml import etree
from selenium import webdriver
import pandas as pd
import time

#定义用于获取定制对象的函数
def get_request(page):
    #获取网页源码
    if page==1:
        url="https://www.bkjx.sdu.edu.cn/index/gztz.htm"
    else:
        url="https://www.bkjx.sdu.edu.cn/index/gztz/" + str(180-page) + ".htm"
    #制作请求头
    headers={
    "cookie":
    "SESSIONID = 823D11F3D5F489B9398122E8A33918E9",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    #定制对象
    request=ur.Request(url=url,headers=headers)
    return request

#定义用于获取返回内容的函数
def get_content(request):
    #发送请求并获取返回内容
    response=ur.urlopen(request)
    content=response.read().decode("utf-8")
    return content

#定义用于解析返回内容从而获得所需数据的函数
def search(content,num):
    #使用xpath方法定位所需元素：标题、发布时间、链接
    tree=etree.HTML(content)
    a=f"/html/body/div[2]/div[2]/div[2]/div[2]/div/div[{str(num)}]/div[2]/a/text()"
    title=tree.xpath(a)[0]
    b=f"/html/body/div[2]/div[2]/div[2]/div[2]/div/div[{str(num)}]/div[3]/text()"
    time=tree.xpath(b)[0]
    link_list=tree.xpath("//div[@id='div_more_news']//a/@href")
    #分类并修改返回的网址
    if  "http" in link_list[num-1]:
        link=link_list[num-1]
    else:
        link="https://www.bkjx.sdu.edu.cn"+link_list[num-1]
        link=link.replace("..","")
    #用selenium工具获取消息内容
    browser = webdriver.Chrome()
    browser.get(link)
    #剔除部分来自其他网站的消息
    if "bkjx" not in link:
        print(f"对不起，该通知由于是来源于山东大学本科生网的转载无法显示内容，请点击链接进行查看{link}")
        return title,time,link,0
    else:
        detail=browser.find_element("xpath","//div/form/div")
        detail=detail.text
        print(f"\n标题：{title}\n\n发布时间：{time}\n\n链接：{link}\n\n内容：{detail}")
        return title,time,link,detail

#定时爬取功能扩展
def time_set(in_time):
    in_page = int(input("请输入查询的页码（共19页）："))
    in_request = get_request(in_page)
    in_content = get_content(in_request)
    in_num = int(input("请输入要查询多少条消息："))
    #设置休眠时间
    time.sleep(in_time)
    #爬取用户想要查询的所有消息并保存
    in_data=[]
    for i in range(1,in_num+1,1):
      in_title, in_time, in_link, in_detail = search(in_content, i)
      in_data.append((in_title, in_time, in_link, in_detail))
    df = pd.DataFrame(in_data, columns=('标题', '发布时间', '链接', '内容'))
    df.to_excel('消息.xlsx')


#程序本体，通过调用各个函数实现功能需求
need=int(input("请问是查询信息(输入1)还是设置定时获取信息功能(输入2)："))
if need==1:
   #进入循环，从而存储所有需要的消息
   count=0
   data=[]
   while count==0:
     #调用以上函数进行功能实现
     page=int(input("请输入查询的页码（共19页）："))
     request=get_request(page)
     content=get_content(request)
     num=int(input("请输入查询的通知的位置（每页15条消息）："))
     title,time,link,detail=search(content,num)
     data.append((title,time,link,detail))
     #生成表格
     df = pd.DataFrame(data, columns=('标题','发布时间','链接','内容'))
     df.to_excel('消息.xlsx')
     ask=input("是否需要继续查询(是或否)：")
     if ask=="是":
        continue
     else:
        break
else:
      time_get=float(input("请输入设定的时间(秒)："))
      time_set(time_get)









