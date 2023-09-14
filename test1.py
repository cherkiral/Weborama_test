import json
import random
import string
import time


class SortFile:
    def __init__(self, filepath):
        self.filepath = rf'{filepath}'
        self.table = {}
        self.parsed_list = []
        self.ids_list = []

    # Парсит файл в список строк (self.parsed_list) и обрезает \n на конце
    def parse_file(self):
        with open(self.filepath, 'r') as f:
            unparsed_list = f.readlines()
            self.parsed_list = [item.rstrip() for item in unparsed_list]
        return self.parsed_list

    # Берет self.parsed_list и создает из него список только из id
    def get_ids(self):
        for item in self.parsed_list:
            self.ids_list.append(item.split(',')[1])
        return self.ids_list

    # Создает словарь вида {id: количество раз встречающихся в файле}
    def create_parsed_dict(self):
        for id in self.ids_list:
            if id not in self.table.keys():
                self.table[id] = 1
            else:
                self.table[id] += 1
        return self.table

    # Заполняет self.table, self.parsed_list, self.ids_list данными
    def prepare_for_parsing(self):
        self.parse_file()
        self.get_ids()
        self.create_parsed_dict()

    # Ищет в self.table значения равные 3 и создает список
    def amount_of_ids_is_3(self):
        self.prepare_for_parsing()
        dict_with_ids_3 = {}
        for key, value in self.table.items():
            if value == 3:
                dict_with_ids_3[key] = value
        return [keys for keys in dict_with_ids_3.keys()]

    # Сортирует self.table по значениям
    def sorted_dict(self):
        self.prepare_for_parsing()
        return sorted(self.table.items(), key=lambda x: x[1])

    # Методы для создания файла со случайными cache:id
    @staticmethod
    def random_word():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    @staticmethod
    def randon_number():
        return random.randint(10 ** 5, 10 ** 6 - 1)

    @staticmethod
    def create_test_file():
        string_list = []
        for i in range(100000):
            string = SortFile.random_word() + ',' + str(SortFile.randon_number())
            string_list.append(string)

        with open('test.txt', 'w') as f:
            string_list = [item + '\n' for item in string_list]
            f.writelines(string_list)


if __name__ == '__main__':
    choise = input("Do you want to create random file? (y/n)\n")
    filepath = ''
    if choise == 'y':
        SortFile.create_test_file()
        filepath = 'test.txt'
    elif choise == 'n':
        filepath = rf'{input("Enter path to file: ")}'
    else:
        print('Not a valid input')

    # Создает 2 файла для 2-ух пунктов задания
    if filepath:
        try:
            with open('occur_3_times_in_file', 'w') as f:
                f.writelines(json.dumps(SortFile(filepath).amount_of_ids_is_3()))
            with open('sorted_file', 'w') as f:
                f.writelines(json.dumps(SortFile(filepath).sorted_dict()))
        except FileNotFoundError:
            print('Not a valid file')