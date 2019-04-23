from lib.request import Base
from config import url_path
import json
import os





class Imgdown(Base,url_path.Tmall):
	"""docstring for Imgdown"""
	def __init__(self,main_path):
		super(Imgdown, self).__init__()
		self.base_url = self.enm.get(main_path).get('base_url')
		self.xpath = self.enm.get(main_path).get('xpath')
		self.title_xpath = self.enm.get(main_path).get('title_xpath')
		# self.img_xpath = "//ul[@id='J_UlThumb']/li/a/img/@src"
		self.xpath_one = self.enm.get(main_path).get('xpath_one')
		self.xpath_two = self.enm.get(main_path).get('xpath_two')
		self.zol_dict = self.enm.get(main_path).get('zol_dict')
		self.xpath_three = self.enm.get("tianmao").get('xpath_three')
		self.xpath_four = self.enm.get("tianmao").get('xpath_four')


	#如果图片地址没有http，加上并返回
	def url_header(self,url):
		if ('https:' or 'http:') in url[:6]:
			return url
		elif 'bizhi' in url:
			return 'http://desk.zol.com.cn'+url
		else:
			return 'https:'+url

	#裁剪图片尺寸，并返回图片地址
	def url_re(self,url,size):
		if 'png' in url:
			url_ = url.split('.png')[:-1]
			n = ''.join(url_)
			return n+'.png_'+size+'.jpg'
		
		elif 'jpg_' in url:
			new_url = url.split('.jpg')[:-2]
			new = ''.join(new_url)
			return new+'.jpg_'+size+'.jpg'

		elif 'desk' in url:
			return url.replace('144x90',size)

		else:
			return url



	#下载主程序::返回格式{商品地址：【图片地址】，商品地址：【图片地址】}的dict
	def get_html(self,name,path,size,num):
		new_url = self.base_url.format(name)
		print(new_url)
		pro_list = self.output(new_url,self.xpath)#获取页面的所有商品地址list
		pro_tit = self.output(new_url,self.title_xpath)
		m = 0
		for i, l in zip(pro_list[:num], pro_tit[:num]):
			print(i,l)
			url = self.url_header(i)
			# pro_title = self.output(self.url_header(i),self.title_xpath)[0].strip()#获取商品的标题并去空格
			# new_xpath = self.xpath_two if 'tmall' in i else self.xpath_one
			pro_url = self.output(url,self.xpath_one) + self.output(self.url_header(i),self.xpath_two)#获取商品的所有图片地址list

			# 生成文件路径
			p = self.add_path(path,name,l)
			print(p)
			self.img_down(pro_url,p,size)
			m +=1

	def get_test(self,name):
		new_url = self.base_url.format(name)
		re = self.request(new_url).text
		print(new_url)

	#创建路径地址
	def add_path(self,path,name,pro_title):
		new_name = name
		dicxx = self.zol_dict
		try:
			if new_name in dicxx.values():
				new_name = list(dicxx.keys())[list(dicxx.values()).index(name)]
		except Exception as e:
			print(e)
		else:
			new_name = name

		title = path+'\\'+ new_name +'\\'+pro_title
		if not os.path.exists(title):
			os.makedirs(title)
		return title


	#下载图片，地址url，需要下载的图片xpath_list，下载路径，下载数量
	def img_down(self,img_xpath_list,img_path,img_size,img_num=None):
		n = 0
		for t in img_xpath_list:
			print(t)
			jpg_url = self.url_re(t,img_size)
			content = self.request(self.url_header(jpg_url)).content
			img_name = img_path+'\\'+img_path[-5:]+str(n)+'.jpg'
			print(img_name)
			with open(img_name,'wb') as f:
				f.write(content)
			n += 1


if __name__ == '__main__':
	pass

	# c = Imgdown()
	# print(c.get_test('卫衣'))
	print(Imgdown('tianmao').get_html('苹果手机','d:\\秀店商品图片','800x800',int(1)))
	# print(Imgdown('zol').add_path("D:/秀店商品图片",'dongman','ceshi'))
