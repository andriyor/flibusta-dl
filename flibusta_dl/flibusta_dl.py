import os
import sys
import time
import cgi
import pathlib
import zipfile

import click
import requests
import grequests
import humanize
from pyquery import PyQuery as pq
from tqdm import tqdm

_t = humanize.i18n.activate('ru_RU')

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

    if r.text == 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        tqdm.write(f'Не нашлось ни единой книги по запросу {book_name}')
        return 'No result'
    else:
        return r.text


def fetch_book_id(search_result, sort):
    doc = pq(search_result)
    if sort == 'litres':
        book = [pq(i)('div > a').attr.href for i in doc.find('div') if '[litres]' in pq(i).text().lower()][0]
    elif sort == 'rating':
        books = [(pq(i)('div > a').attr.href, pq(i)('img').attr.title) for i in doc.find('div')]
        # print(books)
        # pass
        book = sorted(books, key=lambda book: RATING[book[1]], reverse=True)[0][0]
        # book = sorted(books, key=lambda book: RATING[book[1], reverse=True)[0][0]
    else:
        book = doc('div > a').attr.href
    return book


def get_all_links(books, sort, file_format):
    books_link = dict()
    for book_name in books:
        search_result = get_search_result(book_name, sort)
        if search_result == 'No result':
            continue
        else:
            book = fetch_book_id(search_result, sort)
            link = f'http://flibusta.is{book}/{file_format}'
            books_link[book_name] = link
    return books_link


def save_file(sfn, book_file, output_folder, file_format, book_name):
    if sfn:
        filename = cgi.parse_header(book_file.headers['content-disposition'])[1]['filename']
        file_path = os.path.join(output_folder, filename)
    else:
        file_path = os.path.join(output_folder, f'{book_name}.{file_format}')

    with open(file_path, 'wb') as f:
        f.write(book_file.content)

    if file_format == 'fb2':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        os.remove(file_path)


def download_async(books_link, sfn, output_folder, file_format):
    downloaded_sizes, downloaded_book = [], []
    rs = (grequests.get(u) for u in books_link.values())
    for book_file, book_name in zip(grequests.map(rs, size=3), books_link.keys()):
        save_file(sfn, book_file, output_folder, file_format, book_name)

        content_length = int(book_file.headers['content-length'])
        downloaded_sizes.append(content_length)
        downloaded_book.append(book_name)
        size = humanize.naturalsize(content_length)
        click.echo(f'книга {book_name} загружена размер - {size}')

    total_size = humanize.naturalsize(sum(downloaded_sizes))
    return downloaded_book, total_size


def download_sync(books_link, sfn, output_folder, file_format):
    downloaded_sizes, downloaded_book = [], []
    for book_name, book_link  in tqdm(books_link.items(), miniters=1, disable=True):
        book_file = requests.get(book_link)
        save_file(sfn, book_file, output_folder, file_format, book_name)

        content_length = int(book_file.headers['content-length'])
        downloaded_sizes.append(content_length)
        downloaded_book.append(book_name)
        size = humanize.naturalsize(content_length)
        tqdm.write(f'книга {book_name} загружена размер - {size}')

    total_size = humanize.naturalsize(sum(downloaded_sizes))
    return downloaded_book, total_size


@click.command()
@click.argument('infile', type=click.File('r'))
@click.option('-of', '--output_folder', default='flibusta_books', help='путь к папке в которую будут сохранятся книги')
@click.option('--min-filesize', 'sort', flag_value='ss1', help='загрузка книг с минимальным размером')
@click.option('--max-filesize', 'sort', flag_value='ss2', help='загрузка книг  с максимальным размером')
@click.option('-o', '--oldest', 'sort', flag_value='sd1', help='загрузка самых старых книг')
@click.option('-n', '--newest', 'sort', flag_value='sd2', default=True, help='загрузка самых новых книг')
@click.option('-l', '--litres', 'sort', flag_value='litres', help='приоритет загрузки по litres')
@click.option('-r', '--rating', 'sort', flag_value='rating', help='приоритет загрузки по оценке')
@click.option('-ff', '--file_format', type=click.Choice(['fb2', 'epub', 'mobi']), default='epub', help=' формат книг')
@click.option('--sfn', is_flag=True, help='имя файла такое же как при загрузке с сайта')
@click.option('--asy', is_flag=True, help='асинхронная загрузка книг')
def cli(infile, output_folder, sort, file_format, sfn, asy):
    books = infile.read().splitlines()
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    if asy:
        books_link = get_all_links(books, sort, file_format)
        downloaded_book, total_size = download_async(books_link, sfn, output_folder, file_format)
    else:
        books_link = get_all_links(books, sort, file_format)
        downloaded_book, total_size = download_sync(books_link, sfn, output_folder, file_format)

    end_time = humanize.naturaldelta(time.time() - start_time)
    click.echo(f'всего загружено {len(downloaded_book)} книг из {len(books)} общим размером - {total_size} за {end_time}')
