import json
import datetime


def read_json(file: str) -> list:
    """
    Читаем json и выводим список с одобренные EXECUTED операциями.
    И главное - исключаем пустой словарь.
    Сортируем по дате.
    Берём последние 5 операций.
    """
    try:
        with open(file, 'r', encoding='UTF8') as d:
            data = json.load(d)
            operate_list = [o for o in data if o.get("state") if o["state"] == "EXECUTED"]
        return sorted(operate_list, key=lambda o: o['date'])[-5:]
    except FileNotFoundError:
        print(f'Не правильно указан путь к файлу')


def skip_numbers(skip_list: list) -> list:
    """
    Скрываем номера счетов отправителя и получателя, в зависимости от карт, или счетов
    """

    for o in skip_list:
        o['date'] = datetime.datetime.strptime(o['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        if 'from' in o:
            new_from = (o['from']).split()
            if new_from[0] == 'Счет':
                o['from'] = f"{new_from[0]}: **** **** **** **** {new_from[1][-4:]}"
            elif new_from[0] == 'Visa':
                o['from'] = f"{new_from[0]} {new_from[1]}: {new_from[2][0:4]} **** **** {new_from[2][-4:]}"
            else:
                o['from'] = f"{new_from[0]}: {new_from[1][0:4]} **** **** {new_from[1][-4:]}"

        if 'to' in o:
            new_to = (o['to']).split()
            if new_to[0] == 'Счет':
                o['to'] = f"{new_to[0]}: **** **** **** **** {new_to[1][-4:]}"
            elif new_to[0] == 'Visa':
                o['to'] = f"{new_to[0]} {new_to[1]}: {new_to[2][0:4]} **** **** {new_to[2][-4:]}"
            else:
                o['to'] = f"{new_to[0]}: {new_to[1][0:4]} **** **** {new_to[1][-4:]}"

    return skip_list


def form_vision_list(file) -> str:
    """
    Формируем список нужного формата
    """

    read_list = read_json(file)
    skip_list = skip_numbers(read_list)

    vision_list = ''
    for o in skip_list:
        if 'from' in o:
            message = (f"{o['date']} {o['description']} \n"
                       f"{o['from']} -> {o['to']} \n"
                       f"{o['operationAmount']['amount']} {o['operationAmount']['currency']['name']} \n \n")
        else:
            message = (f"{o['date']} {o['description']} \n"
                       f"Зачисление на {o['to']} \n"
                       f"{o['operationAmount']['amount']} {o['operationAmount']['currency']['name']} \n \n")
        vision_list += message

    return vision_list
