import sys
import urllib.request

from parser import MainInfoParser
from src.saver import FileSaver

main_info_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]


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

        parser = MainInfoParser(main_info_tags, url)
        parser.feed(html_code)

        saver = FileSaver(parser.main_info, url, 80)
        saver.save_to_file()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
