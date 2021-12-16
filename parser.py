import urllib.request
import urllib.parse
import os
from bs4 import BeautifulSoup
import settings
from utils import split_text_to_lines, replace_a_with_href


class MainInfoParser:
    def __init__(self, url: str):
        self.url = url
        self._get_page()
        self._remove_tags()
        self._replace_links()
        self._get_main_info()

    def _get_page(self):
        """Получает страницу по url и парсит с помощью BeautifulSoup"""
        req = urllib.request.urlopen(self.url)
        html = req.read()
        self.soup = BeautifulSoup(html, "html.parser")

    def _remove_tags(self):
        """Удаляет заданные в settings теги"""
        for tag in self.soup.find_all(settings.TAGS_TO_REMOVE):
            tag.decompose()

    def _replace_links(self):
        """Заменяет теги <a> на ссылки в квадратных скобках"""
        parsed_url = urllib.parse.urlparse(self.url)
        host_name = parsed_url.netloc
        scheme = parsed_url.scheme
        for tag in self.soup.find_all("a"):
            replace_a_with_href(tag, host_name, scheme)

    def _get_main_info(self):
        """Берет со страницы заданные в settings теги"""
        self.info_tags = self.soup.find_all(settings.TAGS_TO_SEARCH)

    def save_to_file(self):
        """Сохраняет текст в файл, директории и название файла формируются из URL"""
        parsed_url = urllib.parse.urlparse(self.url)
        host_name = parsed_url.netloc

        path = parsed_url.path
        path = path.rstrip("/")
        dot = path.rfind(".")
        if dot != -1:
            path = path[:dot]
        path += ".txt"

        file_name = os.path.join(os.curdir, host_name + path)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as file:
            for tag in self.info_tags:
                text = tag.get_text()
                if text == "" or text.isspace():
                    continue
                # Убрать неразрывные пробелы
                text = text.replace(chr(0x00A0), " ")
                # Убрать символы новой строки
                text = text.replace("\n", " ")
                lines = split_text_to_lines(text, settings.LINE_WIDTH)
                for line in lines:
                    file.write(line + "\n")
                file.write("\n")
