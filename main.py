import sys
from urllib.error import HTTPError, URLError
from parser import MainInfoParser

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print("Ошибка: не введен URL")
    quit()

try:
    parser = MainInfoParser(url)
except HTTPError as e:
    print(f"Ошибка: {e.code} {e.reason}")
except URLError as e:
    print("Ошибка: неверный URL")
else:
    parser.save_to_file()
