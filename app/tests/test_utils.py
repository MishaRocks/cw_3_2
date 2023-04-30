import pytest
from app.utils.utils import read_json, skip_numbers


@pytest.fixture
def data():
    test_list = [{'date': '2019-11-13T17:38:04.800051',
                  'description': 'Перевод со счета на счет',
                  'from': 'Счет 38611439522855669794',
                  'id': 482520625,
                  'operationAmount': {'amount': '62814.53',
                                      'currency': {'code': 'RUB', 'name': 'руб.'}},
                  'state': 'EXECUTED',
                  'to': 'Счет 46765464282437878125'},
                 {'date': '2019-11-19T09:22:25.899614',
                  'description': 'Перевод организации',
                  'from': 'Maestro 7810846596785568',
                  'id': 154927927,
                  'operationAmount': {'amount': '30153.72',
                                      'currency': {'code': 'RUB', 'name': 'руб.'}},
                  'state': 'EXECUTED',
                  'to': 'Счет 43241152692663622869'}]
    return test_list


def test_read_json():
    assert read_json('ata/operations.json') == None
    assert read_json('data/operations.json') == [{'date': '2019-11-05T12:04:13.781725', 'description': 'Открытие вклада', 'id': 801684332, 'operationAmount': {'amount': '21344.35', 'currency': {'code': 'RUB', 'name': 'руб.'}}, 'state': 'EXECUTED', 'to': 'Счет 77613226829885488381'}, {'date': '2019-11-13T17:38:04.800051', 'description': 'Перевод со счета на счет', 'from': 'Счет 38611439522855669794', 'id': 482520625, 'operationAmount': {'amount': '62814.53', 'currency': {'code': 'RUB', 'name': 'руб.'}}, 'state': 'EXECUTED', 'to': 'Счет 46765464282437878125'}, {'date': '2019-11-19T09:22:25.899614', 'description': 'Перевод организации', 'from': 'Maestro 7810846596785568', 'id': 154927927, 'operationAmount': {'amount': '30153.72', 'currency': {'code': 'RUB', 'name': 'руб.'}}, 'state': 'EXECUTED', 'to': 'Счет 43241152692663622869'}, {'date': '2019-12-07T06:17:14.634890', 'description': 'Перевод организации', 'from': 'Visa Classic 2842878893689012', 'id': 114832369, 'operationAmount': {'amount': '48150.39', 'currency': {'code': 'USD', 'name': 'USD'}}, 'state': 'EXECUTED', 'to': 'Счет 35158586384610753655'}, {'date': '2019-12-08T22:46:21.935582', 'description': 'Открытие вклада', 'id': 863064926, 'operationAmount': {'amount': '41096.24', 'currency': {'code': 'USD', 'name': 'USD'}}, 'state': 'EXECUTED', 'to': 'Счет 90424923579946435907'}]


def test_skip_numbers(data):
    assert skip_numbers(data) == [{'date': '13.11.2019', 'description': 'Перевод со счета на счет', 'from': 'Счет: **** **** **** **** 9794', 'id': 482520625, 'operationAmount': {'amount': '62814.53', 'currency': {'code': 'RUB', 'name': 'руб.'}}, 'state': 'EXECUTED', 'to': 'Счет: **** **** **** **** 8125'},
                                  {'date': '19.11.2019', 'description': 'Перевод организации', 'from': 'Maestro: 7810 **** **** 5568', 'id': 154927927, 'operationAmount': {'amount': '30153.72', 'currency': {'code': 'RUB', 'name': 'руб.'}}, 'state': 'EXECUTED', 'to': 'Счет: **** **** **** **** 2869'}]
