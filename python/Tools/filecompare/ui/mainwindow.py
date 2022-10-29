# coding=utf-8
import os, mimetypes, filecmp
from difflibparser.difflibparser import *
from ui.mainwindow_ui import MainWindowUI
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory    # 文件、路径对话框
from tkinter.simpledialog import askstring
# from PIL import ImageTk , Image
from tkinter import messagebox as msb    # 消息框
from tkinter import messagebox as mBox   # 弹框
from PyUiFileCompare import DEFAULT_PATH

QUOTE = """
Copyright (c) 2016 Yasser Elsayed
Modify：feiying 2018-4-27
--- 2018-05-03 ---
1、增加比较结果输出文件功能；
2、增加工具栏，可显示不同部分和所有部分；
"""


class MainWindow:
    def __init__(self, leftpath=None, rightpath=None, ico=None):
        self.main_window = Tk()
        print('窗口位置：', self.main_window.winfo_x(), self.main_window.winfo_y())
        # self.main_window.iconbitmap(ico)
    # def start(self, leftpath = None, rightpath = None ,ico = None):
        # self.main_window = Tk()

        self.main_window.title('File Compare Based on Python Ui & Difflib 1.1')

        self.__main_window_ui = MainWindowUI(self.main_window)
        self.leftFile = ''
        self.rightFile = ''
        self.outputLeft = ''     # 输出基准文件结果
        self.outputRight = ''    # 输出比较文件结果
        self.type = 1            # 所有部分=1 或者 不同部分=0
        self.__main_window_ui.center_window()
        self.main_window.iconbitmap(ico)   # 设置geometry之后

        self.__main_window_ui.create_file_path_labels()
        self.__main_window_ui.create_text_areas()
        self.__main_window_ui.create_search_text_entry(self.__findNext)
        self.__main_window_ui.create_line_numbers()
        self.__main_window_ui.create_tree_buttons()
        self.__main_window_ui.create_scroll_bars()
        self.__main_window_ui.create_file_treeview()
        path_to_my_project = os.getcwd()
        print('窗口位置：', self.main_window.winfo_x(), self.main_window.winfo_y())
        self.__main_window_ui.add_menu('File', [
            {'name': 'Compare Files', 'command': self.__browse_files},
            # {'name': 'Compare Directories', 'command': self.__browse_directories},
            {'name': 'Compare File & Directories','command':self.__browse_file_directories},
            {'separator'},
            {'name': 'Exit', 'command': self.__exit, 'accelerator': 'Alt+F4'}
            ])
        self.__main_window_ui.add_menu('Edit', [
            {'name': 'Find', 'command': self.__startFindText, 'accelerator': 'Ctrl+F'},
            {'separator'},
            {'name': 'Cut', 'command': self.__cut, 'accelerator': 'Ctrl+X'},
            {'name': 'Copy', 'command': self.__copy, 'accelerator': 'Ctrl+C'},
            {'name': 'Paste', 'command': self.__paste, 'accelerator': 'Ctrl+P'},
            {'separator'},
            {'name': 'Go To Line', 'command': self.__goToLine, 'accelerator': 'Ctrl+G'}
            ])
        self.__main_window_ui.add_menu('Print', [
            # {'name': 'Print', 'command': self.__output_result_into_file, 'accelerator': 'Ctrl+P'},
            {'name':'Print All','command':self.__output_results_into_files,'accelerator':'Ctrl+O'}
        ])
        self.__main_window_ui.add_menu('Help', [
            {'name': 'About', 'command': self.__helpInfo,'accelerator': 'Ctrl+H'}
        ])

        self.__main_window_ui.fileTreeView.bind('<<TreeviewSelect>>', lambda *x:self.treeViewItemSelected())

        # 创建工具栏
        self.__createToolbar()

        if (leftpath and os.path.isdir(leftpath)) or (rightpath and os.path.isdir(rightpath)):
            self.__load_directories(leftpath, rightpath)
        else:
            self.leftFile = leftpath if leftpath else ''
            self.rightFile = rightpath if rightpath else ''
            self.filesChanged()

        self.__bind_key_shortcuts()

    def start(self):
        self.main_window.mainloop()

    def __createToolbar(self):
        # img = Image.open("./diff.png")
        # eimg = ImageTk.PhotoImage(img)
        # self.__main_window_ui.fileTreeView.grid()
        # self.__main_window_ui.fileTreeYScrollbar.grid()
        # self.__main_window_ui.fileTreeXScrollbar.grid()
        # self.__main_window_ui.fileTreeView.delete(*self.__main_window_ui.fileTreeView.get_children())
        same = Button(self.main_window, text=u'all', width=8, anchor='center', relief=GROOVE,fg='blue'
                      , command=lambda:self.filesChangedByType(1))
        same.image = 'name.ico'
        same.grid(row=0, column = 0, columnspan=1, sticky=E)
        # same.pack(side=LEFT, padx=2, pady=2)   # columnspan=2
        diff = Button(self.main_window, text=u'diff', width=8, anchor='center',relief=GROOVE, fg='red'
                      ,command= lambda:self.filesChangedByType(0))
        diff.grid(row=0, column = 2, columnspan=1, sticky=E)

    def __bind_key_shortcuts(self):
        self.main_window.bind('<Control-f>', lambda *x: self.__startFindText())
        self.main_window.bind('<Control-g>', lambda *x: self.__goToLine())
        self.main_window.bind('<Escape>', lambda *x: self.__endFindText())
        self.main_window.bind('<F3>', self.__main_window_ui.searchTextDialog.nextResult)

    # 文件之间比较
    def __browse_files(self):
        BoolChooseLeft = self.__message_askbox('Info', 'Choose a basic file')
        if BoolChooseLeft:
            self.__load_file('left')
        else:
            return
        BoolChooseRight = self.__message_askbox('Info', 'Choose a file to compare')
        if BoolChooseRight:
            self.__load_file('right')
        else:
            return
        if self.leftFile == '':
            return
        if self.rightFile == '':
            return
        self.filesChanged()
        self.__main_window_ui.fileTreeView.grid_remove()
        self.__main_window_ui.fileTreeYScrollbar.grid_remove()
        self.__main_window_ui.fileTreeXScrollbar.grid_remove()

    # Load directories into the treeview
    def __browse_directories(self):
        leftDir = self.__load_directory('left')
        rightDir = self.__load_directory('right')
        self.__load_directories(leftDir, rightDir)

    def __load_directories(self, leftDir, rightDir):
        if leftDir and rightDir:
            self.__main_window_ui.fileTreeView.grid()
            self.__main_window_ui.fileTreeYScrollbar.grid()
            self.__main_window_ui.fileTreeXScrollbar.grid()
            self.__main_window_ui.fileTreeView.delete(*self.__main_window_ui.fileTreeView.get_children())
            self.__browse_process_directory('', leftDir, rightDir)

    # Recursive method to fill the treevie with given directory hierarchy
    def __browse_process_directory(self, parent, leftPath, rightPath):
        if parent == '':
            leftPath = leftPath.rstrip('/')
            rightPath = rightPath.rstrip('/')
            leftDirName = os.path.basename(leftPath)
            rightDirName = os.path.basename(rightPath)
            self.__main_window_ui.fileTreeView.heading('#0', text=leftDirName + ' / ' + rightDirName, anchor=W)
        leftListing = os.listdir(leftPath)
        rightListing = os.listdir(rightPath)
        mergedListing = list(set(leftListing) | set(rightListing))
        for l in mergedListing:
            newLeftPath = leftPath + '/' + l
            newRightPath = rightPath + '/' + l
            bindValue = (newLeftPath, newRightPath)
            # Item in left dir only
            if l in leftListing and l not in rightListing:
                self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue,
                                                          open=False, tags=('red', 'simple'))
            # Item in right dir only
            elif l in rightListing and l not in leftListing:
                self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue,
                                                          open=False, tags=('green', 'simple'))
            # Item in both dirs
            else:
                # If one of the diffed items is a file and the other is a directory,
                # show in yellow indicating a difference
                if (not os.path.isdir(newLeftPath) and os.path.isdir(newRightPath)) or (os.path.isdir(newLeftPath)
                                                  and not os.path.isdir(newRightPath)):
                    self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue,
                                                              open=False, tags=('yellow', 'simple'))
                else:
                    # If both are directories, show in white and recurse on contents
                    if os.path.isdir(newLeftPath) and os.path.isdir(newRightPath):
                        oid = self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, open=False)
                        self.__browse_process_directory(oid, newLeftPath, newRightPath)
                    else:
                        # Both are files. diff the two files to either show them in white or yellow
                        if filecmp.cmp(newLeftPath, newRightPath):
                            oid = self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue,
                                                                            open=False, tags=('simple',))
                        else:
                            oid = self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue,
                                                                            open=False, tags=('yellow', 'simple'))

    def __load_file(self, pos):
        """
        title: dialog title
        multiple: if true user may select more than one file
        initialdir: initial directory.  preserved by dialog instance.
        filetypes: sequence of (label, pattern) tuples.  the same pattern may occur wit
        eg: file_path=askopenfilename(title='Select the diagnostic instrument .exe file',
                                      filetypes=[('EXE', '*.exe'), ('All Files', '*')],
                                      initialdir='C:\\Windows\\files')
        """
        fname = askopenfilename(initialdir=DEFAULT_PATH, filetypes=[('All Files', '*')])
        if fname:
            if pos == 'left':
                self.leftFile = fname
            else:
                self.rightFile = fname
            return fname
        else:
            return None

    def __load_directory(self, pos):
        dirName = askdirectory()
        if dirName:
            if pos == 'left':
                self.__main_window_ui.leftFileLabel.config(text=dirName)
            else:
                self.__main_window_ui.rightFileLabel.config(text=dirName)
                self.rightFile = dirName   # 记录文件路径
            return dirName
        else:
            return None

    # Callback for changing a file path
    def filesChanged(self):
        self.__main_window_ui.leftLinenumbers.grid_remove()
        self.__main_window_ui.rightLinenumbers.grid_remove()

        if not self.leftFile or not self.rightFile:
            self.__main_window_ui.leftFileTextArea.config(background=self.__main_window_ui.grayColor)
            self.__main_window_ui.rightFileTextArea.config(background=self.__main_window_ui.grayColor)
            return

        if os.path.exists(self.leftFile):
            self.__main_window_ui.leftFileLabel.config(text=self.leftFile)
            self.__main_window_ui.leftFileTextArea.config(background=self.__main_window_ui.whiteColor)
            self.__main_window_ui.leftLinenumbers.grid()
        else:
            self.__main_window_ui.leftFileLabel.config(text='')

        if os.path.exists(self.rightFile):
            self.__main_window_ui.rightFileLabel.config(text=self.rightFile)
            self.__main_window_ui.rightFileTextArea.config(background=self.__main_window_ui.whiteColor)
            self.__main_window_ui.rightLinenumbers.grid()
        else:
            self.__main_window_ui.rightFileLabel.config(text='')

        self.diff_files_into_text_areas()

    def treeViewItemSelected(self):
        item_id = self.__main_window_ui.fileTreeView.focus()
        paths = self.__main_window_ui.fileTreeView.item(item_id)['values']
        if paths == None or len(paths) == 0:
            return
        self.leftFile = paths[0]
        self.rightFile = paths[1]
        self.filesChanged()

    # Insert file contents into text areas and highlight differences
    def diff_files_into_text_areas(self):
        try:
            leftFileContents = open(self.leftFile).read()
        except:
            leftFileContents = ''
        try:
            rightFileContents = open(self.rightFile).read()
        except:
            rightFileContents = ''

        diff = DifflibParser(leftFileContents.splitlines(), rightFileContents.splitlines())

        # enable text area edits so we can clear and insert into them
        self.__main_window_ui.leftFileTextArea.config(state=NORMAL)
        self.__main_window_ui.rightFileTextArea.config(state=NORMAL)
        self.__main_window_ui.leftLinenumbers.config(state=NORMAL)
        self.__main_window_ui.rightLinenumbers.config(state=NORMAL)

        # clear all text areas
        self.__main_window_ui.leftFileTextArea.delete(1.0, END)
        self.__main_window_ui.rightFileTextArea.delete(1.0, END)
        self.__main_window_ui.leftLinenumbers.delete(1.0, END)
        self.__main_window_ui.rightLinenumbers.delete(1.0, END)

        leftlineno = rightlineno = 1
        for line in diff:
            if line['code'] == DiffCode.SIMILAR:
                self.__main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n')
                self.__main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n')
            elif line['code'] == DiffCode.RIGHTONLY:
                self.__main_window_ui.leftFileTextArea.insert('end', '\n', 'gray')
                self.__main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n', 'green')
            elif line['code'] == DiffCode.LEFTONLY:
                self.__main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n', 'red')
                self.__main_window_ui.rightFileTextArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffCode.CHANGED:
                for (i,c) in enumerate(line['line']):
                    self.__main_window_ui.leftFileTextArea.insert('end', c, 'darkred' if i in line['leftchanges'] else 'red')
                for (i,c) in enumerate(line['newline']):
                    self.__main_window_ui.rightFileTextArea.insert('end', c, 'darkgreen' if i in line['rightchanges'] else 'green')
                self.__main_window_ui.leftFileTextArea.insert('end', '\n')
                self.__main_window_ui.rightFileTextArea.insert('end', '\n')

            if line['code'] == DiffCode.LEFTONLY:
                self.__main_window_ui.leftLinenumbers.insert('end', str(leftlineno) + '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', '\n', 'line')
                leftlineno += 1
            elif line['code'] == DiffCode.RIGHTONLY:
                self.__main_window_ui.leftLinenumbers.insert('end', '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', str(rightlineno) + '\n', 'line')
                rightlineno += 1
            else:
                self.__main_window_ui.leftLinenumbers.insert('end', str(leftlineno) + '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', str(rightlineno) + '\n', 'line')
                leftlineno += 1
                rightlineno += 1

        # calc width of line numbers texts and set it
        self.__main_window_ui.leftLinenumbers.config(width=len(str(leftlineno)))
        self.__main_window_ui.rightLinenumbers.config(width=len(str(rightlineno)))

        # disable text areas to prevent further editing
        self.__main_window_ui.leftFileTextArea.config(state=DISABLED)
        self.__main_window_ui.rightFileTextArea.config(state=DISABLED)
        self.__main_window_ui.leftLinenumbers.config(state=DISABLED)
        self.__main_window_ui.rightLinenumbers.config(state=DISABLED)

    def __cut(self):
        area = self.__getActiveTextArea()
        if area:
            area.event_generate("<<Cut>>")

    def __copy(self):
        area = self.__getActiveTextArea()
        if area:
            area.event_generate("<<Copy>>")

    def __paste(self):
        area = self.__getActiveTextArea()
        if area:
            area.event_generate("<<Paste>>")

    def __getActiveTextArea(self):
        if self.main_window.focus_get() == self.__main_window_ui.leftFileTextArea:
            return self.__main_window_ui.leftFileTextArea
        elif self.main_window.focus_get() == self.__main_window_ui.rightFileTextArea:
            return self.__main_window_ui.rightFileTextArea
        else:
            return None

    def __goToLine(self):
        line = askstring('Go to line', 'Enter line number:')
        if line:
            try:
                linenumber = int(line)
                self.__main_window_ui.leftFileTextArea.see(float(linenumber) + 5)
            except:
                pass

    def __startFindText(self):
        self.__main_window_ui.searchTextDialog.grid()
        self.__main_window_ui.searchTextDialog.focus()

    def __endFindText(self):
        self.__main_window_ui.leftFileTextArea.tag_remove('search', 1.0, END)
        self.__main_window_ui.rightFileTextArea.tag_remove('search', 1.0, END)
        self.__main_window_ui.searchTextDialog.unfocus()
        self.__main_window_ui.searchTextDialog.grid_remove()

    def __findNext(self, searchresult):
        term, leftpos, rightpos = searchresult['term'], searchresult['indices'][0], searchresult['indices'][1]
        if leftpos != -1:
            self.__main_window_ui.leftFileTextArea.tag_remove('search', 1.0, END)
            self.__main_window_ui.leftFileTextArea.tag_add('search', leftpos, '%s + %sc' % (leftpos, len(term)))
            # scroll to position plus five lines for visibility
            self.__main_window_ui.leftFileTextArea.see(float(leftpos) + 5)
        if rightpos != -1:
            self.__main_window_ui.rightFileTextArea.tag_remove('search', 1.0, END)
            self.__main_window_ui.rightFileTextArea.tag_add('search', rightpos, '%s + %sc' % (rightpos, len(term)))
            # scroll to position plus five lines for visibility
            self.__main_window_ui.rightFileTextArea.see(float(rightpos) + 5)

    def __exit(self):
        self.main_window.destroy()

    def __helpInfo(self):
        # helpText = Text(self.main_window, height=50, width=100)
        # helpText.pack()
        # quote = QUOTE
        # helpText.insert(END, quote)
        # b1 = Button(helpText, text='cancel', command=self.__cancel_helptest(helpText))
        # helpText.window_create(INSERT, window=b1)

        mBox.showinfo("About",QUOTE)

    def __cancel_helptest(self,helpText):
        helpText.grid_remove()
        pass

    # 文件与文件路径比较
    def __browse_file_directories(self):

        BoolChooseLeft = self.__message_askbox('Info','Choose a basic file')
        if BoolChooseLeft:
            leftFile = self.__load_file('left')
        else:
            return
        BoolChooseRight = self.__message_askbox('Info', 'Choose a directory to compare')
        if BoolChooseRight:
            rightDir = self.__load_directory('right')
        else:
            return

        if rightDir:
            self.__main_window_ui.fileTreeView.grid()
            self.__main_window_ui.fileTreeYScrollbar.grid()
            self.__main_window_ui.fileTreeXScrollbar.grid()
            self.__main_window_ui.fileTreeView.delete(*self.__main_window_ui.fileTreeView.get_children())
            self.__browse_process_file_directory('', leftFile, rightDir)

    def __browse_process_file_directory(self, parent, leftPath, rightPath):
        if parent == '':
            leftPath = leftPath.rstrip('/')
            rightPath = rightPath.rstrip('/')
            # print leftPath,rightPath
            leftDirName = os.path.basename(leftPath)
            rightDirName = os.path.basename(rightPath)
            # print leftPath,rightPath
            self.__main_window_ui.fileTreeView.heading('#0', text=leftPath + ' / ' + rightDirName, anchor=W)
        # leftListing = os.listdir(leftPath)
        rightListing = os.listdir(rightPath)
        # mergedListing = list(set(leftListing) | set(rightListing))
        mergedListing = list(set(rightListing))
        for l in mergedListing:
            # newLeftPath = leftPath + '/' + l
            newLeftPath = leftPath
            newRightPath = rightPath + '/' + l
            bindValue = (newLeftPath, newRightPath)
            self.__main_window_ui.fileTreeView.insert(parent, 'end', text=l, value=bindValue, open=False,
                                                      tags=('green', 'simple'))

    def __message_askbox(self,level,msg):
        accept = msb.askokcancel(level, msg )
        return accept

    def __output_result_into_file(self):
        """
        文件与文件之间比较 ， 输出结果到文件
        :return:
        """
        if '.' in self.leftFile and '.' in self.rightFile:
            pass
        else:
            msb.showerror('Error', 'one or more file error!')
            return

        self.__output(self.leftFile,self.rightFile)

    # 将多文件对比结果输出到文件
    def __output_results_into_files(self):
        """
        文件与路径比较 ，输出结果到文件
        :return:
        """
        if self.leftFile == '' or self.rightFile == '':
            msb.showerror('Error','File is not exist')
            return

        leftPath = self.leftFile.rstrip('/')
        rightPath = self.rightFile.rstrip('/')

        if not os.path.exists('result'):
            os.mkdir('./result')
        if os.access('./result', os.F_OK):
            os.chdir('./result')

        isDir = False
        if '.' not in self.rightFile:
            isDir = True


        # 文件与文件比较
        if not isDir:
            self.__output_result_into_file()
        # 文件与文件夹比较
        else:

            rightListing = os.listdir(rightPath)

            mergedListing = list(set(rightListing))
            for l in mergedListing:
                newLeftPath = leftPath
                newRightPath = rightPath + '/' + l
                self.__output(newLeftPath, newRightPath)
        os.chdir('../')

        outputPath = os.getcwd().replace('\\','/') + '/result'
        msb.showinfo('Info', 'Result are output to dir:{filepath} '.format(filepath=outputPath))

    def __output(self,leftfile,rightfile):
        try:
            leftFileContents = open(leftfile).read()
        except:
            leftFileContents = ''
        try:
            rightFileContents = open(rightfile).read()
        except:
            rightFileContents = ''

        leftFileName = leftfile.split('/')[-1].split('.')
        rightFileName = rightfile.split('/')[-1].split('.')
        printLFile = 'diff_' + leftFileName[0] + '_' + rightFileName[0] + '.' + leftFileName[1]
        printRFile = 'diff_' + rightFileName[0] + '_' + leftFileName[0] + '.' + rightFileName[1]
        # print printLFile,printRFile
        fpl = open(printLFile, 'w+')
        fpr = open(printRFile, 'w+')

        diff = DifflibParser(leftFileContents.splitlines(), rightFileContents.splitlines())

        for line in diff:
            if line['code'] == DiffCode.RIGHTONLY:
                fpl.write('\n')
                fpr.write(line['line'] + '\n')
            elif line['code'] == DiffCode.LEFTONLY:
                fpl.write(line['line'] + '\n')
                fpr.write('\n')
            elif line['code'] == DiffCode.CHANGED:
                for (i, c) in enumerate(line['line']):
                    fpl.write(c)
                for (i, c) in enumerate(line['newline']):
                    fpr.write(c)
                fpl.write('\n')
                fpr.write('\n')
        fpl.close()
        fpr.close()
        return True

    def filesChangedByType(self,type):
        self.__main_window_ui.leftLinenumbers.grid_remove()
        self.__main_window_ui.rightLinenumbers.grid_remove()

        if not self.leftFile or not self.rightFile:
            self.__main_window_ui.leftFileTextArea.config(background=self.__main_window_ui.grayColor)
            self.__main_window_ui.rightFileTextArea.config(background=self.__main_window_ui.grayColor)
            return

        if os.path.exists(self.leftFile):
            self.__main_window_ui.leftFileLabel.config(text=self.leftFile)
            self.__main_window_ui.leftFileTextArea.config(background=self.__main_window_ui.whiteColor)
            self.__main_window_ui.leftLinenumbers.grid()
        else:
            self.__main_window_ui.leftFileLabel.config(text='')

        if os.path.exists(self.rightFile):
            self.__main_window_ui.rightFileLabel.config(text=self.rightFile)
            self.__main_window_ui.rightFileTextArea.config(background=self.__main_window_ui.whiteColor)
            self.__main_window_ui.rightLinenumbers.grid()
        else:
            self.__main_window_ui.rightFileLabel.config(text='')

        self.diff_files_into_text_areas_by_type(type)

    def diff_files_into_text_areas_by_type(self,type):
        try:
            leftFileContents = open(self.leftFile).read()
        except:
            leftFileContents = ''
        try:
            rightFileContents = open(self.rightFile).read()
        except:
            rightFileContents = ''

        diff = DifflibParser(leftFileContents.splitlines(), rightFileContents.splitlines())

        # enable text area edits so we can clear and insert into them
        self.__main_window_ui.leftFileTextArea.config(state=NORMAL)
        self.__main_window_ui.rightFileTextArea.config(state=NORMAL)
        self.__main_window_ui.leftLinenumbers.config(state=NORMAL)
        self.__main_window_ui.rightLinenumbers.config(state=NORMAL)

        # clear all text areas
        self.__main_window_ui.leftFileTextArea.delete(1.0, END)
        self.__main_window_ui.rightFileTextArea.delete(1.0, END)
        self.__main_window_ui.leftLinenumbers.delete(1.0, END)
        self.__main_window_ui.rightLinenumbers.delete(1.0, END)

        leftlineno = rightlineno = 1
        for line in diff:
            if line['code'] == DiffCode.SIMILAR and type:
                self.__main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n')
                self.__main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n')
            elif line['code'] == DiffCode.RIGHTONLY:
                self.__main_window_ui.leftFileTextArea.insert('end', '\n', 'gray')
                self.__main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n', 'green')
            elif line['code'] == DiffCode.LEFTONLY:
                self.__main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n', 'red')
                self.__main_window_ui.rightFileTextArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffCode.CHANGED:
                for (i,c) in enumerate(line['line']):
                    self.__main_window_ui.leftFileTextArea.insert('end', c, 'darkred' if i in line['leftchanges'] else 'red')
                for (i,c) in enumerate(line['newline']):
                    self.__main_window_ui.rightFileTextArea.insert('end', c, 'darkgreen' if i in line['rightchanges'] else 'green')
                self.__main_window_ui.leftFileTextArea.insert('end', '\n')
                self.__main_window_ui.rightFileTextArea.insert('end', '\n')

            if line['code'] == DiffCode.LEFTONLY:
                self.__main_window_ui.leftLinenumbers.insert('end', str(leftlineno) + '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', '\n', 'line')
                leftlineno += 1
            elif line['code'] == DiffCode.RIGHTONLY:
                self.__main_window_ui.leftLinenumbers.insert('end', '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', str(rightlineno) + '\n', 'line')
                rightlineno += 1
            else:
                self.__main_window_ui.leftLinenumbers.insert('end', str(leftlineno) + '\n', 'line')
                self.__main_window_ui.rightLinenumbers.insert('end', str(rightlineno) + '\n', 'line')
                leftlineno += 1
                rightlineno += 1

        # calc width of line numbers texts and set it
        self.__main_window_ui.leftLinenumbers.config(width=len(str(leftlineno)))
        self.__main_window_ui.rightLinenumbers.config(width=len(str(rightlineno)))

        # disable text areas to prevent further editing
        self.__main_window_ui.leftFileTextArea.config(state=DISABLED)
        self.__main_window_ui.rightFileTextArea.config(state=DISABLED)
        self.__main_window_ui.leftLinenumbers.config(state=DISABLED)
        self.__main_window_ui.rightLinenumbers.config(state=DISABLED)
