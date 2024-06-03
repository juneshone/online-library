import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from pathlib import Path


def on_reload(books, template):
    pages_count = 10
    book_pages = list(chunked(books, pages_count))

    start_page_number = 1
    for page, books in enumerate(book_pages, start_page_number):
        columns = 2
        book_columns = list(chunked(books, columns))
        rendered_page = template.render(
            book_columns=book_columns,
            page=page,
            pages=len(book_pages),
        )

        with open((Path('pages/') / f'index{page}.html'), 'w', encoding='utf-8') as index:
            index.write(rendered_page)


def main():
    os.makedirs('pages/', mode=0o666, exist_ok=True)

    parser = argparse.ArgumentParser(
        description='Зазружает медиа в веб-интерфейс'
    )
    parser.add_argument(
        '--template_path',
        default='templates',
        help='Путь к шаблону HTML'
    )
    parser.add_argument(
        '--template',
        default='template.html',
        help='Наименование шаблона HTML'
    )
    args = parser.parse_args()
    env = Environment(
        loader=FileSystemLoader(args.template_path),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(args.template)

    with open('books.json', 'r', encoding='utf-8') as books_json:
        books = json.loads(books_json.read())

    on_reload(books, template)

    server = Server()
    server.watch('template.html', main)
    server.serve(root='.')


if __name__ == '__main__':
    main()
