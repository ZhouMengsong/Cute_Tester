import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from mall_download import Imgdown
import time

window = tk.Tk()
window.title('my window')
window.geometry('300x300')
v = StringVar()
v.set('tianmao')


#zol壁纸的类型对应dict

zol_dict = {
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
}


def print_selection():
    # a.config(text=v.get())
    if v.get() == 'tianmao':
        a2.current()
        a2['values'] = ('50x50','400x400','800x800')
        e1.config(state='disabled')
        e.config(state='normal')
    if v.get() == 'zol':
        a2.current()
        a2['values'] = ('1024x768','1280x800','1280x1024','1366x768','1440x900','1600x900','1680x1050','1920x1080',
        	'1920x1200','2560x1600','2880x1800')
        e.delete(0,END)
        e.config(state='readonly')
        e1.config(state='normal')
		# e['values'] = ("全部","风景","动漫","美女","创意","卡通","汽车","游戏","可爱","明星","建筑","植物","静物","动物","影视",
		# 	"车模","体育","品牌","星座","美食","节日","其他")


menu = tk.Radiobutton(window,text='天猫',variable = v,value = 'tianmao',command=print_selection).pack(anchor = W)
menu1 = tk.Radiobutton(window,text='ZOL壁纸',variable = v,value = 'zol',command=print_selection).pack(anchor = W)

a = tk.Label(window,text="请输入下载的图片名称")
a.pack()
e = tk.Entry(window,show=None)
e.pack()
e1 = ttk.Combobox(window,state='disabled')
e1['values'] = ("全部","风景","动漫","美女","创意","卡通","汽车","游戏","可爱","明星","建筑","植物","静物","动物","影视",
			"车模","体育","品牌","星座","美食","节日","其他")
e1.current()
e1.pack()


def selectpath():
    path_ = askdirectory()
    path.set(path_)

path = StringVar()
a1 = tk.Button(window,text='选择下载路径',width=15,
            height=1,command=selectpath)
a1.pack()

c = tk.Entry(window,show=None,textvariable=path,state='readonly')
c.pack()

d = tk.Label(window,text='选择下载的图片格式')
d.pack()
a2 = ttk.Combobox(window)
a2['values'] = ('50x50','400x400','800x800')
a2.current()
a2.pack()

f = tk.Label(window,text='选择下载商品个数')
f.pack()
f1 = tk.Entry(window,show=None)
f1.insert(0,'1')
f1.pack()

def insert_point():
    p, name, road, size, num = v.get(), e.get(), c.get(), a2.get(), f1.get()
    if name == '':
    	# name = e1.get()
    	name = zol_dict.get(e1.get())
    if name == '' or road == '':
        tk.messagebox.showerror('错误','请输入完整信息后下载')
        return
    print(name,road,size)
    e.config(state='readonly')
    c.config(state='readonly')
    a1.config(state='disabled')
    a2.config(state='disabled')

    f1.config(state='disabled')
    b1.config(state="disabled",text='下载中')
    try:
        # print(v.get())
        print(Imgdown(p).get_html(name,road,size,int(num)))
        time.sleep(2)
        e.config(state='normal')
        c.config(state='normal')
        a1.config(state='normal')
        a2.config(state='normal')
        f1.config(state='normal')
        b1.config(state="normal",text='下载完成')
    except Exception:
        tk.messagebox.showerror('错误','下载失败'+Exception)
        e.config(state='normal')
        c.config(state='normal')
        a1.config(state='normal')
        a2.config(state='normal')
        f1.config(state='normal')
        b1.config(state="normal",text='重新下载')
        return
        

def insert_end():
    var = e.get()
    t.insert('end',var)
b1 = tk.Button(window,text='下载',width=15,
            height=2,command=insert_point)
b1.pack()

window.mainloop()
