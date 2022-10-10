import urllib.request

from parser import MainInfoParser


main_info_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]


def get_page(url):
    """Получает страницу по url и парсит"""
    req = urllib.request.urlopen(url)
    html_code = str(req.read(), encoding="utf-8")

    parser = MainInfoParser(main_info_tags, url)
    parser.feed(html_code)
    print(parser.main_info)


get_page("https://habr.com/ru/post/692302/")
