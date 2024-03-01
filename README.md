# Проект парсинга pep
## Описание
Программа-парсер собирает данные о статусах PEP, смотрит новые версии и записывает в файл необходимую информацию.

## Применяемые технологии

[![Python](https://img.shields.io/badge/Python-3.7-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![Beautiful Soup 4](https://img.shields.io/badge/BeautifulSoup-4.9.3-blue?style=flat-square&labelColor=d0d0d0)](https://beautiful-soup-4.readthedocs.io)

### Развертывание и запуск парсера

Клонировать репозиторий, перейти в папку в проектом, затем создать, активировать виртуальное окружение и установить зависимости:

```bash
git clone git@github.com:Xizillimax/bs4_parser_pep.git
cd bs4_parser_pep
python3 -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
```

## Работа с парсером

### Режимы работы
Сброр ссылок на статьи о нововведениях в Python:
```bash
python main.py whats-new
```
Сброр информации о версиях Python:
```bash
python main.py latest-versions
```
Скачивание архива с актуальной документацией:
```bash
python main.py download
```
Сброр статусов документов PEP и подсчёт их количества:
```bash
python main.py pep
```

### Аргументы командной строки
Полный список аргументов:
```bash
python main.py -h
```
```bash
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

Автор - [Maxim Zelenin](https://github.com/Xizillimax)