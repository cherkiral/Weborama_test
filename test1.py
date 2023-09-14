import random, string
class HashTable:
    def __init__(self, filepath):
        self.filepath = rf'{filepath}'
        self.table = {}

    def parse_file(self):
        with open(self.filepath, 'r') as f:
            unparsed_list = f.readlines()
            parsed_list = [item.rstrip() for item in unparsed_list]
        return parsed_list

    def create_parsed_dict(self, id):
        if id not in self.table.keys():
            self.table[id] = 1
        else:
            self.table[id] += 1

        return self.get_ids(self.table)

    def amount_of_ids_is_3(self):
        dict_with_ids_3 = {}
        for key, value in self.table.items():
            if value == 3:
                dict_with_ids_3[key] = value
        return dict_with_ids_3

    @staticmethod
    def get_ids(text_list):
        list_of_ids = []
        for item in text_list:
            list_of_ids.append(item.split(',')[1])
        return list_of_ids

    @staticmethod
    def random_word():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    @staticmethod
    def randon_number():
        return random.randint(10**5, 10**6 - 1)

    @staticmethod
    def create_test_file():
        string_list = []
        for i in range(100000):
            string = HashTable.random_word() + ',' + str(HashTable.randon_number())
            string_list.append(string)

        with open('test.txt', 'w') as f:
            string_list = [item + '\n' for item in string_list]
            f.writelines(string_list)



HS = HashTable('test.txt')
text_list = HS.parse_file()
id_list = HS.get_ids(text_list)

for item in id_list:
    HS.create_parsed_dict(item)

print(HS.amount_of_ids_is_3())