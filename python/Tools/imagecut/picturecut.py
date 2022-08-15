#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 16:32
# @Author  : 1823218990@qq.com
# @File    : imagecut.py
# @Software: PyCharm
"""
activebackground	1. 设置当 Label 处于活动状态（通过 state 选项设置状态）的背景色
                    2. 默认值由系统指定
activeforeground	1. 设置当 Label 处于活动状态（通过 state 选项设置状态）的前景色
                    2. 默认值由系统指定
anchor	1. 控制文本（或图像）在 Label 中显示的位置
        2. "n", "ne", "e", "se", "s", "sw", "w", "nw", 或者 "center" 来定位（ewsn 代表东西南北，上北下南左西右东）
        3. 默认值是 "center"
background	1. 设置背景颜色
            2. 默认值由系统指定
bg	跟 background 一样
bitmap	1. 指定显示到 Label 上的位图
        2. 如果指定了 image 选项，则该选项被忽略
borderwidth	1. 指定 Label 的边框宽度
            2. 默认值由系统指定，通常是 1 或 2 像素
bd	跟 borderwidth 一样
compound	1. 控制 Label 中文本和图像的混合模式
            2. 默认情况下，如果有指定位图或图片，则不显示文本
            3. 如果该选项设置为 "center"，文本显示在图像上（文本重叠图像）
            4. 如果该选项设置为 "bottom"，"left"，"right" 或 "top"，那么图像显示在文本的旁边（如 "bottom"，则图像在文本的下方）
            5. 默认值是 NONE
cursor	1. 指定当鼠标在 Label 上飘过的时候的鼠标样式
        2. 默认值由系统指定
disabledforeground	1. 指定当 Label 不可用的时候前景色的颜色
                    2. 默认值由系统指定
font	1. 指定 Label 中文本的字体(注：如果同时设置字体和大小，应该用元组包起来，如（"楷体", 20）
        2. 一个 Label 只能设置一种字体
        3. 默认值由系统指定
foreground	1. 设置 Label 的文本和位图的颜色
            2. 默认值由系统指定
fg	跟 foreground 一样
height	1. 设置 Label 的高度
        2. 如果 Label 显示的是文本，那么单位是文本单元
        3. 如果 Label 显示的是图像，那么单位是像素（或屏幕单元）
        4. 如果设置为 0 或者干脆不设置，那么会自动根据 Label 的内容计算出高度
highlightbackground	1. 指定当 Label 没有获得焦点的时候高亮边框的颜色
                    2. 默认值由系统指定，通常是标准背景颜色
highlightcolor	1. 指定当 Label 获得焦点的时候高亮边框的颜色
                2. 默认值由系统指定
highlightthickness	1. 指定高亮边框的宽度
                    2. 默认值是 0（不带高亮边框）
image	1. 指定 Label 显示的图片
        2. 该值应该是 PhotoImage，BitmapImage，或者能兼容的对象
        3. 该选项优先于 text 和 bitmap 选项
justify	1. 定义如何对齐多行文本
        2. 使用 "left"，"right" 或 "center"
        3. 注意，文本的位置取决于 anchor 选项
        4. 默认值是 "center"
padx	1. 指定 Label 水平方向上的额外间距（内容和边框间）
        2. 单位是像素
pady	1. 指定 Label 垂直方向上的额外间距（内容和边框间）
        2. 单位是像素
relief	1. 指定边框样式
        2. 默认值是 "flat"
        3. 另外你还可以设置 "groove", "raised", "ridge", "solid" 或者 "sunken"
state	1. 指定 Label 的状态
        2. 这个标签控制 Label 如何显示
        3. 默认值是 "normal
        4. 另外你还可以设置 "active" 或 "disabled"
takefocus	1. 如果是 True，该 Label 接受输入焦点
            2. 默认值是 False
text	1. 指定 Label 显示的文本
        2. 文本可以包含换行符
        3. 如果设置了 bitmap 或 image 选项，该选项则被忽略
textvariable	1. Label 显示 Tkinter 变量（通常是一个 StringVar 变量）的内容
                2. 如果变量被修改，Label 的文本会自动更新
underline	1. 跟 text 选项一起使用，用于指定哪一个字符画下划线（例如用于表示键盘快捷键）
            2. 默认值是 -1
            3. 例如设置为 1，则说明在 Button 的第 2 个字符处画下划线
width	1. 设置 Label 的宽度
        2. 如果 Label 显示的是文本，那么单位是文本单元
        3. 如果 Label 显示的是图像，那么单位是像素（或屏幕单元）
        4. 如果设置为 0 或者干脆不设置，那么会自动根据 Label 的内容计算出宽度
wraplength	1. 决定 Label 的文本应该被分成多少行
            2. 该选项指定每行的长度，单位是屏幕单元
            3. 默认值是 0

Button:
state : normal, disable, active

Canvas:

  rect
    outline = 'red'  边框颜色
    fill = 'red'     背景颜色
    width = 5        线宽
    tags = 'r1'      id
  line
    tags = 'r1'      id
    fill = 'red'     线条颜色

  event
    canvas.tag_bind('r1','<Button-3>',printLine)


事件类型	事件格式	事件解释
鼠标事件	<Button-1>	鼠标点击（1-左键，2-中键，3-右键）
        <Double-Button-1>	鼠标双击（1-左键，2-中键，3-右键）
        <B1-Motion>	鼠标拖动（1-左键，2-中键，3-右键）
        <Motion>   鼠标移动
        <ButtonRelease-1>	鼠标按下之后释放（1-左键，2-中键，3-右键）
        <Enter>	鼠标进入控件范围（widget），不是键盘按键
        <Leave>	鼠标离开控件范围（widget）
键盘事件	<Key>/<KeyPress>	任意键盘按键（键值会以char的格式放入event对象）
        <Return>
        <Cancel>
        <BackSpace>
        <Tab>
        <Shift_L>
        <Control_L>
        <Alt_L>
        <Home>
        <Left>
        <Up>
        <Down>
        <Right>
        <Delete>
        <F1>
        <F2>
对应键盘按键
组件事件	<Configure>	如果widget的大小发生改变，新的大小（width和height）会打包到event发往handler。
        <Activate>	当组件从不可用变为可用
        <Deactivate>	当组件从可用变为不可用
        <Destroy>	当组件被销毁时
        <Expose>	当组件从被遮挡状态变为暴露状态
        <Map>	当组件由隐藏状态变为显示状态
        <Unmap>	当组件由显示状态变为隐藏状态
        <FocusIn>	当组件获得焦点时
        <FocusOut>
        当组件失去焦点时

        <Property>	当组件属性发生改变时
        <Visibility>	当组件变为可视状态时

"""
from tkinter import Tk, Label, PhotoImage, Menu, Canvas, Button, RAISED, SUNKEN, StringVar, Entry
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as msb  # 消息框
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s %(asctime)s]-[line:(lineno)s]: %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

