import re
import csv
print('Программа запускается...')
with open("csv_data/phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def organizing_fio() -> list:
    print("Сортируются ФИО...")
    fio: list[dict[str, str]] = []
    unique_fio: list = []
    for contact in contacts_list:
        new_contact = " ".join(contact[0:3]).split(" ")
        part_fio = []
        for name in new_contact:
            if name != '':
                part_fio.append(name)
        if len(part_fio) < 3:
            pass
        else:
            if ' '.join(part_fio) not in unique_fio:
                unique_fio.append(' '.join(part_fio))
                fio.append({'last_name': part_fio[0], 'first_name': part_fio[1], 'surname': part_fio[2]})
    return fio


def change_numbers():
    print("Декомпозируются номера телефонов...")
    with open("csv_data/phonebook.csv", encoding="utf8") as f:
        text = f.read()
    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
    with open("csv_data/phonebook.csv", 'w+', encoding="utf8") as f:
        f.write(fixed_phones)


def dict_for_csv() -> list:
    print("Создаётся словарь для файла...")
    birth_info: dict[str, str]
    new_fio = []
    for birth_info in organizing_fio():
        for person in contacts_list[:-1]:
            if birth_info['last_name'] == person[0].split()[0]:
                if person[-4] != '':
                    birth_info['organization'] = person[-4]
                if person[-3] != '':
                    birth_info['position'] = person[-3]
                if person[-2] != '':
                    birth_info['phone'] = person[-2]
                if person[-1] != '':
                    birth_info['email'] = person[-1]
        new_fio.append(list(birth_info.values()))
    return new_fio


# TODO 2: сохраните получившиеся данные в другой файл
if __name__ == '__main__':
    print("Информация записывается в файл...")
    with open("csv_data/phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(dict_for_csv())
    change_numbers()
