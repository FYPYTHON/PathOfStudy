# coding=utf-8
from tkinter import Tk, scrolledtext
import tkinter.font as TkFont
from tkinter import ttk
from tkinter import Frame
from tkinter import END, DISABLED, NORMAL
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory    # 文件、路径对话框
from datetime import datetime
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COLOR_RED = 'red'
COLOR_GREEN = 'green'
COLOR_BLUE = 'blue'
COLOR_48D1CC = '#48D1CC'
COLOR_ADD8E6 = '#ADD8E6'
FIRST_ROW = 1
SECOND_ROW = 2
CONSUMER_ROW = 3
TOPICS_ROW = 3
TIME_RANGE_ROW = 4
OFFSET_GET_ROW = 5
CONTENT_ROW = 6


def setup_err_msg(self, msg):
    self.err_var = tk.StringVar()
    self.err_var.set(msg)
    self.error_msg = tk.Label(self.ui, fg='red', textvariable=self.err_var)
    self.error_msg.grid(row=CONTENT_ROW + 1, column=1, rowspan=1, columnspan=6)
    # self.error_msg = tk.Label(self.ui, text=u"{}".format(msg), fg='red', textvariable=)
    # self.error_msg.grid(row=CONTENT_ROW + 1, column=2, rowspan=1)
    self.error_msg.place(x=50, y=610)


def setup_admin(self):
    # button data
    newt_label = tk.Label(self.admin_ui, text=u'New Topic：', bg=COLOR_ADD8E6)
    newt_label.grid(row=1, column=1)
    newt_var = tk.StringVar()
    self.newt_input = tk.Entry(self.admin_ui, textvariable=newt_var)
    newt_var.set("")
    self.newt_input.grid(row=1, column=2, padx=10, pady=5)

    # new partition
    newp_label = tk.Label(self.admin_ui, text=u'New Partiion：', bg=COLOR_ADD8E6)
    newp_label.grid(row=1, column=3)
    newp_var = tk.StringVar()
    self.newp_input = tk.Entry(self.admin_ui, textvariable=newp_var)
    newp_var.set("")
    self.newp_input.grid(row=1, column=4, pady=5)

    btn_admin = tk.Button(self.admin_ui, text=u'添加', width=10, command=self.create_topics)
    btn_admin.grid(row=1, column=5)
    pass

    # partition manage
    # new
    self.comvaluep = tk.StringVar()  # 窗体自带的文本，新建一个值
    # comvalue.set('meetingData')
    self.combox_topic_listp = ttk.Combobox(self.admin_ui, textvariable=self.comvaluep, height=13, width=30)  # 初始化
    self.combox_topic_listp["values"] = self.all_topic
    self.combox_topic_listp['state'] = 'readonly'
    self.combox_topic_listp['text'] = 'topic'
    self.combox_topic_listp.current(0)  # 选择第一个
    self.combox_topic_listp.bind("<<ComboboxSelected>>", self.region_set_inner)  # 绑定事件,(下拉列表框被选中时，绑定函数)
    self.combox_topic_listp.grid(row=SECOND_ROW, column=1, padx=8, pady=7, columnspan=2)
    self.combox_topic_listp.set(self.cur_topic)

    newpn_label = tk.Label(self.admin_ui, text=u'Partiion Num：', bg=COLOR_ADD8E6)
    newpn_label.grid(row=2, column=3)
    newpn_var = tk.StringVar()
    self.newpn_input = tk.Entry(self.admin_ui, textvariable=newpn_var)
    newpn_var.set("")
    self.newpn_input.grid(row=2, column=4, pady=4)

    btn_partition = tk.Button(self.admin_ui, text=u'修改', width=10, command=self.create_partiton)
    btn_partition.grid(row=2, column=5)

    btn_return = tk.Button(self.admin_ui, text=u'返回', width=10, command=self.return_main)
    btn_return.grid(row=3, column=5)
    # print(btn_return.size())
    btn_return.place(x=600 - btn_return.size()[0] - 100, y=400 - btn_return.size()[1] - 50)


def setup_label(self):
    ip_label = tk.Label(self.ui, text=u'服务器IP：', bg=COLOR_ADD8E6)
    ip_label.grid(row=FIRST_ROW, column=1)

    service_var = tk.StringVar()
    service_var.set(self.def_ip)
    self.service_input = tk.Entry(self.ui, textvariable=service_var)
    self.service_input.grid(row=FIRST_ROW, column=2, padx=10, pady=5)

    port_label = tk.Label(self.ui, text=u'端口号：', bg=COLOR_ADD8E6)
    port_label.grid(row=FIRST_ROW, column=3)

    port_var = tk.StringVar()
    self.port_input = tk.Entry(self.ui, textvariable=port_var)
    port_var.set(self.def_port)
    self.port_input.grid(row=FIRST_ROW, column=4, padx=10, pady=5)

    btn_conn = tk.Button(self.ui, text=u'连接', width=10, command=self.get_connect)
    btn_conn.grid(row=FIRST_ROW, column=5)

    btn_admin = tk.Button(self.ui, text=u'管理', width=10, command=self.get_admin)
    btn_admin.grid(row=FIRST_ROW, column=6)


