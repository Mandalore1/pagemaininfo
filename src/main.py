import sys
import urllib.request

from parser import MainInfoParser
from saver import FileSaver
import settings


def get_page(url: str) -> str:
    """Получает страницу по url"""
    req = urllib.request.urlopen(url)
    return str(req.read(), encoding="utf-8")


def main():
    url = ""
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Ошибка: не введен URL")
        quit()

    try:
        html_code = get_page(url)

        parser = MainInfoParser(settings.TAGS_TO_SEARCH, url)
        parser.feed(html_code)

        saver = FileSaver(parser.main_info, url, settings.LINE_WIDTH)
        saver.save_to_file()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
