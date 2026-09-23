import logging
import time

from parser_dates import parser

mass = [
        # 'https://instrument.ru/catalog/prochiy-instrument/zamki/?filter=product_status-is-true',
        # 'https://instrument.ru/catalog/prochiy-instrument/gorelki-gazovye/?filter=product_status-is-true',
        # 'https://instrument.ru/catalog/prochiy-instrument/izdeliya-kanatno-verevochnye/?filter=product_status-is-true',
        # 'https://instrument.ru/catalog/prochiy-instrument/instrument-dlya-prochistki-trub/?filter=product_status-is-true',
        #
        # 'https://instrument.ru/catalog/prochiy-instrument/kleevye-sterzhni/?filter=product_status-is-true',
        # 'https://instrument.ru/catalog/prochiy-instrument/lampy-payalnye-kerosinovye/?filter=product_status-is-true',
        # 'https://instrument.ru/catalog/prochiy-instrument/lestnitsy/?filter=product_status-is-true',
        # '',
        #
        # '',
        # '',
        # '',
        # '',
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
