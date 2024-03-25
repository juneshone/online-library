import os
import requests
from pathvalidate import sanitize_filename
from pathlib import Path
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    book_file = sanitize_filename(filename)
    filepath = os.path.join(folder, book_file)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_books():
    for id in range(1, 11):
        book_url = f"https://tululu.org/b{id}/"
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        book_name = soup.find('h1').text.split('::', maxsplit=1)
        book_title = f'{id}. {book_name[0].strip()}.txt'
        try:
            file_url = f'https://tululu.org/txt.php?id={id}'
            download_txt(file_url, book_title)
        except requests.exceptions.HTTPError:
            print(f'Отсутствует книга с id = {id}')


if __name__ == '__main__':
    Path("books/").mkdir(parents=True, exist_ok=True)
    get_books()
