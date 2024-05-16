import argparse
import json
import requests
import time
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from parse_tululu import (parse_book_page, download_txt,
                          download_image, check_for_redirect)


def download_fantastic_books(start_page, end_page):
    books_content = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l55/{page}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books = soup.select('#content .d_book')
            for book in books:
                try:
                    book_page_url = urljoin(url, book.select_one('a')['href'])
                    response = requests.get(book_page_url)
                    response.raise_for_status()
                    check_for_redirect(response)
                    book_content = parse_book_page(book_page_url, response.content)

                    full_image_url = book_content['image_url']
                    if full_image_url:
                        download_image(full_image_url)

                    book_file_url = book_content['book_url']
                    book_id = unquote(urlparse(book_file_url).query).split('=')[-1]
                    book_filename = f'{book_id}. {book_content["title"]}.txt'
                    if book_file_url:
                        download_txt(book_file_url, book_filename)
                    books_content.append(book_content)
                except requests.exceptions.HTTPError as e:
                    sys.stderr.write(f'Ошибка HTTP: {e}\n')
                except requests.exceptions.ConnectionError as e:
                    sys.stderr.write(f'Ошибка соединения: {e}\n')
                    time.sleep(10)
        except requests.exceptions.HTTPError as e:
            sys.stderr.write(f'Ошибка HTTP: {e}\n')
        except requests.exceptions.ConnectionError as e:
            sys.stderr.write(f'Ошибка соединения: {e}\n')
            time.sleep(10)
    with open('books.json', 'w') as books_file:
        json.dump(books_content, books_file, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Парсинг книг с сайта tululu.org'
    )
    parser.add_argument(
        "--start_page",
        type=int,
        default=1,
        help='Номер первой страницы для скачивани книг'
    )
    parser.add_argument(
        "--end_page",
        type=int,
        default=702,
        help='Номер последней страницы для скачивани книг'
    )
    args = parser.parse_args()
    download_fantastic_books(args.start_page, args.end_page)


if __name__ == '__main__':
    main()
