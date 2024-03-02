from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

MESSAGE_RESPONSE_ERROR = 'Возникла ошибка {error} при загрузке страницы {url}'
MESSAGE_ERROR = 'Не найден тег {tag} {attrs}'


def get_response(session, url, format_encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = format_encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            MESSAGE_RESPONSE_ERROR.format(error=error, url=url))


def find_tag(soup, tag=None, attrs=None, text=None):
    if text:
        searched_tag = soup.find(text=text)
    else:
        attrs_data = {} if attrs is None else attrs
        searched_tag = soup.find(tag, attrs=attrs_data)
    if searched_tag is None:
        raise ParserFindTagException(
            MESSAGE_ERROR.format(tag=tag, attrs=attrs))
    return searched_tag


def make_soup(session, url, feature="lxml"):
    return BeautifulSoup(get_response(session, url).text, features=feature)
