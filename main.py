import os
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


def main():
    for id in range(1, 11):
        book_url = f"https://tululu.org/b{id}/"
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        book_name = soup.find('h1').text.split('::', maxsplit=1)
        book_title = f'{id}. {book_name[0].strip()}.txt'

        book_file_url = f'https://tululu.org/txt.php?id={id}'
        file_response = requests.get(book_file_url)
        file_response.raise_for_status()

        comments_texts = soup.find_all(class_="texts")
        try:
            check_for_redirect(file_response)
            image_url = soup.find(class_="bookimage").find('img')['src']
            full_image_url = urljoin('https://tululu.org/', image_url)
            download_image(full_image_url)
            download_txt(book_file_url, book_title)

            print(book_title)
            books_genres = soup.find('span', class_="d_book").find_all('a')
            print([genre.text for genre in books_genres])

            for comment in comments_texts:
                book_comment = comment.find('span').text
                print(book_comment)
        except requests.exceptions.HTTPError:
            print(f'Отсутствует книга с id = {id}')


if __name__ == '__main__':
    Path("books/").mkdir(parents=True, exist_ok=True)
    Path("images/").mkdir(parents=True, exist_ok=True)
    main()
