import csv
import os


def search(data):  # поиск книг или выведение всего списка
    with open('library.csv', encoding='utf-8') as library_csv:
        library_rows = csv.DictReader(library_csv)
        output = []
        if data == 'list':
            return list(library_rows)
        else:
            for item in library_rows:
                if (
                    item['title'].lower() == data
                    or item['author'].lower() == data
                    or str(item['year']) == data
                ):
                    output.append(item)
                else:
                    pass
            if len(output) == 0:
                return ["\nCan't find your book.\n"
                        "Please check that the entered data is correct."]
            else:
                return output


def add_book(title, author, year):  # добавление новой книги
    books_id_list = []
    books_list = []
    new_id = 1
    with open('library.csv', encoding='utf-8') as library_csv_read:
        library_rows = csv.DictReader(library_csv_read)
        for item in library_rows:
            books_id_list.append(int(item['id']))
            books_list.append(item)
        while new_id in books_id_list:
            new_id += 1
    with open('library.csv', 'w', encoding='utf-8') as library_csv:
        columns = ['id', 'title', 'author', 'year', 'status']
        data = {
            'id': new_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'in stock'
            }
        writer = csv.DictWriter(library_csv, fieldnames=columns)
        writer.writeheader()
        for row in books_list:
            writer.writerow(row)
        writer.writerow(data)
    return new_id


def delete(id):  # удаление книги
    with open('library.csv', encoding='utf-8') as library_csv:
        library_rows = csv.DictReader(library_csv)
        with open('temporary.csv', mode='w', encoding='utf-8') as file:
            columns = ['id', 'title', 'author', 'year', 'status']
            new_library = csv.DictWriter(
                file,
                fieldnames=columns,
                delimiter=',',
                quoting=csv.QUOTE_NONNUMERIC
                )
            new_library.writeheader()
            for item in library_rows:
                if str(item['id']) != id:
                    new_library.writerow(item)
    os.remove('library.csv')
    os.rename('temporary.csv', 'library.csv')
    return id


def change(id):  # изменение статуса
    with open('library.csv', encoding='utf-8') as library_csv:
        library_rows = csv.DictReader(library_csv)
        with open('temporary.csv', mode='w', encoding='utf-8') as file:
            columns = ['id', 'title', 'author', 'year', 'status']
            new_library = csv.DictWriter(
                file,
                fieldnames=columns,
                delimiter=',',
                quoting=csv.QUOTE_NONNUMERIC
                )
            new_library.writeheader()
            for item in library_rows:
                if str(item['id']) != id:
                    new_library.writerow(item)
                else:
                    new_item = {
                        'id': item['id'],
                        'title': item['title'],
                        'author': item['author'],
                        'year': item['year'],
                        'status': item['status']
                        }
                    if new_item['status'] == 'in stock':
                        new_item['status'] = 'not in stock'
                    else:
                        new_item['status'] = 'in stock'
                    new_library.writerow(new_item)
    os.remove('library.csv')
    os.rename('temporary.csv', 'library.csv')
    return id


print('Hello!')
print('Welcome to the digital library\n')
print('To find a book, enter "find"')
print('To list all books, enter "list"')
print('To add a book, enter "add"')
print('To delete a book, enter "delete"')
print('To change the status of a book, enter "change"')
print('To end the program, enter "exit"')


while (command := input().lower()) != 'exit':
    match command:
        case 'find':  # найти книгу
            print('Enter title, author or year of book:')
            book = str(input()).lower()
            local_search = search(book)
            for item in local_search:
                print(
                    f"ID: {item['id']}; "
                    f"Title: {item['title']}; "
                    f"Author: {item['author']}; "
                    f"Year: {item['year']}; "
                    f"Status: {item['status']}"
                    )

        case 'list':  # вывести полный список имеющихся книг
            list_books = search(command)
            print(list_books)
            for item in sorted(list_books, key=lambda x: x['id']):
                print(
                    f"ID: {item['id']}; "
                    f"Title: {item['title']}; "
                    f"Author: {item['author']}; "
                    f"Year: {item['year']}; "
                    f"Status: {item['status']}"
                    )

        case 'add':  # добавить книгу
            title = input('Please enter the title of the book: ')
            while title.strip() == '':
                print("Title of book can't be empty")
                title = input('Please enter the title of the book: ')
            author = input('Please enter the author of the book: ')
            while author.strip() == '':
                print("Author of book can't be empty")
                author = input('Please enter the author of the book: ')
            year = input('Please enter the year the book was published: ')
            while (year.isdigit() is not True
                   and (1564 > int(year) or int(year) > 2024)):
                year = input('Sorry, thats date is incorrect.\n'
                             'Please enter the year the book was published: ')
            temp_id = add_book(title, author, int(year))
            print(f'Book added! It is registered under ID {temp_id}')

        case 'delete':  # удалить книгу
            temp_id = input('Please enter the ID of book you wat to remove: ')
            while temp_id.isdigit() is not True:
                print('Incorrect ID')
                temp_id = input(
                    'Please enter the ID of book you wat to remove: '
                    )
            delete(str(temp_id))
            print(f'The book {temp_id} was deleted if it existed')

        case 'change':  # изменить статус книги
            temp_id = input('Please enter the ID of the book '
                            'wich status you want to change: ')
            while temp_id.isdigit() is not True:
                print('Incorrect ID')
                temp_id = input(
                    'Please enter the ID of book you wat to remove: '
                    )
            change(str(temp_id))
            print(f'The book {temp_id} was changed')

        case _:
            print('Unknown command. Please enter one of available command')
