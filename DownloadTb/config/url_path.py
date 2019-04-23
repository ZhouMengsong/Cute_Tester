

class Img_xpath:
	URL = 'http://desk.zol.com.cn/pc/'
	PC_XPATH = '//div/dl[@class="filter-item first clearfix"]/dd/a/@href'
	FENLEI_XPATH = '//div/dl[@class="filter-item first clearfix"]/dd/a/text()'
	IMG_XPATH = '//ul[@class="pic-list2  clearfix"]/li/a/img/@src'
	WAHAHA = '//ul[@id="showImg"]/li/a/img/@src'  #大图地址
	QQQ = 'https://desk-fd.zol-img.com.cn/t_s144x90c5/g5/M00/02/07/ChMkJlqY_RuIan7sAAulVLYx4zcAAlEewK65CoAC6Vs300.jpg'
	CHENGP_PRC = 'http://desk.zol.com.cn/showpic/1920x1080_4824_81.html'

class Tmall:
	enm = {
			"zol":{
						
						"base_url" : "http://desk.zol.com.cn/{}/",
						"xpath" : "//a[@class='pic']/@href",
						"title_xpath" : "//a[@class='pic']/img/@title",
						# self.img_xpath = "//ul[@id='J_UlThumb']/li/a/img/@src"
						"xpath_one" : "//ul[@id='showImg']/li/a/img/@srcs",
						"xpath_two" : "//ul[@id='showImg']/li/a/img/@src",
						#zol壁纸的类型对应dict

						"zol_dict":{
									"全部":'pc',
									"风景":'fengjing',
									"动漫":'dongman',
									"美女":'meinv',
									"创意":'chuangyi',
									"卡通":'katong',
									"汽车":'qiche',
									"游戏":'youxi',
									"可爱":'keai',
									"明星":'mingxing',
									"建筑":'jianzhu',"植物":'zhiwu',
									"静物":'jingwu',
									"动物":'dongwu',
									"影视":'yingshi',
									"车模":'chemo',
									"体育":'tiyu',
									"品牌":'pinpai',
									"星座":'xingzuo',
									"美食":'meishi',
									"节日":'jieri',
									"其他":'qita'
								},

						},
			
			"tianmao":{
						"base_url":'https://list.tmall.com/search_product.htm?q={}',
						"xpath" : "//p[@class='productTitle']/a/@href",
						"title_xpath" : "//p[@class='productTitle']/a/@title",
						# self.img_xpath = "//ul[@id='J_UlThumb']/li/a/img/@src",
						"xpath_one" : '//ul[@id="J_UlThumb"]/li/div/a/img/@data-src',
						"xpath_two" : '//ul[@id="J_UlThumb"]/li/a/img/@src',
						}
		}
	


class Xiudian:
	tianmao = {
		"base_url": 'https://list.tmall.com/search_product.htm?q={}',
		"xpath": '//div[@class="productImg-wrap"]/a/@href',
		"title_xpath": "//p[@class='productTitle']/a/@title",
	}
	urls = "http://apibo.logoliqp.com/n/pro/add"
	headers = {
		"Content - Type":"application/json",
		"Authorization":"Bearer 2c2678e175c47bd865267cc39301765d_T"
	}
	bodys = {
			"status": 3,
			"classId": "MD,b01,004",
			"className": "手机数码,手机通讯,手机",
			"title": "",#商品标题
			"subTitle": "",#商品副标题
			"proLabel": "热卖",
			"groupId": "5c7e1ea0ebac5a521b4ef0f4",
			"proImg": "",#商品主图
			"proVideoImg": "",#商品视频主图
			"imageList": [],
			"brandName": "",#商品品牌
			"proType": "3",
			"typeName": "普通",
			"proArea": "中国",
			"attribute": [],#商品属性值
			"sendTime": "0.015",
			"wareHouse": "浙江仓库",
			"returnAddr": "5ca1b8da1a9b0903952d045a",
			"returnTime": "7",
			"noDvaArea": [],
			"limit": "2",
			"remark": [],
			"proAttr": [],
			"detailImgList": [],
			"skulist": [],
			# "logisticsId": "5cb7e6a6a9ca80766c50975a",
}