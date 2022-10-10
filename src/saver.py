import os
import urllib.parse


class FileSaver:
    """Сохраняет основную информацию страницы в файл"""

    def __init__(self, main_info: str, url: str, line_width: int = 80):
        self.main_info = main_info
        self.url = url
        self.line_width = line_width

    def save_to_file(self):
        """Сохраняет текст в файл, директории и название файла формируются из URL"""
        # Формируем путь для сохранения
        parsed_url = urllib.parse.urlparse(self.url)
        host_name = parsed_url.netloc

        path = parsed_url.path
        path = path.rstrip("/")
        dot = path.rfind(".")
        if dot != -1:
            path = path[:dot]
        path += ".txt"

        # Создаем папки по пути
        file_name = os.path.join(os.curdir, host_name + path)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Записываем в файл
        with open(file_name, "w", encoding="utf-8") as file:
            for paragraph in self.main_info.split("\n"):
                # Если параграф представляет собой пробелы, игнорируем
                if paragraph == "" or paragraph.isspace():
                    continue

                # Убрать неразрывные пробелы
                paragraph = paragraph.replace(chr(0x00A0), " ")

                # Разбиваем на строки указанной ширины
                lines = self.__split_text_to_lines(paragraph, self.line_width)
                for line in lines:
                    file.write(line + "\n")
                file.write("\n")

    @staticmethod
    def __split_text_to_lines(text: str, line_width: int) -> list:
        """Разделяет текст на строки длиной не более line_width, перенос по словам"""
        result = []
        while len(text) > line_width:
            if " " not in text:
                break

            right_space = text.rfind(" ", 0, line_width)
            # Если слово больше длины строки, выводим его на одной строке
            if right_space == -1:
                right_space = text.find(" ")

            result.append(text[:right_space])
            text = text[right_space + 1:]

        result.append(text)
        return result
