#-*- coding:utf-8 -*-
import requests
import sys
import csv
from lxml import etree

header={
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
	"Content-Type":"application/x-www-form-urlencoded",
	"Accept-Encoding":"gzip, deflate",
	"Origin":"http://www.jsons.cn",
	"Cookie":"Hm_lvt_486b267e380702c62812c2d37b1c9949=1653884131,1653963930,1653978836; ASP.NET_SessionId=r10b23lldqq1t4zauofc4bnc; Hm_lpvt_486b267e380702c62812c2d37b1c9949=1653978836"
}

targeturl = "http://www.jsons.cn/ipbatch/"

data={
	"txt_ip":""
}

def usage():
	print(
		'''
			 *******************************************************************
			 	IP归属地批量查询：											   
			 	1.脚本一次性只支持查找200个url地址,将要查询的url放入urls.txt   
			 	2.脚本会将查询结果写入result.csv文件当中 
			 *******************************************************************
			 Author: Arenid
			 Version: 1.0
		'''
	)

def search():
	targets = ""
	url_count = 0
	with open('urls.txt','r') as f:
		urls = f.readlines()
		url_count = len(urls)
		for url in urls:
			url = url.replace(":","%3A").replace("/","%2F").replace("\n","%0A%0D")
			targets += url
	
	data["txt_ip"] = targets
	response = requests.request('post',targeturl,headers=header,data=data)
	if response.status_code == 200:
		tree = etree.HTML(response.text)
		title = tree.xpath('//div[@class="accordion-group"]/div/div/div/table/tbody/tr[1]//th/text()')
		with open('result.csv',mode='w',encoding='utf-8-sig',newline='') as f:
			writer = csv.writer(f)
			writer.writerow(title)
			for i in range(2,url_count+1):
				ip = tree.xpath("//div[@class=\"accordion-group\"]/div/div/div/table/tbody/tr["+str(i)+"]/td[1]/a/text()")
				divs = tree.xpath("//div[@class=\"accordion-group\"]/div/div/div/table/tbody/tr["+str(i)+"]//td/text()")
				if len(divs) == 0 or len(ip) == 0:
					continue
				else:
					divs = datastrip(divs)
					divs[1] = datastrip(ip)[0]
					writer.writerow(divs[1:])
			
def datastrip(datas):
	ls = []
	for data in datas:
		ls.append(data.strip("\r\n").strip(" "))
	
	return ls

	
def main():
	usage()
	search()
	
if __name__ == '__main__':
	main()






