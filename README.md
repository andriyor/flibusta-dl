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
  -o, --output_folder TEXT        путь к папке в которую будут сохранятся
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
  --help                          Show this message and exit.
```
### Example usage


## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```
