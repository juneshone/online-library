import argparse
import os
import time
import sys
import requests
from pathvalidate import sanitize_filename
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    book_name = sanitize_filename(filename)
    filepath = os.path.join(folder, book_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    url_parts = unquote(urlparse(url).path)
    image_name = url_parts.split('/')[-1]
    filepath = os.path.join(folder, image_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(url, content):
    soup = BeautifulSoup(content, 'lxml')

    book_name = soup.select_one('h1').text.split('::', maxsplit=1)

    book_title = book_name[0].strip()
    book_author = book_name[1].strip()

    book_url = soup.select('table.d_book a')[-3]['href']
    full_book_url = urljoin(url, book_url)

    image_url = soup.select_one('.bookimage img')['src']
    full_image_url = urljoin(url, image_url)

    comments = soup.select('.texts')
    book_comments = [comment.select_one('span').text for comment in comments]

    genres = soup.select_one('span.d_book').select('a')
    book_genres = [genre.text for genre in genres]

    book_content = {
        'title': book_title,
        'author': book_author,
        'image_url': full_image_url,
        'comments': book_comments,
        'genres': book_genres,
        'book_url': full_book_url
    }
    return book_content


def main():
    Path("books/").mkdir(parents=True, exist_ok=True)
    Path("images/").mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(description='Скачивает книги')
    parser.add_argument(
        "start_id",
        type=int,
        default=1,
        help='C какой станицы скачивать'
    )
    parser.add_argument(
        "end_id",
        type=int,
        default=10,
        help='По какую страницу скачивать'
    )
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id):
        book_page_url = f"https://tululu.org/b{book_id}/"
        try:
            response = requests.get(book_page_url)
            response.raise_for_status()
            check_for_redirect(response)
            book_content = parse_book_page(book_page_url, response.content)

            full_image_url = book_content['image_url']
            download_image(full_image_url)

            book_file_url = book_content['book_url']
            book_filename = f'{book_id}. {book_content["title"]}.txt'
            if book_file_url:
                download_txt(book_file_url, book_filename)

            print('Название:', book_content['title'])
            print('Автор:', book_content['author'])
        except requests.exceptions.HTTPError as e:
            sys.stderr.write(f'Ошибка HTTP: {e}\n'
                             f'Отсутствует книга с id = {book_id}\n')
        except requests.exceptions.ConnectionError as e:
            sys.stderr.write(f'Ошибка соединения {url}: {e}\n')
            time.sleep(10)


if __name__ == '__main__':
    main()
