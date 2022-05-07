import os
import time
import json
from tornado.escape import url_unescape
import pickle

from selenium import webdriver

service_args=[]
service_args.append('--load-images=no')
service_args.append('--disk-cache=yes')
service_args.append('--ignore-ssl-errors=true')
driver = webdriver.PhantomJS("E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",service_args=service_args)
file = "E:\\mahjong data\\scraw2017\\2017\\"
file_save = "E:\\mahjong data\\data\\2017\\"
tot = 0
for root, dirs, files in os.walk(file):
    for f in files:
        f_tmp = open(file + f, 'r', encoding='utf-8')
        get_date = f
        get_date = get_date.lstrip("scc")
        get_date = get_date.rstrip(".html")
        if not os.path.exists(file_save + get_date):
            os.mkdir(file_save + get_date)
        lines = f_tmp.readlines()
        for line in lines:
            tic1=time.perf_counter()
            tmpinfo = line.split('|')
            comkind = tmpinfo[2]
            if comkind.find("四") == -1 or comkind.find("南") == -1:
                continue
            tmp_href = tmpinfo[3].split("\"")
            href = tmp_href[1]
            href = href.replace('0','6', 1)
            link = href
            link = link.lstrip("https://tenhou.net/6/?log=")
            cnt = 0
            f_save = open(file_save + get_date+"\\"+link, 'w', encoding="utf-8")
            while True:
                url = href+"&ts="+str(cnt)
                driver.get(url)
                while driver.current_url == url:
                    time.sleep(0.1)
                tmp1, tmp2 = driver.current_url.split("json=")
                json_data, tmp3 = tmp2.split("&")
                json_data = url_unescape(json_data)
                json_tmp = json.loads(json_data)
                if json_tmp['log'][0][16][0] == '不明':
                    break
                f_save.write(json.dumps(json_tmp,ensure_ascii=False))
                f_save.write('\n')
                cnt += 1
            tic2=time.perf_counter()
            tot+=1
            print(line,"done,using:",(tic2-tic1),"s,tot:",tot)

