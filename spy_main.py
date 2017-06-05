import os

import requests
from bs4 import BeautifulSoup
import threading
import spy_type
import spy_city
import spy_list

URL = "https://www.damai.cn/projectlist.do?isText=1"

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")
spy_type.spy_type(soup)
spy_city.spy_city(soup)

cities = []
types = []

with open("res/city_id.txt", "r", encoding="utf-8") as f:
    ct = f.readline()
    for i in range(0, int(ct)):
        l = f.readline()[:-1]
        cities.append(l.split(","))

with open("res/type_id.txt", "r", encoding="utf-8") as f:
    ct = f.readline()
    for i in range(0, int(ct)):
        l = f.readline()[:-1]
        types.append(l.split(","))

threads = []
for city, city_id in cities:
    if os.path.exists("res/" + city + ".txt"): os.remove("res/" + city + ".txt")
    for show_type, type_id in types:
        if show_type in ["超级票", "优惠券", "票票堂", "电影优惠券", "周边商品", "旅游演艺"]: continue
        t = threading.Thread(target=spy_list.fetch_city, args=(city, city_id, show_type, type_id))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
