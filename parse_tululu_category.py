import requests
import time
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from parse_tululu import (parse_book_page, download_txt,
                          download_image, check_for_redirect)


def download_fantastic_books():
    for page in range(1, 5):
        url = f'https://tululu.org/l55/{page}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books = soup.find_all('table', class_="d_book")
            for book in books:
                try:
                    book_page_url = urljoin(url, book.find('a')['href'])
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

                except requests.exceptions.HTTPError as e:
                    sys.stderr.write(f'Ошибка HTTP: {e}\n')
                except requests.exceptions.ConnectionError as e:
                    sys.stderr.write(f'Ошибка соединения: {e}\n')
                    time.sleep(10)
        except requests.exceptions.HTTPError as e:
            sys.stderr.write(f'Ошибка HTTP: {e}')
        except requests.exceptions.ConnectionError as e:
            sys.stderr.write(f'Ошибка соединения {url}: {e}\n')
            time.sleep(10)

    '''book = [books.find_all('a')['href'] for book in books]
    soup.find_all('a', class_='npage')[-1]['href']'''


if __name__ == '__main__':
    download_fantastic_books()
