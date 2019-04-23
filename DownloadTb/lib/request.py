import requests
from lxml import etree
import xmltodict
import json
import requests_html
import time
from requests import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options





class Base:
	def __init__(self):
		self.session = requests.Session()

	def request(self,url,encoding='gb18030'):
		# proxy = {'http':'http://172.25.127.12:8888','https':'https://172.25.127.12:8888'}
		header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"}
		# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		urllib3.disable_warnings()
		resp = self.session.get(url,headers=header, verify=False)
		time.sleep(1)
		if encoding:
			resp.encoding = encoding
		if resp.status_code != 200:
			return resp.status_code
		return resp

	def parse(self,html,xpath):
		html_new = html.replace(r'<!--', '"').replace(r'-->', '"')
		return etree.HTML(html_new).xpath(xpath)

	def output(self,url,xpath):
		return self.parse(self.request(url).text,xpath)

	def outputall(self,url,xpath):
		chrome_op = Options()
		chrome_op.add_argument('--headless')
		chrome_op.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_op)
		driver.get(url)
		while True:
			re = True
			try:
				# driver.execute_script('window.scrollTo(0,1000000)')
				time.sleep(3)
				data = driver.page_source
				html = etree.HTML(data).xpath(xpath)
				# driver.find_element_by_id('description')
				# print(html)
				re = True
			except Exception as e:
				re = False
				print(e)

			if len(html) > 1:
				break
		driver.quit()
		return html





class Xml:
	def __init__(self):
		'''初始化xml类'''
		pass

	@staticmethod
	def xml_to_dict(xml_data):
		'''xml 转化 json'''
		return json.dumps(xmltodict.parse(xml_data), ensure_ascii=False, sort_keys=True)

	@staticmethod
	def json_to_xml(json_data):
		'''json转化 xml'''
		return xmltodict.unparse(json.loads(json_data))
