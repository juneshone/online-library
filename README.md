# online-library

Cкрипт скачивает книги с сайта [tululu.org](https://tululu.org/) в папку на пк. У каждой книги можно посмотреть название, автора, ссылку на скачивание, комментарии и жанры, а также скачать обложку. Загруженные файлы можно вывести в веб-интефейсе.

## Как установить

Python3 должен быть уже установлен. Склонируйте репозиторий на пк, а затем используйте pip для установки зависимостей:

```python
pip install -r requirements.txt
```

## Как запустить

Убедитесь, что в терминале находитесь в директории кода и ознакомьтесь со справкой по запуску кода, используя команды:

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

```python
python .\parse_tululu_category.py -h
```
_Пример вывода:_

```
usage: parse_tululu_category.py [-h] [--start_page START_PAGE] [--end_page END_PAGE] [--dest_folder DEST_FOLDER] [--skip_imgs] [--skip_txt]
                                                                                                                                           
Парсинг книг с сайта tululu.org                                                                                                            
                                                                                                                                           
options:                                                                                                                                   
  -h, --help            show this help message and exit                                                                                    
  --start_page START_PAGE                                                                                                                  
                        Номер первой страницы для скачивани книг                                                                           
  --end_page END_PAGE   Номер последней страницы для скачивани книг                                                                        
  --dest_folder DEST_FOLDER                                                                                                                
                        Путь к каталогу с результатами парсинга                                                                            
  --skip_imgs           Не скачивать картинки                                                                                              
  --skip_txt            Не скачивать книги  
```
Для запуска скриптов укажите позиционные аргументы.

_Пример запуска скриптов:_

```python
python .\parse_tululu.py 20 30
```

```
python .\parse_tululu_category.py --start_page 700 --dest_folder C:\Users\user\Desktop\folder --skip_imgs
```

После запуска скрипта `parse_tululu.py` скачается библиотека и обложки к книгам, а в консоле скрипта выведутся заголовки и авторы книг, а также идентификаторы книг, которые невозможно скачать. После запуска скрипта `parse_tululu_category.py` скачиваются обложки и книги из категории фантастики по заданному пути.

## Загрузка книг в веб-интефейс

Перед загрузкой книг в веб-интерфейсе ознакомьтесь со справкой по запуску кода, используя команду:

```python
python .\render_website.py -h
```

_Пример вывода:_

```
usage: render_website.py [-h] [--template_path TEMPLATE_PATH] [--template TEMPLATE]

Зазружает медиа в веб-интерфейс

options:
  -h, --help            show this help message and exit
  --template_path TEMPLATE_PATH
                        Путь к шаблону HTML
  --template TEMPLATE   Наименование шаблона HTML
```

Для загрузки книг в веб-интерфейс укажите позиционные аргументы (по умолчанию папка `templates` и шаблон `template.html`):

```python
python .\render_website.py --template_path 'templates' --template 'template.html'
```

Страницы с книгами сохраняются в директорию `.\pages` и открываются с помощью браузера. Сайт доступен по [адресу](http://127.0.0.1:5500/pages/index1.html).
Пример опубликованного сайта находится [здесь](https://juneshone.github.io/online-library/pages/index5.html).

![library](https://github.com/juneshone/online-library/blob/master/static/library.png)

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).