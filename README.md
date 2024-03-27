# online-library

Cкрипт скачивает книги с сайта [tululu.org](https://tululu.org/) в папку на пк. У каждой книги можно посмотреть название, автора, ссылку на скачивание, комментарии и жанры, а также скачать обложку. 

## Как установить

Python3 должен быть уже установлен. Склонируйте репозиторий на пк, а затем используйте pip для установки зависимостей:

```python
pip install -r requirements.txt
```

## Как запустить

Убедитесь, что в терминале находитесь в директории кода и ознакомьтесь со справкой по запуску кода, используя команду:

```python
python .\parse_tululu.py -h
```
_Пример вывода:_

```
usage: parse_tululu.py [-h] start_id end_id

Скачивает книги

positional arguments:
  start_id    C какой станицы скачивать
  end_id      По какую страницу скачивать
```

Для запуска скрипта укажите позиционные аргументы, например:

```python
python .\parse_tululu.py 20 30
```

После запуска скрипта скачается библиотека и обложки к книгам. В консоле выведутся заголовки и авторы книг, а также идентификаторы книг, которые невозможно скачать. 

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).