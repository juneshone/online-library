import argparse
import json
import requests
import time
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from parse_tululu import (parse_book_page, download_txt,
                          download_image, check_for_redirect)


def download_fantastic_books(start_page, end_page, dest_folder, skip_imgs, skip_txt):
    books_content = []
    for page in range(start_page, end_page):
        page_url = f'https://tululu.org/l55/{page}'
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            books = soup.select('#content .d_book')
            for book in books:
                book_page_url = urljoin(page_url, book.select_one('a')['href'])
                try:
                    response = requests.get(book_page_url)
                    response.raise_for_status()
                    check_for_redirect(response)
                    book_content = parse_book_page(book_page_url, response.content)

                    full_image_url = book_content['image_url']
                    if full_image_url and not skip_imgs:
                        download_image(
                            full_image_url,
                            folder=Path(dest_folder) / 'images/'
                        )
                    book_file_url = book_content['book_url']
                    book_id = unquote(urlparse(book_file_url).query).split('=')[-1]
                    book_filename = f'{book_content["title"]}.txt'
                    if book_file_url and not skip_txt:
                        download_txt(
                            book_file_url,
                            book_filename,
                            folder=Path(dest_folder) / 'books/'
                        )
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
    with open((Path(dest_folder) / 'books.json'), 'w', encoding='utf-8') as books_file:
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
    parser.add_argument(
        "--dest_folder",
        type=str,
        default='',
        help='Путь к каталогу с результатами парсинга'
    )
    parser.add_argument(
        "--skip_imgs",
        action='store_true',
        help='Не скачивать картинки'
    )
    parser.add_argument(
        "--skip_txt",
        action='store_true',
        help='Не скачивать книги'
    )
    args = parser.parse_args()
    Path(args.dest_folder).joinpath('books/').mkdir(
        parents=True,
        exist_ok=True
    )
    Path(args.dest_folder).joinpath('images/').mkdir(
        parents=True,
        exist_ok=True
    )

    download_fantastic_books(
        args.start_page,
        args.end_page,
        args.dest_folder,
        args.skip_imgs,
        args.skip_txt
    )



if __name__ == '__main__':
    main()
