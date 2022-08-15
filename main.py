'''
Модуль для сокращения ссылок и отчета о количестве кликов.
Используются два сервиса: Bitly и ReBrandly.

Интерфейс.
Команда "create", параметры "link" обязательный и "number" (Сколько нужно создать ссылок)
необязательный.
Команда "report", параметр ID короткой ссылки.

В команде "create" выбор сервиса производится по дополнительному параметру "number".
Если этот параметр заполнен, то применяется ReBrandly. Конанда возвращает
от 1 до number строк вида short_link|short_link_id.

В команде "report" выбор сервиса зависит от типа ID. Если ID это ссылка, то применяется
Bitly, если GUID, то ReBrandly. Возвращает количество кликов.

Логика выбора сервиса основана на том факте, что Bitly при повторном вызове для одной и той же
длинной ссылки создает только одну короткую, а ReBrandly создает разные,
поэтому ReBrandly удобнее для анализа эффективности рекламной компании.

'''
import argparse
import os
import sys

from dotenv import load_dotenv
import requests as req

from bitly  import Shortener_Bitly
from rebrandly import Shortener_Rebrandly


def get_cli_args():
    parser = argparse.ArgumentParser(description='Генерация укороченных ссылок и отчет о кликах')
    subparsers = parser.add_subparsers(dest='command', description='Список команд')
    
    parser_create = subparsers.add_parser('create', help='Создать ссылку')
    parser_create.add_argument('link', help='Длинная ссылка')
    parser_create.add_argument(
        'number',
        type=int,
        nargs='?',
        help='Сколько нужно создать ссылок'
    )

    parser_report = subparsers.add_parser('report', help='Отчет о количестве кликов')
    parser_report.add_argument('id', help='ID короткой ссылки')    
        
    return parser.parse_args()


def create_bitly():
    token = os.environ['BITLINK_TOKEN']
    return Shortener_Bitly(token)


def create_brandly():
    token = os.environ['REBRANDLY_TOKEN']        
    return Shortener_Rebrandly(token)


def get_shortener_by_number(number):
    if number is None:
        return create_bitly()
    
    return create_brandly()

        
def get_shortener_by_id(link_id):
    if '.' in link_id:
        return create_bitly()

    return create_brandly()


if __name__ == "__main__":
    
    load_dotenv()    
    args = get_cli_args()    
    
    if (args.command == 'create'):        
        shortener = get_shortener_by_number(args.number)
        if args.number is None or args.number < 1:
            args.number = 1
        
        try:
            for i in range(args.number):
                print(shortener.shorten_link(args.link))
                
        except req.exceptions.HTTPError as err:    
            print(err)
            

    if (args.command == 'report'):        
        shortener = get_shortener_by_id(args.id)
        if (shortener.is_short_link(args.id)):
            print(shortener.count_click(args.id))
