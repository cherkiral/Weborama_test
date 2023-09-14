import sys
import pathlib
from ebooklib import epub
from bs4 import BeautifulSoup


class FB2Parser:
    def __init__(self, filepath):
        self.book_path = filepath

    @staticmethod
    # При поиске элемента в soup ьожет вернуться None есди элемент не найден. Если это произошло функция возвращает пустую строку.
    def get_element_text_or_none(element):
        if element:
            return element.text
        else:
            return ''

    # Создает объект soup
    def get_soup(self):
        with open(self.book_path, 'r', encoding='utf-8') as f:
            xml_file = f.read()
            soup = BeautifulSoup(xml_file, 'lxml')
            return soup

    # Парсит данные с помощью тэгов
    def parse_data(self):
        soup = self.get_soup()

        first_name = self.get_element_text_or_none(soup.find('first-name'))
        middle_name = self.get_element_text_or_none(soup.find('middle-name'))
        last_name = self.get_element_text_or_none(soup.find('last-name'))
        author = first_name + ' ' + middle_name + ' ' + last_name
        title = self.get_element_text_or_none(soup.find('book-title'))
        publisher = self.get_element_text_or_none(soup.find('publisher'))
        date = self.get_element_text_or_none(soup.find('year'))

        return [title, author, publisher, date]




class EpubParser:
    def __init__(self, filepath):
        self.book = epub.read_epub(filepath)

    # Если get_metadata возвращает пустой список, функция возвращает пустую строку, в другом случае получет данные из JSON
    @staticmethod
    def check_if_null(value):
        if not value:
            value = ''
        else:
            return value[0][0]
        return value

    # Если в JSON дата была, то берем только год, в противном случае возвращает пустую строку
    @staticmethod
    def get_year(date):
        if not date:
            value = ''
        else:
            return date[:4]
        return value

    # Парсит данные из метадаты
    def parse_data(self):
        title = self.book.title
        author = self.check_if_null(self.book.get_metadata('DC', 'creator'))
        publisher = self.check_if_null(self.book.get_metadata('DC', 'publisher'))
        date = self.get_year(self.check_if_null(self.book.get_metadata('DC', 'date')))

        return [title, author, publisher, date]


if __name__ == '__main__':
    # Путь до файла как аргумент командной строки
    file_path = rf'{sys.argv[1]}'
    file_extention = pathlib.Path(file_path).suffix

    try:
        if file_extention == '.epub':
            print(EpubParser(file_path).parse_data())
        elif file_extention == '.fb2':
            print(FB2Parser(file_path).parse_data())
        else:
            print('Wrong file format')
    except FileNotFoundError:
        print('Not a valid file')