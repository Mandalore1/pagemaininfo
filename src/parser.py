import html.parser
import urllib.parse


class MainInfoParser(html.parser.HTMLParser):
    """Парсер, забирающий основные данные со страницы"""

    def __init__(self, main_info_tags: list, url: str):
        super().__init__()

        self.main_info_tags = main_info_tags
        self.url = url

        self.__current_tags = []  # Стек тегов
        self.main_info = ""

    def handle_starttag(self, tag, attrs):
        """Кладем в стек тегов теги, указанные в main_info_tags"""
        if tag == "a" and self.__current_tags:
            # Если встретили тег <a> и находимся внутри нужного тега, добавляем ссылку в результат
            href = ""
            for attr, value in attrs:
                if attr == "href":
                    href = value
                    break
            self.main_info += self.__replace_href(href)

        elif tag in self.main_info_tags:
            self.__current_tags.append(tag)

    def handle_endtag(self, tag):
        """При закрытии тега, указанного в main_info_tags, убираем его из стека"""
        if tag in self.main_info_tags:
            # Если не соблюден баланс тегов, выбрасываем исключение
            if self.__current_tags[-1] != tag:
                raise ValueError("HTML-страница невалидна!")

            self.__current_tags.pop()
            self.main_info += "\n"

    def handle_data(self, data):
        """Если мы сейчас находимся внутри тега, указанного в main_info_tags, добавляем данные в результат"""
        if self.__current_tags:
            self.main_info += data

    def __replace_href(self, href):
        """Заменяет href из тега <a> на ссылку в квадратных скобках"""
        parsed_url = urllib.parse.urlparse(self.url)
        host_name = parsed_url.netloc
        scheme = parsed_url.scheme
        return "[" + urllib.parse.urljoin(f"{scheme}://{host_name}", href) + "]"
