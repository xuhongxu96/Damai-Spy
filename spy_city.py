import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.damai.cn/projectlist.do?mcid=1&isText=1"

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

cities = soup.find(id="city").find(attrs={"class": "in"}).find_all("a")
idRegex = re.compile(r"cityID\=(\d+)&")
print(len(cities))
for city in cities:
    href = city["href"]
    print(city.text + "," + idRegex.search(href).group(1))
