import logging
import time

from parser_dates import parser

mass = [
        'https://instrument.ru/catalog/izmeritelnyy-instrument/dalnomery/?filter=product_status-is-true',
       ]

start_time = time.time()
for element in mass:
    try:
        parser(element)
    except Exception as e:
        logging.error(f"Катастрофическая ошибка для {element}: {e}")

    if element == mass[-1]:
        break

    time.sleep(10)

print(time.localtime(start_time))
print(time.localtime(time.time()))