DEFAULT_PATH = "./cutpicture"
if not os.path.exists(DEFAULT_PATH): os.makedirs(DEFAULT_PATH)


class PictureCut(object):
    def __init__(self):
        self.photo = None
        self.ui = Tk()
        self.ui.title('pcut')

        # 宽x高+偏移量(相对于屏幕)=width*height+xpos+ypos
        self.ui.geometry('600x400+532+244')
        self.img = None
        self.img_canvas = None
        self.imgw = 0
        self.imgh = 0
        self.filename = None
        self.tempname = None
        self.cutbtn = None
        self.cache = []
        self.savename = None
        self.savebtn = None
        self.step = 150
        self.rate = 1
        # tool
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.bh = None
        self.bv = None
        self.line = "h"
        self.tip = None
        self.msg = None
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.dash = 1  # 虚线
        # init
        self.menubar = Menu(self.ui)
        self.menus = {}
        self.init()
        # self.initView()

    def init(self):
        self.add_menu('File', [
            {'name': 'Open File', 'command': self.open_img},
            {'name': 'Exit', 'command': self.pcutexit, 'accelerator': 'Alt+F4'}
        ])

    def add_menu(self, menuName, commandList):
        self.menus[menuName] = Menu(self.menubar, tearoff=0)
        for c in commandList:
            if 'separator' in c:
                self.menus[menuName].add_separator()
            else:
                self.menus[menuName].add_command(label=c['name'], command=c['command'],
                                                 accelerator=c['accelerator'] if 'accelerator' in c else '')
        self.menubar.add_cascade(label=menuName, menu=self.menus[menuName])
        self.ui.config(menu=self.menubar)

    def initView(self):
        xstart = self.imgw + 10
        self.x1 = Label(self.ui, text="x1")
        self.x1.place(x=xstart, y=10)
        self.x2 = Label(self.ui, text="x2")
        self.x2.place(x=xstart, y=40)
        self.y1 = Label(self.ui, text="y1")
        self.y1.place(x=xstart, y=70)
        self.y2 = Label(self.ui, text="y2")
        self.y2.place(x=xstart, y=100)

        self.tip = Label(self.ui)
        self.tip.place(x=0, y=self.imgh + 10)

        self.msg = Label(self.ui, fg="red")
        self.msg.place(x=0, y=self.imgh + 30)

        self.bh = Button(self.ui, text="——")
        self.bh.place(x=xstart, y=140)
        self.bh.bind("<Button-1>", self.bhClick)

        self.bv = Button(self.ui, text=" | ")
        self.bv.bind("<Button-1>", self.bvClick)
        self.bv.place(x=xstart + 50, y=140)

        labeltip = Label(self.ui, text=u"文件名(picture_图片)：")
        labeltip.place(x=xstart, y=180)

        savename = StringVar()
        savename.set("")
        self.savename = Entry(self.ui, textvariable=savename)
        self.savename.place(x=xstart, y=210)

        self.savebtn = Button(self.ui, text="save", relief=RAISED)
        self.savebtn.place(x=xstart, y=240)
        self.savebtn.bind("<Button-1>", self.cut_piture)

    def bhClick(self, event):
        self.bh['state'] = "disable"
        self.bh['relief'] = SUNKEN

        self.bv['state'] = "normal"
        self.bv['relief'] = RAISED

        self.line = "h"

    def bvClick(self, event):
        self.bv['state'] = "disable"
        self.bv['relief'] = SUNKEN

        self.bh['state'] = "normal"
        self.bh['relief'] = RAISED

        self.line = "v"

    def setLabelValue(self):
        self.x1['text'] = u"左: " + str(self.left)
        self.y1['text'] = u"上: " + str(self.top)
        self.x2['text'] = u"右: " + str(self.right)
        self.y2['text'] = u"下: " + str(self.bottom)

    def clearLabelValue(self):
        self.top, self.bottom, self.left, self.right = 0, 0, 0, 0
        self.setLabelValue()

    def DrawLine(self, event):
        if len(self.cache) == 2:
            if self.line == "h":
                self.line = "v"
                self.bvClick("")
            else:
                self.line = "h"
                self.bhClick("")
            pass
        if self.line == "h":
            # dash=10
            # line = self.img_canvas.create_line(10, 10, 100, 10)
            if len(self.cache) > 3:
                logger.error("cache len 4")
                msb.showerror("Error", u"已有四条线")
                pass
            else:
                x1 = event.x - self.step if event.x - self.step > 0 else 0
                x2 = event.x + self.step if event.x + self.step < self.imgw else self.imgw
                if self.top == 0 and self.bottom == 0:
                    self.top, self.bottom = event.y, event.y
                if event.y > self.top:
                    self.bottom = event.y
                else:
                    self.top, self.bottom = event.y, self.bottom
                # print(x1, event.y, x2, event.y)
                # outline='blue',fill='red'
                line = self.img_canvas.create_line(x1, event.y, x2, event.y, dash=self.dash, fill='red')
                self.cache.append(line)

            pass
        else:
            print(event.x, event.y)
            if len(self.cache) > 3:
                logger.error("cache len 4")
                msb.showerror("Error", u"已有四条线")
                pass
            else:
                y1 = event.y - self.step if event.y - self.step > 0 else 0
                y2 = event.y + self.step if event.y + self.step < self.imgh else self.imgh
                if self.left == 0 and self.right == 0:
                    self.left, self.right = event.x, event.x
                else:
                    if event.x > self.left:
                        self.right = event.x
                    else:
                        self.left, self.right = event.x, self.left
                # print(event.x, y1, event.x, y2)
                line = self.img_canvas.create_line(event.x, y1, event.x, y2, dash=self.dash, fill="red")
                self.cache.append(line)
            pass
        self.setLabelValue()

    def CancleLine(self, event):

        if len(self.cache) > 0:
            item = self.cache[-1]
            logger.info("delete line {}".format(item))
            for item in self.cache:
                self.img_canvas.delete(item)
                # self.cache.pop()
            self.cache = []
            self.clearLabelValue()
        else:
            logger.error("no line in cache")
            pass

    def ShowPos(self, event):
        self.tip['text'] = "x:{}, y:{}".format(event.x, event.y)
        pass

    def initImage(self):
        # self.photo = PhotoImage(file="temp.gif")
        # self.img_label = Label(self.ui, image=self.photo, relief="solid")
        # self.img_label.image = self.photo
        # self.img_label.place(x=10, y=10)
        #
        self.img = Image.open(self.filename)
        logger.info("ori img size: {}".format(self.img.size))
        self.imgw, self.imgh = self.img.size[0] // self.rate, self.img.size[1] // self.rate

        curw = self.imgw + 210
        curh = self.imgh + 50 if self.imgh > 280 else 280

        logger.info("cur size: {}".format((curw, curh)))
        self.ui.geometry('{}x{}+532+244'.format(curw, curh))
        self.initView()
        # self.photo = PhotoImage(img)

        self.photo = PhotoImage(file=self.tempname, width=self.imgw, height=self.imgh)
        self.img_canvas = Canvas(self.ui, relief="solid", width=self.imgw, height=self.imgh)
        self.img_canvas.place(x=0, y=0)
        self.img_canvas.bind("<Button-1>", self.DrawLine)
        self.img_canvas.bind("<Motion>", self.ShowPos)
        self.img_canvas.bind("<Button-3>", self.CancleLine)

        img = self.img_canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def open_img(self):
        self.filename = askopenfilename(initialdir=DEFAULT_PATH, filetypes=[('All Files', '*.jpeg;*.jpg;*.png;*.gif')])
        logger.info("filename select:{}".format(self.filename))
        if self.filename is not None:
            suffix = os.path.splitext(self.filename)[1]
            if suffix and suffix.lower() != ".gif":
                self.jpegTogif()
            else:
                self.tempname = self.filename
            self.initImage()
        else:
            self.img = None
            msb.showerror("Error", u"文件格式不匹配（jpeg,jpg,png,gif）")

    def jpegTogif(self):
        img = Image.open(self.filename)
        if img.size[1] > 600:
            self.rate = 2
            rsize = (img.size[0] // self.rate, img.size[1] // self.rate)
            img = img.resize(rsize, Image.ANTIALIAS)
        else:
            self.rate = 1
        img.save("temp.gif", "gif")
        # self.img = Image.open("temp.png")
        self.tempname = "temp.gif"

    def cut_piture(self, event):
        cropped = self.img.crop((self.left * self.rate, self.top * self.rate,
                                 self.right * self.rate, self.bottom * self.rate))
        wname = self.savename.get()
        if wname == "":
            msb.showerror("Error", u"保存文件名不能为空")
            return
        else:
            wname = wname + ".gif"
        logger.info("{} saved.".format(wname))
        cropped.save(os.path.join(DEFAULT_PATH, wname))
        msb.showinfo("Info", u"{} 已保存".format(wname))

        self.CancleLine("")
        self.clearLabelValue()
        self.savebtn['state'] = "normal"
        self.msg['text'] = "{} saved".format(wname)
        return None

    def pcutexit(self):
        self.ui.destroy()


if __name__ == "__main__":
    # C:\softDev\python35\Lib\site-packages\PyInstaller
    # pyinstaller kafka_client.py -w -F --icon="kafka.ico" --upx-dir ../upx-3.95-win64/upx.exe
    demo = PictureCut()
    demo.ui.mainloop()
    logger.info("picture cut main loop start ...")
