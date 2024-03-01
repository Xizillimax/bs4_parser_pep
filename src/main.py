import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, make_soup

DOWNLOADS_DIR = BASE_DIR / 'downloads'

MESSAGE_NOT_CORRECT_STATUS = """Несовпадающие статусы:
                                {link_object}
                                Статус в карточке: {dd}
                                Ожидаемые статусы: {status}"""

MESSAGE_INFO = 'Архив был загружен и сохранён: {archive_path}'
MESSAGE_START_PARSER = 'Аргументы командной строки: {args}'


def whats_new(session):
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    for section in tqdm(make_soup(session, whats_new_url).select(
            '#what-s-new-in-python div.toctree-wrapper li.toctree-l1')):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        results.append(
            (version_link,
             find_tag(make_soup(session, version_link), 'h1').text,
             find_tag(make_soup(session, version_link),
                      'dl').text.replace('\n', ' '))
        )
    return results


def latest_versions(session):
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    sidebar = find_tag(make_soup(session, MAIN_DOC_URL),
                       'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise KeyError('Не найден список c версиями Python')
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    main_tag = find_tag(make_soup(session, downloads_url),
                        'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(MESSAGE_INFO.format(archive_path=archive_path))


def pep(session):
    logs = []
    counter = defaultdict(int)
    for string in tqdm(make_soup(session, PEP_URL).select(
            '#numerical-index tbody tr')):
        td_tag = find_tag(string, "td")
        href_object = td_tag.find_next_sibling("td")
        link_object = urljoin(PEP_URL, href_object.a["href"])
        start = find_tag(make_soup(session, link_object),
                         text=re.compile("^Status$")).parent
        dd = start.find_next_sibling("dd").text

        if dd not in EXPECTED_STATUS[
                list(td_tag.text)[-1] if len(td_tag.text) == 2 else '']:
            status = EXPECTED_STATUS[list(td_tag.text)[-1]]
            logs.append(MESSAGE_NOT_CORRECT_STATUS.format(
                link_object=link_object,
                dd=dd,
                status=status
            ))
        counter[dd] += 1
    for log in logs:
        logging.info(log)
    return [
        ('Статус', 'Количество'),
        *counter.items(),
        ('Всего', sum(counter.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(MESSAGE_START_PARSER.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(error, stack_info=True)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
