from lib.request import Base
from config import url_path
import json
import os
import re
import requests
import random



class ProApi(Base, url_path.Xiudian):
    """docstring for ProApi"""

    def __init__(self):
        super(ProApi, self).__init__()
        self.base_url = self.tianmao.get('base_url')
        self.xpath = self.tianmao.get('xpath')
        self.title_xpath = self.tianmao.get('title_xpath')
        self.header = self.headers
        self.data = self.bodys
        self.addapi = self.urls

    # 如果图片地址没有http，加上并返回
    def url_header(self, url):
        if ('https:' or 'http:') in url[:6]:
            return url
        elif 'bizhi' in url:
            return 'http://desk.zol.com.cn' + url
        else:
            return 'https:' + url

    # 裁剪图片尺寸，并返回图片地址
    def url_re(self, url, size):
        if 'png' in url:
            url_ = url.split('.png')[:-1]
            n = ''.join(url_)
            return n + '.png_' + size + '.jpg'

        elif 'jpg_' in url:
            new_url = url.split('.jpg')[:-2]
            new = ''.join(new_url)
            return new + '.jpg_' + size + '.jpg'

        elif 'desk' in url:
            return url.replace('144x90', size)

        else:
            return url


    #传入商品地址，返回商品规格的dict
    def sku_info(self,url,tb=1):
        """tb:1返回规格dict   2返回商品轮播图list"""
        p_bq = self.output(url, '//div[@class="tb-key"]//dt/text()')[:-2]  # 获取商品规格名

        pro_info = self.output(url, '//*[@id="J_DetailMeta"]/div/script[3]/text()')
        ru = re.compile(r'({).*}')
        reslut = re.search(ru, pro_info[0].split('Setup')[-1])
        item_info = json.loads(reslut.group())
        # print(item_info)
        skulist = item_info.get("valItemInfo").get("skuList")
        skuprice = item_info.get("valItemInfo").get("skuMap")
        try:
            skuimg = item_info.get("propertyPics")
            proimg_list = skuimg.get("default")
        except Exception as e:
            return e
        else:
            pass
        if tb == 1:
            return  self.pro_p_and_i(p_bq, skulist, skuprice, skuimg)
        if tb == 2:
            return proimg_list


    #传入商品地址，返回商品规格的dict
    def pro_sku(self,url):
        # 获取对应的规格和规格值列表
        p_bq = self.output(url, '//div[@class="tb-key"]//dt/text()')[:-2]  # 获取商品规格名
        all = []
        index = 1
        for p in p_bq:
            p_bq_c = self.output(url,'//div[@class="tb-key"]//dl[{}]/dd/ul/li/span/text()'.format(index))
            # pro_color = self.output(url,'//div[@class="tb-key"]//dl[{}]/dd/ul/li/a/@style'.format(index))
            if not p_bq_c:
                p_bq_c = self.output(url,'//div[@class="tb-key"]//dl[{}]/dd/ul/li/a/span/text()'.format(index))
            if not p_bq_c:
                p_bq_c = self.output(url,'//div[@class="tb-key"]//dl[{}]/dd/ul/li/a/text()'.format(index))
            # print(p_bq_c)
            all = all+ self.pro_guige(p,p_bq_c)
            index += 1
        return all


    def pro_guige(self, pro, pv_list):
        # print(pk_list)
        # print(pv_list)
        proAttr = []
        x_num = 1
        # 遍历规格值，获得对应的规格值组成dict
        # for a in pk_list:
        # 	# proAttr_one.append(p_bq_c)
        children = []
        for c in pv_list:
            p_d_one = {
                "model": c,
                "apeciErr": True,
                "isCheck": True
            }
            children.append(p_d_one)

        p_d = {
            "value": pro,
            "isCheck": True,
            "isClearBtn": True,
            "children": children
        }
        proAttr.append(p_d)
        x_num += 1

        return proAttr

    def pro_p_and_i(self, p_list, sku_list, price_list, img_list):
        skulist = []
        for i in sku_list:#遍历规格
            names = i.get('names').split(' ')#获得规格值
            pvs = i.get('pvs')#获得规格pvs
            skuid = i.get('skuId')#获取规格id
            for j in price_list.values():
                if skuid == j.get('skuId'):
                    for n in img_list.keys():
                        if n[1:-1] in pvs:
                            si = img_list.get(n)[0]
                            sp = j.get('price')
                            ss = j.get('stock')
                            sl = []
                            for l in range(len(p_list)):
                                aa = {
                                    p_list[l]: names[l]
                                }
                                sl.append(aa)
                            skuinfo = {
                                "skuAttr": sl,
                                "skuImg": si,
                                "distPrice": float(sp),
                                "stock": ss,
                                "price": float('%.2f' % (float(sp)*0.8)),
                                "salePrice": float('%.2f' % (float(sp)*0.8)),
                                "artCode": skuid,
                                "barCode": pvs,
                                "weight": 0.15
                            }
                            skulist.append(skuinfo)
        return skulist

    #获取商品属性
    def pro_xq(self,url):
        xq_list = self.output(url,'//ul[@id="J_AttrUL"]/li/text()')
        attribute = []
        for i in xq_list:
            a = {
                "name": i.split('：')[0] if '：'in i else i.split(':')[0],
                "value": i.split('：')[-1] if '：'in i else i.split(':')[-1]
            }
            attribute.append(a)
        return attribute

    #获取商品详情图
    def pro_xq_img(self,url):
        xq_img = self.outputall(url,'//div[@id="description"]//p/img/@src')
        return xq_img

    #对接秀店商家后台主接口,传入商品名称和商品数量
    def add_pro(self,name,num,logisticsId,addressId):
        new_url = self.base_url.format(name)
        print(new_url)
        pro_list = self.output(new_url, self.xpath)  # 获取页面的所有商品地址list
        # pro_tit = self.output(new_url, self.title_xpath)
        m = 0
        result_list = []
        for i in pro_list[:num]:
            print(i)
            url = self.url_header(i)
            # self.pro_xq(url)
            pro_tit = self.output(url, '//div[@id="J_DetailMeta"]//h1/a/text()') + self.output(url, '//div[@id="J_DetailMeta"]//h1/text()')
            pro_fu_tit = self.output(url, '//div[@class="tb-detail-hd"]/p/text()')
            new_data = self.data
            # print(new_data)
            all_img = self.sku_info(url,tb=2)
            xq_img = self.pro_xq_img(url)
            try:
                new_data['title'] = pro_tit[0].strip()
                new_data['subTitle'] = pro_fu_tit[0].strip()
                new_data['proImg'] = all_img[0]
                # new_data['proVideoImg']
                new_data['imageList'] = all_img
                new_data['brandName'] = name
                new_data['attribute'] = self.pro_xq(url)
                new_data['proAttr'] = self.pro_sku(url)
                new_data['detailImgList'] = xq_img   #暂时无法抓取的动态图片，先用轮播图代替
                new_data['skulist'] = self.sku_info(url)
                new_data['logisticsId'] = logisticsId
                new_data['returnAddr'] = addressId
            except Exception as e:
                print(e)
            # new_data = json.loads(new_data)
            # print(type(new_data), new_data)
            rsp = requests.Session().post(self.addapi,json=new_data,headers=self.header).json()
            # print(rsp)
            result_list.append(rsp)
            m += 1
        return result_list

    #输入商家后台用户名和密码，新增商品的名称，类似商品的数量
    def main_fuc(self,user,pwd,pro_name,pro_num):
        #调用登录接口获取用户token
        user_token = requests.Session().post('http://apibo.logoliqp.com/n/trader/login',json={"account":user,"password":pwd}).json()
        self.header['Authorization'] = "Bearer "+user_token.get('result').get('token')
        #调用查询退货地址获取id
        return_re= requests.Session().get('http://apibo.logoliqp.com/n/address?pageSize=10&pageIndex=1', headers=self.header).json()
        addressId = return_re.get('result').get('data')[0].get('id')
        #获取运费模板id
        logistics = requests.Session().get('http://apibo.logoliqp.com/n/logistics/list?pageSize=10&pageIndex=1',headers=self.header).json()
        logisticsId = logistics.get('result').get('data')[0].get('id')
        rsp = self.add_pro(pro_name,pro_num,logisticsId,addressId)
        n = 0
        for i in rsp:
            if i.get('code') == '0000':
                n += 1
        print('新增商品成功,一共新增商品{}条'.format(n),'其中新增失败{}条'.format(len(rsp)-n))






if __name__ == '__main__':
    pass
    # print(ProApi().get_html('小米9', int(1)))
    # print(ProApi().pro_xq('http://detail.tmall.com/item.htm?id=589192455077&skuId=4200326178501&sku=10016:319258063&user_id=1714128138&cat_id=50024400&is_b=1&rn=347da55ee636783bb694a0a01b677707'))
    print(ProApi().main_fuc('zhou1234','zhou1234','电热水壶', int(5)))
    # print(ProApi().pro_xq_img('http://detail.tmall.com/item.htm?id=579794586729&skuId=3856455121119&user_id=2616970884&cat_id=2&is_b=1&rn=5e020aa499b1bed90b39ac6ee81f00b6'))