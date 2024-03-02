import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, FILE_PARAMETR, PRETTY_PARAMETR

MESSAGE_INFO = 'Файл с результатами был сохранён: {file_path}'
RESULTS_PARAMETR = 'results'


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    RESULTS_DIR = BASE_DIR / RESULTS_PARAMETR
    RESULTS_DIR.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = RESULTS_DIR / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect=csv.unix_dialect).writerows(results)
    logging.info(MESSAGE_INFO.format(file_path=file_path))


VAR_OUTPUT = {
    PRETTY_PARAMETR: pretty_output,
    FILE_PARAMETR: file_output,
    None: default_output
}


def control_output(results, cli_args):
    VAR_OUTPUT.get(cli_args.output)(results, cli_args)
