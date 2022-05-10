import os
import time
import json
from tornado.escape import url_unescape
from multiprocessing import Process
import pickle

from selenium import webdriver

def progress(date):
    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--disk-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    driver = webdriver.PhantomJS("E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe", service_args=service_args)
    file = "E:\\mahjong data\\scraw2017\\2017\\scc"+date+".html"
    file_save = "E:\\mahjong data\\data\\2017\\"+date+"\\"
    tot = 0
    f_tmp = open(file , 'r', encoding='utf-8')
    if not os.path.exists(file_save):
        os.mkdir(file_save)
    lines = f_tmp.readlines()
    for line in lines:
        tic1 = time.perf_counter()
        tmpinfo = line.split('|')
        comkind = tmpinfo[2]
        if comkind.find("四") == -1 or comkind.find("南") == -1:
            continue
        tmp_href = tmpinfo[3].split("\"")
        href = tmp_href[1]
        href = href.replace('0', '6', 1)
        link = href
        link = link.lstrip("https://tenhou.net/6/?log=")
        cnt = 0
        if os.path.exists(file_save + link):
            continue
        f_save = open(file_save + link, 'w', encoding="utf-8")
        while True:
            url = href + "&ts=" + str(cnt)
            driver.get(url)
            while driver.current_url == url:
                time.sleep(0.1)
            tmp1, tmp2 = driver.current_url.split("json=")
            json_data, tmp3 = tmp2.split("&")
            json_data = url_unescape(json_data)
            json_tmp = json.loads(json_data)
            if json_tmp['log'][0][16][0] == '不明':
                break
            f_save.write(json.dumps(json_tmp, ensure_ascii=False))
            f_save.write('\n')
            cnt += 1
        tic2 = time.perf_counter()
        tot += 1
        print(line, "done,using:", (tic2 - tic1), "s,tot:", tot)

def main():
    process_list=[]
    p1 = Process(target=progress, args=("20170103",))
    p1.start()
    process_list.append(p1)
    p2 = Process(target=progress, args=("20170104",))
    p2.start()
    process_list.append(p2)
    p3 = Process(target=progress, args=("20170105",))
    p3.start()
    process_list.append(p3)
    p4 = Process(target=progress, args=("20170106",))
    p4.start()
    process_list.append(p4)
    p5 = Process(target=progress, args=("20170107",))
    p5.start()
    process_list.append(p5)
    p6 = Process(target=progress, args=("20170108",))
    p6.start()
    process_list.append(p6)
    p7 = Process(target=progress, args=("20170109",))
    p7.start()
    process_list.append(p7)
    p8 = Process(target=progress, args=("20170110",))
    p8.start()
    process_list.append(p8)
    for t in process_list:
        t.join()

if __name__=='__main__':
    main()