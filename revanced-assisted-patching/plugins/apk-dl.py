import urllib.request as urllib2
from bs4 import BeautifulSoup
#import re


def get_apk_url(package_name):
    opener = urllib2.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
        )
    ]
    urllib2.install_opener(opener)

    response = opener.open("http://apk-dl.com/" + package_name)
    soup = BeautifulSoup(response.read(), "html.parser")
    temp_link = soup.find("div", {"class": "download-btn"}).find("a")["href"]
    print(temp_link)

    response = opener.open("http://apk-dl.com/" + temp_link)
    soup = BeautifulSoup(response.read(), "html.parser")
    temp_link2 = soup.find("section", {"class": "detail"}).find("a")["href"]
    print(temp_link2)

    response = opener.open(temp_link2)
    soup = BeautifulSoup(response.read(), "html.parser")
    temp_link3 = soup.find("div", {"class": "contents"}).find("a")["href"]
    print(temp_link3)

    return "http:" + temp_link3


print(get_apk_url("com.facebook.katana"))
