#coding=utf-8

from tkinter import Tk
from tkinter import ttk
from tkinter import Frame
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import Button,RAISED,FLAT,LEFT,TOP,X
class Demo:
    def __init__(self):
        self.ui = Tk()
        # self.ui.mainloop()
        self.ui.title('Demo')
        self.ui.geometry('800x600+100+100') # 宽x高+偏移量
        self.ui.iconbitmap('name.ico')
        print self.ui.winfo_x(),self.ui.winfo_y()
        self.setup_ui()


    def start(self):
        self.ui.iconbitmap('name.ico')
        print self.ui.winfo_x(), self.ui.winfo_y()


    def setup_ui(self):
        # self.createToolbar()

        self.setup_label()
        self.setup_button()
        import pdb
        pdb.set_trace()
        self.createToolbar()

    def createToolbar(self):
        toolbar = Frame(self.ui, bd=1, relief=RAISED)

        img = Image.open("name.ico")
        eimg = ImageTk.PhotoImage(img)

        exitButton = Button(toolbar, image=eimg, relief=FLAT,
                            command=quit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)
        #
        toolbar.pack(side=TOP, fill=X)
        # toolbar.config(menu=menubar)
        toolbar.pack()


    def quit(self):
        self.ui.quit()

    def setup_label(self):
        label = ttk.Label(self.ui, text=u'标签1')
        label.grid(row=0,column = 1)
    def setup_button(self):
        button1 = ttk.Button(self.ui, text=u'按钮1',width=10, command=self.clicked)
        button1.grid(row=1,column=2)


    def clicked(self):
        action = ttk.Entry(self.ui,text=u"请输入...")
        labe2 = ttk.Label(self.ui, text=u'标签1')
        labe2.grid(row=1, column=1)
        print 'clicked...'


if __name__ == "__main__":
    demo = Demo()
    # demo.start()
    demo.ui.mainloop()


