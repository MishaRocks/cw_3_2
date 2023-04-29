import json
import datetime


def read_json(file) -> list:
    """
    Читаем json и выводим список с одобренные EXECUTED операциями.
    И главное - исключаем пустой словарь)
    Сортируем по дате
    """
    with open(file, 'r', encoding='UTF8') as d:
        data = json.load(d)
        operate_list = [o for o in data if o.get("state") if o["state"] == "EXECUTED"]
        return sorted(operate_list, key=lambda o: o['date'])


def skip_numbers(file) -> list:
    """
    Скрываем номера счетов отправителя и получателя, в зависимости от карт
    берём последние 5 операций
    """
    skip_list = read_json(file)
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

    return skip_list[:5]


def form_vision_list(file) -> list:
    """
    Формируем список нужного формата
    """
    vision_list = []
    for o in skip_numbers(file):
        if 'from' in o:
            message = (f"{o['date']} {o['description']} \n"
                       f"{o['from']} -> {o['to']} \n"
                       f"{o['operationAmount']['amount']} {o['operationAmount']['currency']['name']} \n")
        else:
            message = (f"{o['date']} {o['description']} \n"
                       f"Зачисление на {o['to']} \n"
                       f"{o['operationAmount']['amount']} {o['operationAmount']['currency']['name']} \n")

        vision_list.append(message)
    return vision_list

