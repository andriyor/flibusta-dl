import os
import sys

import click
import requests
import humanize
from pyquery import PyQuery as pq
from tqdm import tqdm

RATING = {
    'файл не оценен': 0,
    'файл на 1': 1,
    'файл на 2': 2,
    'файл на 3': 3,
    'файл на 4': 4,
    'файл на 5': 5
}


def get_search_result(book_name, sort):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        r = requests.get('http://flibusta.is/makebooklist', params=payload)
    except requests.exceptions.ConnectionError:
        click.echo('не удалось подключиться к серверу flibusta.is')
        sys.exit(1)
    return r.text


def fetch_book_id(search_result, custom_sort):
    doc = pq(search_result)
    if custom_sort == 'litres':
        book = [pq(i)('div > a').attr.href for i in doc.find('div') if '[litres]' in pq(i).text().lower()][0]
    elif custom_sort == 'rating':
        books = [(pq(i)('div > a').attr.href, pq(i)('img').attr.title) for i in doc.find('div')]
        book = sorted(books, key=lambda book: RATING[book[1]], reverse=True)[0][0]
    else:
        book = doc('div > a').attr.href
    return book


@click.command()
@click.argument('infile', type=click.File('r'))
@click.option('--min-filesize', 'sort', flag_value='ss1')
@click.option('--max-filesize', 'sort', flag_value='ss2')
@click.option('--oldest', 'sort', flag_value='sd1')
@click.option('--newest', 'sort', flag_value='sd2', default=True)
@click.option('--litres', 'custom_sort', flag_value='litres')
@click.option('--rating', 'custom_sort', flag_value='rating')
@click.option('--fb2', 'file_format', flag_value='fb2')
@click.option('--epub', 'file_format', flag_value='epub', default=True)
@click.option('--mobi', 'file_format', flag_value='mobi')
def cli(infile, sort, file_format, custom_sort):
    books = infile.read().splitlines()
    downloaded_sizes, downloaded_book = [], []
    for book_name in tqdm(books, miniters=1):
        search_result = get_search_result(book_name, sort)

        if search_result == 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
            tqdm.write('Не нашлось ни единой книги по запросу {}.'.format(book_name))
            continue

        book = fetch_book_id(search_result, custom_sort)
        book_file = requests.get('http://flibusta.is{}/{}'.format(book, file_format))

        filename = os.path.join('books', '{}.{}'.format(book_name, file_format))
        with open(filename, 'wb') as f:
            f.write(book_file.content)
            content_length = int(book_file.headers['content-length'])
            downloaded_sizes.append(content_length)
            downloaded_book.append(book_name)
            size = humanize.naturalsize(content_length)
            tqdm.write('книга {} загружена размер - {}'.format(book_name, size))
    total_size = humanize.naturalsize(sum(downloaded_sizes))
    click.echo('всего загружено {} книг из {} общим размером - {}'.format(len(downloaded_book), len(books), total_size))
