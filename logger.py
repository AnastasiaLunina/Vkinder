import time
import datetime
import os


def logger(file_name):
    def _loger(out_func):
        def inner_func(*args, **kwargs):
            start = time.time()
            result = out_func(*args, **kwargs)
            path = f'{os.getcwd()}/{file_name}'
            data = f'--- Function name: {out_func.__name__}, ' \
                   f'Arguments: {args} {kwargs}, ' \
                   f'Calling date: {datetime.date.today()}, ' \
                   f'Time: {time.time() - start}, ' \
                   f'Result: {result}'
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
