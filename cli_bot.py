'''
На першому етапі наш бот-асистент повинен вміти зберігати ім'я
та номер телефону, знаходити номер телефону за ім'ям, змінювати записаний
номер телефону, виводити в консоль всі записи, які зберіг.
Щоб реалізувати таку нескладну логіку, скористаємося словником.
У словнику будемо зберігати ім'я користувача як ключ і номер телефону
як значення.
'''
import sys
#import re
from adresbook import AddressBook, Record

adres_book = AddressBook()

def input_error(func):
    '''
    This is the Errors handling function wrapper
    '''

    def inner(*args):
        '''
        THIS is the errors handling functions
        '''
        try:
            return func(*args)

        except (KeyError, ValueError, IndexError, TypeError) as err:
            return f'Error: {err}'

    return inner

@input_error
def hello_func():
    '''
    "hello", відповідає у консоль "How can I help you?"
    '''
    return 'How can I help you?'


@input_error
def add_func(*args):
    '''
    "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад)
    новий контакт. Замість ... користувач вводить ім'я та номер телефону,
    обов'язково через пробіл.
    '''

    res = ''

    if args[0] in adres_book.keys():
        adres_book[args[0]].add_phone(args[1])
        res = f'for {args[0]} was added the number {args[1]}'

    else:
        new_record = Record(args[0])
        new_record.add_phone(args[1])
        adres_book.add_record(new_record)
        res = f'{args[0]} was added'

    return res


@input_error
def del_func(*args):
    '''
    "hello", відповідає у консоль "How can I help you?"
    '''
    res = ''
    if len(args) == 1:
        adres_book.delete(args[0])
        res = f'Contact {args[0]} was deleted'
    elif len(args) == 2:
        adres_book[args[0]].remove_phone(args[1])
        res = f'Number {args[1]} from contact {args[0]} was deleted'
    else:
        res = 'Enter NAME or NAME with ONE number'

    return res

@input_error
def change_func(*args):
    '''
    "change ..." За цією командою бот зберігає в пам'яті новий номер телефону
    існуючого контакту. Замість ... користувач вводить ім'я та номер телефону,
    обов'язково через пробіл.
    '''
    if len(args) != 3:
        raise KeyError('Enter ONE name OLD number NEW number')

    if args[0] in adres_book:
        adres_book[args[0]].edit_phone(args[1], args[2])

    else:
        raise KeyError('No such name in the list')

    return f'Contact {args[0]}: Number {args[1]}  changed to {args[2]}'


@input_error
def phone_func(*args):
    '''
    "phone ...." За цією командою бот виводить у консоль номер телефону
    для зазначеного контакту. Замість ... користувач вводить ім'я контакту,
    чий номер треба показати.
    '''
    if len(args) > 1:
        raise ValueError('Enter one name')

    if args[0] in adres_book:
        return adres_book[args[0]]

    return 'No such name in the list'

@input_error
def show_func():
    '''
    "show all". За цією командою бот виводить всі збереженні контакти
    з номерами телефонів у консоль.
    '''

    return '\n'.join([str(rec) for rec in adres_book.values()])

@input_error
def exit_func():
    '''
    "good bye", "close", "exit" по будь-якій з цих команд бот завершує
    свою роботу після того, як виведе у консоль "Good bye!".
    '''
    adres_book.save_address_book()
    adres_book.save_to_table()
    return 'Good bye'



def main():
    '''
    This is the main function
    '''

    COMMANDS = {
        'hello': hello_func,
        'add': add_func,
        'delete': del_func,
        'change': change_func,
        'phone': phone_func,
        'show all': show_func,
        'exit': exit_func,
        'close': exit_func,
        'good bye': exit_func
        }

    while True:
        command = input('Enter the command: ')
        command_words = command.strip().split(' ')

        for _ in filter(lambda x: x == '.', command_words):
            command_words = ['good', 'bye']

        command_words[0] = command_words[0].lower()

        if len(command_words) == 2:
            if ' '.join([command_words[0], command_words[1].lower()]) in COMMANDS:
                command_words[0] = ' '.join([command_words[0], command_words[1].lower()])
                del command_words[1]

        if command_words[0] in COMMANDS:
            func_reply = COMMANDS[command_words[0]](*command_words[1:])
            if func_reply:
                print(func_reply)
            if func_reply == 'Good bye':
                sys.exit()
        else:
            print('wrong command')




if __name__ == '__main__':
    adres_book = adres_book.read_address_book()

    main()
