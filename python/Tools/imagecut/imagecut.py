#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 15:43
# @Author  : 1823218990@qq.com
# @File    : imagecut.py
# @Software: PyCharm
from PIL import Image
import os
path = "/opt/data/public/WordPicture"
psave = "/opt/data/public/WordPicture/word"


# (left, upper, right, lower)
def cut_piture():
    pname = "fe1115cc36004f109c567ea63323ced1.jpeg"
    img = Image.open(os.path.join(path, pname))
    print(img.size)
    all_data = [
        [44, 313, 225, 486, "VCR_录像机"],
        [320, 495, 202, 486, "bookcase_书柜"],
        [517, 756, 227, 486, "cards_扑克牌"],
        [51, 285, 490, 849, "television_电视机"],
    ]

    for d in all_data:
        cropped = img.crop((d[0], d[2], d[1], d[3]))
        wname = d[4] + ".jpeg"
        cropped.save(os.path.join(psave, wname))


def varname(p):
    import inspect, re
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

if __name__ == '__main__':
    # cut_piture()
    vn = [1, 2, 3]
    print(varname(vn))


"""
事件类型	事件格式	事件解释
鼠标事件	<Button-1>	鼠标点击（1-左键，2-中键，3-右键）
        <Double-Button-1>	鼠标双击（1-左键，2-中键，3-右键）
        <B1-Motion>	鼠标拖动（1-左键，2-中键，3-右键）
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











