import urllib.parse


def split_text_to_lines(text: str, line_width: int):
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


def replace_a_with_href(tag, host_name: str, scheme: str):
    """
    Заменяет теги <a> на строку вида 'текст_тега [адрес ссылки тега]'
    Относительные ссылки преобразуются в абсолютные
    """
    try:
        href = tag["href"]
    except KeyError:
        return

    href = urllib.parse.urljoin(f"{scheme}://{host_name}", href)

    string = tag.get_text()
    tag.replace_with(f"{string} [{href}]")
