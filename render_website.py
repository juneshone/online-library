import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from pathlib import Path


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json', 'r') as books_file:
        books = json.load(books_file)

    book_pages = list(chunked(books, 10))

    for page, books in enumerate(book_pages, 1):
        book_columns = list(chunked(books, 2))
        rendered_page = template.render(
            book_columns=book_columns,
            images=Path('../') / 'images/',
            books=Path('../') / 'books/',
            page=page,
            pages=len(book_pages),
        )

        with open((Path('pages/') / f'index{page}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages/', mode=0o666, exist_ok=True)
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
