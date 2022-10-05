# coding=utf-8
# time: 2022/10/05 15:08:00
import re
import requests
from pathlib import Path
from time import time, perf_counter
from fake_useragent import UserAgent


def download_file_from_url(dl_url, file_name, headers):
    file_path = Path(__file__).parent.joinpath(file_name)
    if file_path.exists():
        dl_size = file_path.stat().st_size
    else:
        dl_size = 0
    headers['range'] = 'bytes={dl_size}-'.format(dl_size=dl_size)
    response = requests.get(dl_url, stream=True, headers=headers)
    print("download info")
    total_size = int(response.headers['content-length'])
    print("file name: {}, dlsize: {}, totalsize:{}".format(file_name, dl_size, total_size))
    start = perf_counter()

    data_count = 0
    count_temp = 0
    start_time = time()

    with open(file_path, 'ab') as fp:
        for chunk in response.iter_countent(chunk_size=512):
            data_count += len(chunk)
            now_pross = (data_count/total_size) * 100
            mid_time = time()
            if mid_time - start_time > 0.1:
                speed = (data_count - count_temp) / 1024 / (mid_time - start_time)
                start_time = mid_time
                count_temp = data_count
                print("down load : {} {}/{} speed:{}".format(now_pross, data_count, total_size, speed))
            fp.write(chunk)
    end = perf_counter()
    diff = end - start
    speed = total_size/1024/diff
    print("used time: {} {}".format(diff, speed))


if __name__ == '__main__':
    url = 'https://v3.douyinvod.com/'
    filename = "xx.mp4"
    headers = {
        'User-Agent': ''
    }
    download_file_from_url(url, filename, headers)

