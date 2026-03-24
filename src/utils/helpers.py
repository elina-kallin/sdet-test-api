import re


def strip_html_tags(text: str) -> str:
    """Удаляет HTML теги из текста"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()


def normalize_content(content: str) -> str:
    """Нормализует контент: удаляет HTML теги и лишние пробелы"""
    return strip_html_tags(content).replace('\n', '').replace('\r', '').strip()
