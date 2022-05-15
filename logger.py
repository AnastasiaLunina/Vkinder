import time
import datetime
import os


def logger(file_name):
    def _loger(out_func):
        def inner_func(*args, **kwargs):
            start = time.time()
            result = out_func(*args, **kwargs)
            path = f'{os.getcwd()}/{file_name}'
            data = f'--- Имя функции: {out_func.__name__}, ' \
                   f'Аргументы функции: {args} {kwargs}, ' \
                   f'Дата вызова: {datetime.date.today()}, ' \
                   f'Время выполнения: {time.time() - start}, ' \
                   f'Результат выполнения: {result}'
            with open(path, 'a', encoding='utf-8') as f:
                f.write(data + '\n')
            return result

        return inner_func

    return _loger


def error_func(error: dict):
    print('Error')
    data = f'Error ID: {error.get("error_code")}, ' \
           f'Error message: {error.get("error_msg")},' \
           f'Datetime: {datetime.datetime.now()}'
    path_ = f'{os.getcwd()}/logfile_error.txt'
    with open(path_, 'a', encoding='utf-8') as f:
        f.write(data + '\n')
