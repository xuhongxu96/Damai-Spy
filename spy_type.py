import re


def spy_type(soup):
    types = soup.find(id="maincategory").find(attrs={"class": "in"}).find_all("a")
    idRegex = re.compile(r"mcid\=(\d+)&")
    with open("res/type_id.txt", "w", encoding="utf-8") as f:
        print(len(types))
        f.write(str(len(types)) + "\n")
        for type in types:
            href = type["href"]
            print(type.text + "," + idRegex.search(href).group(1))
            f.write(type.text + "," + idRegex.search(href).group(1) + "\n")