def set_topics(self, topics, consumers):
    if len(topics) == 0:
        return None
    region_label = tk.Label(self.ui, text=u'选择topic：', bg=COLOR_ADD8E6)
    region_label.grid(row=SECOND_ROW, column=1)

    self.comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
    # comvalue.set('meetingData')
    self.combox_topic_list = ttk.Combobox(self.ui, textvariable=self.comvalue, height=13, width=30)  # 初始化
    self.combox_topic_list["values"] = topics
    self.combox_topic_list['state'] = 'readonly'
    self.combox_topic_list['text'] = 'topic'
    self.combox_topic_list.current(0)  # 选择第一个
    self.combox_topic_list.bind("<<ComboboxSelected>>", self.region_set_inner)  # 绑定事件,(下拉列表框被选中时，绑定函数)
    self.combox_topic_list.grid(row=SECOND_ROW, column=2, padx=8, pady=7, columnspan=2)
    self.combox_topic_list.set(self.cur_topic)

    btn_offset = tk.Button(self.ui, text=u'获取最新offset', width=20, command=self.get_offset)
    btn_offset.grid(row=SECOND_ROW, column=4)

    btn_alloffset = tk.Button(self.ui, text=u'获取所有offset', width=20, command=self.get_alloffset)
    btn_alloffset.grid(row=SECOND_ROW, column=6)

    # --- consumer list ---
    if len(consumers) == 0:
        consumers = ["NoConsumer"]
    region_label = tk.Label(self.ui, text=u'选择consumer：', bg=COLOR_ADD8E6)
    region_label.grid(row=CONSUMER_ROW, column=1)

    self.comsumervalue = tk.StringVar()  # 窗体自带的文本，新建一个值
    self.combox_consumer_list = ttk.Combobox(self.ui, textvariable=self.comsumervalue, height=13, width=30
                                             , justify='left')  # 初始化
    # self.combox_consumer_list['choices'] = consumers
    self.combox_consumer_list["values"] = consumers
    self.combox_consumer_list['state'] = 'readonly'
    self.combox_consumer_list['text'] = 'consumer'
    self.combox_consumer_list.current(0)  # 选择第一个
    self.combox_consumer_list.bind("<<ComboboxSelected>>", self.consumer_set_inner)  # 绑定事件,(下拉列表框被选中时，绑定函数)
    # self.combox_consumer_list.bind_all()
    self.combox_consumer_list.grid(row=CONSUMER_ROW, column=2, padx=8, pady=7, columnspan=2)
    self.combox_consumer_list.set(self.cur_consumer)

    btn_consumer = tk.Button(self.ui, text=u'获取最新consumer', width=20, command=self.get_consumer)
    btn_consumer.grid(row=CONSUMER_ROW, column=4)

    # btn_allconsumer = tk.Button(self.ui, text=u'获取所有consumer', width=20, command=self.get_allconsumer)
    # btn_allconsumer.grid(row=CONSUMER_ROW, column=6)

    # offset and time range
    begin_label = tk.Label(self.ui, text=u'开始时间：', bg=COLOR_ADD8E6)
    begin_label.grid(row=TIME_RANGE_ROW, column=2)

    begin_var = tk.StringVar()
    begin_var.set(datetime.now().strftime(TIME_FORMAT))
    self.begin_input = tk.Entry(self.ui, textvariable=begin_var)
    self.begin_input.grid(row=TIME_RANGE_ROW, column=3, padx=10, pady=5)

    end_label = tk.Label(self.ui, text=u'结束时间：', bg=COLOR_ADD8E6)
    end_label.grid(row=TIME_RANGE_ROW, column=4)

    end_var = tk.StringVar()
    self.end_input = tk.Entry(self.ui, textvariable=end_var)
    end_var.set(datetime.now().strftime(TIME_FORMAT))
    self.end_input.grid(row=TIME_RANGE_ROW, column=5, padx=10, pady=5)

    # button data
    filter_label = tk.Label(self.ui, text=u'过滤条件：', bg=COLOR_ADD8E6)
    filter_label.grid(row=OFFSET_GET_ROW, column=2)

    filter_var = tk.StringVar()
    self.filter_input = tk.Entry(self.ui, textvariable=filter_var)
    filter_var.set("CS: setup")
    self.filter_input.grid(row=OFFSET_GET_ROW, column=3, padx=10, pady=5)

    btn_data = tk.Button(self.ui, text=u'获取指定数据', width=20, command=self.get_range_data)
    btn_data.grid(row=OFFSET_GET_ROW, column=4)


def set_content(self):
    region_label = tk.Label(self.ui, text=u'最新offset：', bg=COLOR_ADD8E6)
    region_label.grid(row=CONTENT_ROW, column=1)
    self.content_text = tk.Text(self.ui, width=100,
                                # font=("Times", 11),
                                )
    self.content_text.grid(row=CONTENT_ROW, column=2, rowspan=2, columnspan=6)


def set_status_content(self):
    self.status = tk.StringVar()
    self.status.set('当前无连接')
    self.lblStatus = tk.Label(self.ui, textvariable=self.status, anchor='c',
                              # bg='blue',
                              font=("微软雅黑", 8),
                              fg='blue',
                              width=100,
                              )

    self.lblStatus.grid(row=CONTENT_ROW + 2, column=0, columnspan=6
                        # , sticky=tk.S + tk.E
                        )
    # 880x600+100+100
    # self.lblStatus.grid(columnspan=6)
    # self.lblStatus.place(x=150, y=550, width=100, height=25)
    self.lblStatus.place(x=0, y=630)



# 58.240.217.252 - 39 ?
# 58.211.249.171 - ?