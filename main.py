import requests
from pathlib import Path

def get_books():
    for id in range(1, 11):
        filename = f'books/book{id}.text'
        url = f"https://tululu.org/txt.php?id={id}"

        response = requests.get(url)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)

if __name__ == '__main__':
    Path("books/").mkdir(parents=True, exist_ok=True)
    get_books()