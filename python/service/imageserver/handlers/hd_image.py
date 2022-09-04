# coding=utf-8
import tornado.web
import json
import base64
from io import BytesIO
from tornado.log import app_log as imagelog
import matplotlib.pyplot as plt


class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        xdata = self.get_arguments("xdata")
        ydata = self.get_arguments("ydata")
        sma1 = self.get_arguments("sma1")
        sma2 = self.get_arguments("sma2")
        pos = self.get_arguments("pos")
        kind = self.get_argument("kind", "")

        imagelog.info("len(xdata)={}".format(len(xdata)))
        imagelog.info("len(xdata)={}".format(len(ydata)))
        imagelog.info("mutli={} type={}".format(len(pos) > 1, len(pos)))
        mutli = False
        if len(pos) > 1:
              mutli = True
        if len(xdata) != len(ydata) and not mutli:
            return self.write(json.dumps({"err_code": 1, "msg": "x y length not the same"}))
        # print(f"{xdata} {ydata}")
        # print(xdata)
        # print(ydata)
        ydata = [float(i) for i in ydata]
        if mutli:
            imagelog.info("mutli data len(pos)={}".format(len(pos)))
            sma1 = [float(i) for i in sma1]
            sma2 = [float(i) for i in sma2]
            pos = [int(i) for i in pos]
            sma_data = [ydata, sma1, sma2]
            # plt.plot(xdata, *sma_data, marker='o')
            # plt.plot(xdata, *sma_data, color=["blue", "green", "orange"])
            plt.plot(xdata, ydata, color='blue')
            plt.plot(xdata, sma1, color='green')
            plt.plot(xdata, sma2, color='orange')
            plt.legend(["ori", "sma1", "sma2"])
            ax2 = plt.twinx()
            ax2.set_ylim([-1-0.1, 1+0.1])
            ax2.plot(xdata, pos, color='red')
            # https://blog.csdn.net/u010440456/article/details/90768681
            ax2.legend(['pos'], loc="upper center")  # upper right
        else:
            imagelog.info("single data len(ydata)={}".format(len(ydata)))
            if kind == "bar":
                plt.bar(xdata, ydata)
            else:
                plt.plot(xdata, ydata, marker='o')
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei Mono']
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.xticks(rotation=75, fontsize=12)
        if len(xdata) < 5:
            plt.xlim(0, 5)
        figfile = BytesIO()
        # filename = "xy_{}.png".format(self.request.request_time())
        # print(filename)
        plt.savefig(figfile, dpi=600, format="png")
        figdata_png = base64.b64encode(figfile.getvalue()).decode()
        # figfile.close()
        plt.cla()
        plt.close()
        # print(len(figdata_png))
        imagelog.info("{} {} \nimgb64 len:{}".format("xdata", "ydata", len(figdata_png)))
        return self.write(json.dumps({"err_code": 0, "img": figdata_png}))

