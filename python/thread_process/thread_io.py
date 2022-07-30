# coding=utf-8
from threading import Thread
from multiprocessing import Process
import requests
from bs4 import BeautifulSoup
import time, os


def get_urls(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res, features="html.parser")
    # 通过css selector解析页面，获取元素
    artile_urls = soup.select(".atc_title > a")
    url_list = list(i.get("href") for i in artile_urls)
    return (url_list)


def get_content(urls, dirpath):
    '''
    获取文章内容
    :param urls: 要获取文章的url列表
    :param dirpath: 文章内容文件保存路径
    :return:
    '''

    for url in urls:
        # print("要抓取的url是%s" % url)
        res = requests.get(url).content.decode("utf-8")

        soup = BeautifulSoup(res, features="html.parser")
        paragraphs = soup.select("#sina_keyword_ad_area2 > p")
        content = ""
        for i in paragraphs:
            content += i.get_text()
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        open(dirpath + r'/' + url[-26:], 'w').write(content)


def thread_process_job(n, Thread_or_Process, url_list, job):
    """
    n: numbers
    Thread_Process: Thread／Process class
    url_list: args list
    job: task
    """
    local_time = time.time()

    threads_or_processes = [Thread_or_Process(target=job, args=(url_list[j], str(n)+Thread_or_Process.__name__)) for j in range(n)]
    for t in threads_or_processes:
        t.start()
    for t in threads_or_processes:
        t.join()
    print(n, Thread_or_Process.__name__, " run job need ", time.time() - local_time)


if __name__=="__main__":
    t = time.time()

    urls = []
    for i in range(7):
        url='http://blog.sina.com.cn/s/articlelist_1191258123_0_' + str(i + 1) + '.html'
        page_urls=get_urls(url)
        urls.extend(page_urls)
    url_len = len(urls)
    print("total urls number is ", url_len)

    for n in [8, 4, 2, 1]:
        # 将urls分割到url_list
        url_list = []
        url_split_len = url_len // n
        for i in range(n):
            if i == n - 1:
                url_list.append(urls[i * url_split_len:url_len])
            else:
                url_list.append(urls[i * url_split_len:(i + 1) * url_split_len])
        # 分割任务后创建线程
        print("\t", "thread ", n)
        ts = time.clock()
        thread_process_job(n, Thread, url_list, get_content)
        print("\t", time.clock() - ts)
        print("\t", "process ", n)
        tp = time.clock()
        thread_process_job(n, Process, url_list, get_content)
        print("\t", time.clock() - tp)

    print("All done in ", time.time() - t)