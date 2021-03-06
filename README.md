# flibusta-dl

flibusta-dl - download books from flibusta


## Installation

### Requirements
* Python 3.6 and up

### Installation from source
```
$ git clone https://github.com/andriyor/flibusta-dl.git
$ cd flibusta-dl
$ python3 setup.py install
```

## Usage

### `--help`

```
$ flibusta-dl --help
Usage: flibusta-dl [OPTIONS] INFILE

Options:
  -of, --output_folder TEXT       путь к папке в которую будут сохранятся
                                  книги
  --min-filesize                  загрузка книг с минимальным размером
  --max-filesize                  загрузка книг  с максимальным размером
  -o, --oldest                    загрузка самых старых книг
  -n, --newest                    загрузка самых новых книг
  -l, --litres                    приоритет загрузки по litres
  -r, --rating                    приоритет загрузки по оценке
  -ff, --file_format [fb2|epub|mobi]
                                  формат книг
  --sfn                           имя файла такое же как при загрузке с сайта
  --asy                           асинхронная загрузка книг
  --help                          Show this message and exit.
```
### Example usage


```
$ cat books.txt
автостопом по галактике
сто лет одиночества
Красное и чёрное
Война и мир
Старик и море
Война миров
Моби Дик
Преступление и наказание
```


```
$ flibusta-dl books.txt -r -ff=epub
книга автостопом по галактике загружена размер - 343.6 kB
книга сто лет одиночества загружена размер - 543.2 kB
книга Красное и чёрное загружена размер - 237.6 kB
книга Война и мир загружена размер - 2.6 MB
книга Старик и море загружена размер - 192.7 kB
книга Война миров загружена размер - 258.5 kB
книга Моби Дик загружена размер - 69.4 kB
книга Преступление и наказание загружена размер - 62.9 kB
100%|████████████████████████████| 8/8 [00:08<00:00,  1.02s/it]
всего загружено 8 книг из 8 общим размером - 4.3 MB за 9 секунд
```

```
$ flibusta-dl books.txt -r -ff=epub --asy
книга автостопом по галактике загружена размер - 343.6 kB
книга сто лет одиночества загружена размер - 543.2 kB
книга Красное и чёрное загружена размер - 237.6 kB
книга Война и мир загружена размер - 2.6 MB
книга Старик и море загружена размер - 192.7 kB
книга Война миров загружена размер - 258.5 kB
книга Моби Дик загружена размер - 69.4 kB
книга Преступление и наказание загружена размер - 62.9 kB
всего загружено 8 книг из 8 общим размером - 4.3 MB за 3 секунды
```

## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```
