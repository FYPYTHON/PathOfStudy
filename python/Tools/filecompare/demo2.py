# coding=utf-8
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Menu, Button
from tkinter import LEFT, TOP, X, FLAT, RAISED


class Example(Frame):


        # self.initUI()

    def initUI(self):
        self.master.title("Toolbar")

        menubar = Menu(self.master)
        self.fileMenu = Menu(self.master, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=self.fileMenu)

        toolbar = Frame(self.master, bd=1, relief=RAISED)

        self.img = Image.open("name.ico")
        eimg = ImageTk.PhotoImage(self.img)

        exitButton = Button(toolbar, image=eimg, relief=FLAT,
                            command=self.quit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

    def onExit(self):
        self.quit()

def onExit():
    quit()

def main():
    root = Tk()
    root.geometry("250x150+300+300")

    toolbar = Frame(root, bd=1, relief=RAISED)

    img = Image.open("name.ico")
    eimg = ImageTk.PhotoImage(img)

    exitButton = Button(toolbar, image=eimg, relief=FLAT,
                        command=quit)
    # exitButton.image = eimg
    exitButton.grid(row = 0,column = 1)
    # exitButton.pack(side=LEFT, padx=2, pady=2)
    #
    # toolbar.pack(side=TOP, fill=X)
    # toolbar.config(menu=menubar)
    # toolbar.pack()

    exitButton = Button(root, text=u'按钮2', width=10,
                        command=quit)
    exitButton.grid(row=0, column=1)

    button1 = Button(root, text=u'按钮1', width=10, command=quit)
    button1.grid(row=0, column=2)
    root.mainloop()


if __name__ == '__main__':
    main()