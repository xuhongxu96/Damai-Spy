import requests
from bs4 import BeautifulSoup
import threading

URL = "https://www.damai.cn/projectlist.do?cityID=%s&isText=1"
cities = []

def fetchList(soup, f):
    li_list = soup.find(id="performList").find_all("li")
    for li in li_list:
        a = li.find("a")
        f.write(a.text.strip().replace(",", ";") + ",")
        f.write(a["href"].strip().replace(",", ";") + ",")
        price = li.find(attrs={"class": "price-sort"}).text.strip().split("-")
        if len(price) > 1:
            f.write(price[0] + "," + price[1] + "\n")
        else:
            f.write(price[0] + "," + price[0] + "\n")

def fetchPageCount(soup):
    p = soup.find(attrs={"class": "pagination"})
    if p is None:
        return 1
    p = p.find(attrs={"class": "ml10"}).text.strip()
    p = p[1:-1]
    return int(p)

def fetchCity(city, id):
    with open(city + ".txt", "w") as f:
        r = requests.get(URL % id)
        soup = BeautifulSoup(r.text, "html.parser")
        fetchList(soup, f)
        page_count = fetchPageCount(soup)
        for i in range(2, page_count + 1):
            print(city, "page", i)
            r = requests.get((URL % id) + "&pageIndex=" + str(i))
            soup = BeautifulSoup(r.text, "html.parser")
            fetchList(soup, f)


with open("city_id.txt", "r") as f:
    ct = f.readline()
    for i in range(0, int(ct)):
        l = f.readline()[:-1]
        cities.append(l.split(","))

threads = []

for city, id in cities:
    t = threading.Thread(target=fetchCity, args = (city, id))
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()
