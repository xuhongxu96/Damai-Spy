import requests
from bs4 import BeautifulSoup

URL = "https://www.damai.cn/projectlist.do?cityID=%s&mcid=%s&isText=1"


def fetch_list(soup, f, type):
    li_list = soup.find(id="performList").find_all("li")
    for li in li_list:
        a = li.find("a")
        f.write(type + ",")  # 类型
        f.write(li.find(attrs={"class": "ml20"}).find("a").text.strip().replace(",", ";") + ",")  # 场馆
        f.write(a.text.strip().replace(",", ";") + ",")  # 名称
        f.write(a["href"].strip().replace(",", ";") + ",")  # 连接
        price = li.find(attrs={"class": "price-sort"}).text.strip().split("-")  # 价格区间
        if len(price) > 1:
            f.write(price[0] + "," + price[1] + "\n")
        else:
            f.write(price[0] + "," + price[0] + "\n")


def fetch_page_count(soup):
    p = soup.find(attrs={"class": "pagination"})
    if p is None:
        return 1
    p = p.find(attrs={"class": "ml10"}).text.strip()
    p = p[1:-1]
    return int(p)


def fetch_city(city, city_id, type, type_id):
    with open("res/" + city + ".txt", "a", encoding="utf-8") as f:
        r = requests.get(URL % (city_id, type_id))
        soup = BeautifulSoup(r.text, "html.parser")
        fetch_list(soup, f, type)
        print(city, type, "page", 1)
        page_count = fetch_page_count(soup)
        for i in range(2, page_count + 1):
            print(city, type, "page", i, "/", page_count)
            r = requests.get((URL % (city_id, type_id)) + "&pageIndex=" + str(i))
            soup = BeautifulSoup(r.text, "html.parser")
            fetch_list(soup, f, type)
