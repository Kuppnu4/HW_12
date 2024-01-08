'''
This modul contain classes which implement the Adress Book model
'''

from collections import UserDict
import re
from datetime import datetime
import pickle
import csv

# pylint: disable=too-few-public-methods
class Field:
    '''
    Базовий клас для полів запису. Буде батьківським для всіх полів,
    у ньому реалізується логіка загальна для всіх полів
    '''
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        '''
        value getter
        '''
        return self.__value

    @value.setter
    def value(self, new_value):
        '''
        value setter
        '''
        if self.is_valid():
            self.__value = new_value
        else:
            raise ValueError

    def is_valid(self):
        '''
        болванка. метод всегда возвращает True
        '''
        return True


class Birthday(Field):
    '''
    Поле для дня народження
    '''
    def __init__(self, value):

        self.__value = value
        if self.is_valid():
            super().__init__(self.__value)
        else:
            raise ValueError('Wrong Date')

    def is_valid(self):
        regexp_birthday = re.compile(r'^(?:0[1-9]|[12][0-9]|3[01])-(?:0[1-9]|1[0-2])-(?:19\d{2}|20[0-1]\d|202[0-3])$')

        return bool(regexp_birthday.match(self.__value))



# pylint: disable=too-few-public-methods
class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''

    def __init__(self, value):
        self.__value = value
        if self.is_valid():
            super().__init__(self.__value)
        else:
            raise ValueError('Wrong name')

    def is_valid(self):
        regexp_name = re.compile(r'^[a-zA-Z0-9]{3,15}$')

        return bool(regexp_name.match(self.__value))




# pylint: disable=too-few-public-methods
class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном та таких один запис Record
    може містити декілька.
    '''

    def __init__(self, value):
        self.__value = value
        if self.is_valid():
            super().__init__(self.__value)
        else:
            raise ValueError('Wrong phone number')

    def is_valid(self):
        regexp_10_digits = re.compile(r'^\d{10}$')

        return bool(regexp_10_digits.match(self.__value))



class Record:
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я
    та список телефонів. Відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name
    '''

    def __init__(self, name_value, birthday_value=None):

        self.name = Name(name_value)
        self.phones = []
        if birthday_value:
            self.birthday = Birthday(birthday_value)
        else:
            self.birthday = birthday_value

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


    def days_to_birthday(self):
        '''
        days till next birthday counter
        '''
        result = None
        if self.birthday:
            today = datetime.now()
            this_year = today.year
            days_b4_birthday = 0

            birthday_date_obj = datetime.strptime(self.birthday.value, '%d-%m-%Y')

            this_year_birthday_obj = datetime(
                year = this_year,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )
            next_year_birthday_obj = datetime(
                year = this_year + 1,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )

            if this_year_birthday_obj < today:
                days_b4_birthday = next_year_birthday_obj - today
            else:
                days_b4_birthday = this_year_birthday_obj - today

            result = days_b4_birthday.days

        else:
            print('The birthday was not stated')

        return result


    def add_phone(self, number):
        '''
        Додавання телефонів.
        '''
        self.phones.append(Phone(number))


    def remove_phone(self, number):
        '''
        Видалення телефонів.
        '''
        phones = [phone.value for phone in self.phones]

        if not number in phones:
            raise ValueError('Wrong number')

        for phone_obj in self.phones:
            if phone_obj.value == number:
                self.phones.remove(phone_obj)

    def edit_phone(self, old_number, new_number):
        '''
        Редагування телефонів.
        '''
        exist = False

        for phone_obj in self.phones:
            if phone_obj.value == old_number:

                index_of_old_number = self.phones.index(phone_obj)
                self.phones[index_of_old_number].value = new_number
                exist = True

        if not exist:
            raise ValueError('Wrong nuber')


    def find_phone(self, search_phone):
        '''
        Пошук телефону.
        '''
        find_phone_obj = None
        for phone_obj in self.phones:

            if phone_obj.value == search_phone:
                find_phone_obj = phone_obj

        return find_phone_obj


class AddressBook(UserDict):
    '''
    Клас для зберігання та управління записами. Успадковується від UserDict,
    та містить логіку пошуку за записами до цього класу

    Видалення записів за іменем.
    '''


    def iterator(self):
        '''
        method which iterate address book
        '''
        return Generator(self.data)

    def add_record(self, record_obj):
        '''
        Додавання записів.
        '''
        self.data[record_obj.name.value] = record_obj

    def find(self, search_name):
        '''
        Пошук записів за іменем.
        '''
        for abonent in self.data:
            found_numbers = None
            if abonent == search_name:
                found_numbers = self.data[search_name]

            return found_numbers

    def delete(self, name_str):
        '''
        Видалення записів за іменем.
        '''
        if name_str in self.data:
            del self.data[name_str]

    def save_address_book(self):
        '''
        method dumps address_book to the file
        '''
        file_name = 'address_book.dat'

        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def save_to_table(self):
        '''
        this method saves adresBook to table
        '''
        file_name = 'address_book.csv'
        with open(file_name, 'w', newline='', encoding='utf-8') as file:

            field_names = ['name', 'phones', 'birthday']
            writer = csv.DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            for contact in self.data:
                writer.writerow({'name': self.data[contact].name.value,
                             'phones': [phone.value for phone in self.data[contact].phones],
                             'birthday': self.data[contact].birthday
                                 })

    def read_address_book(self):
        '''
        method loads address_book from the file
        '''
        file_name = 'address_book.dat'
        with open(file_name, 'rb') as file:
            decoded_book = pickle.load(file)
        return decoded_book

    def search(self, search_str):
        '''
        method searches contacts which name or phones match with "search string"
        '''
        result = []
        for abonent_name, abonent_obj in self.data.items():

            if search_str.lower() in abonent_name.lower():
                result.append(str(abonent_obj))
                continue

            for phone in abonent_obj.phones:
                if search_str in phone.value:
                    result.append(str(abonent_obj))
                    break

        return f'matching contacts: {result}'


class Generator:
    '''
    class which generate outputs of adress book
    '''

    def __init__(self, data_dict, n=3):

        self.n = n
        self.data_dict = data_dict
        self.contacts_list = []                                 #список контактов из data_dict, этот список мы перебираем в __next__
        for key, value in self.data_dict.items():
            self.contacts_list.append(f'{key} --- {value}')
        self.written_contacts = []                              #список записанных уже взятых контактов для выдачи
        self.result_contacts = []                               #список из 2х контактов для выдачи


    def __iter__(self):
        return self

    def __next__(self):

        if len(self.written_contacts) < len(self.data_dict):                #проверяем колличество уже взятых контактов для вывода
            self.result_contacts = []

            if len(self.contacts_list) > self.n - 1:                        #проверяем колличество оставшихся контактов для обработки
                self.result_contacts = self.contacts_list[0:self.n]         #берем из списка контактов необходимое колличество

                for _ in range(self.n):
                    self.written_contacts.append(self.contacts_list[0])     #добавляем контакт в список уже взятых контактов
                    del self.contacts_list[0]               #удаляем взятый контакт из списка всех контактов оставшихся для обработки

            else:
                self.result_contacts = self.contacts_list[0:self.n]

                for _ in range(len(self.contacts_list)):
                    self.written_contacts.append(self.contacts_list[0])
                    del self.contacts_list[0]

            return self.result_contacts                   #возвращаем результат итерации, в виде списка контактов заданной длины

        raise StopIteration


if __name__ == '__main__':
    pass
