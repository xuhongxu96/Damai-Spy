import re


def spy_city(soup):
    cities = soup.find(id="city").find(attrs={"class": "in"}).find_all("a")
    idRegex = re.compile(r"cityID\=(\d+)&")
    with open("res/city_id.txt", "w", encoding="utf-8") as f:
        print(len(cities))
        f.write(str(len(cities)) + "\n")
        for city in cities:
            href = city["href"]
            print(city.text + "," + idRegex.search(href).group(1))
            f.write(city.text + "," + idRegex.search(href).group(1) + "\n")
