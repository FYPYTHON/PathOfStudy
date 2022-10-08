#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/1 12:09
# @Author  : 1823218990@qq.com
# @File    : note_scrapy
# @Software: Pycharm


import time
import platform
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
if platform.system() == "Windows":
    dr = webdriver.Chrome("D:\workSpace\chromedriver104_win32\chromedriver.exe")
else:
    print("not windows env can not run this function.")
    exit(0)
# first_chapte="https://www.58160.com/97/97068/72287604.html"
# first_chapte="http://www.cits0871.com/booktxt/41448/23825494.html"
first_chapte="http://www.cits0871.com/booktxt/51643/29674103.html"

f = open("D:/daxiawensheng.txt", "w+")
def gene_all():
    dr.get(first_chapte)
    time.sleep(0.2)
    title = dr.find_element_by_tag_name("h1").text
    first_cxt = dr.find_element_by_id("content").find_elements_by_tag_name("p")
    # first_cxt = dr.find_element_by_id("content")
    # print(first_cxt.text)
    f.write(title)
    f.write("\n")
    # f.write(first_cxt.text)
    # f.write("\n")
    # 无多个
    for px in first_cxt:
        # print(px.text)
        f.write(px.text)
        f.write("\n")

    # next_a = dr.find_element_by_id("next_url")     # id选择器
    # next_a = dr.find_element_by_class_name("next")
    # other next
    next_a = None
    next_content = dr.find_element_by_class_name("bottem2")
    next_content = next_content.find_elements_by_tag_name('a')
    print(next_content)
    for next in next_content:
        if next.text == "下一章":
            next_a = next
            break
    next_txt = next_a.text
    next_url = next_a.get_attribute("href")
    print(title)
    print(next_url)
    print(next_txt)
    # return
    while next_txt == "下一章":
        dr.get(next_url)
        time.sleep(1)
        title = dr.find_element_by_tag_name("h1").text
        first_cxt = dr.find_element_by_id("content").find_elements_by_tag_name("p")
        # first_cxt = dr.find_element_by_id("content")
        f.write(title)
        f.write("\n")
        # f.write(first_cxt.text)
        # f.write("\n")
        # 无多列
        for px in first_cxt:
            # print(px.text)
            try:
                f.write(px.text)
            except Exception as e:
                print(e)
                pass
            f.write("\n")
        # next_a = dr.find_element_by_id("next_url")     # id选择器
        # next_a = dr.find_element_by_class_name("next")
        # other next
        next_a = None
        next_content = dr.find_element_by_class_name("bottem2").find_elements_by_tag_name('a')
        for next in next_content:
            if next.text == "下一章":
                next_a = next
                break
        next_txt = next_a.text
        next_url = next_a.get_attribute("href")
        print(title)
        print(next_url)
        print(next_txt)
        pass



gene_all()
f.close()
dr.close()



