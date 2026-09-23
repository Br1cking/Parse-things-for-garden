import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from parser_characteristic import get_characterstic
from parser_images import get_images

def take_info(date):
    for i in range(len(date)):
        curr = BeautifulSoup(str(date[i]), "html.parser")
        date[i] = curr.string

    return date

def parser(rqest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            no_viewport=False
        )

        time_out = 120000

        page = context.new_page()

        page.goto("https://instrument.ru/login/", timeout=time_out)
        page.wait_for_load_state("load", timeout=time_out)

        page.fill("input[type='email']", "login")
        page.fill("input[type='password']", "password")
        page.click("button[type='submit']")

        page.wait_for_url(lambda url: "login" not in url, timeout=time_out)

        while True:
            try:
                page.goto(rqest, timeout=time_out)
                page.wait_for_load_state("networkidle", timeout=time_out)
                break
            except Exception as e:
                page.wait_for_timeout(5000)

        load_more_btn = 'button[class="button button--transparent-gray"]'
        while page.locator(load_more_btn).count() > 0:
            page.click(load_more_btn)
            page.wait_for_timeout(5000)

        html = str(page.content())
        page.close()
        context.close()
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string
        directory = f"Товары\\{title}"
        os.mkdir(directory)

        directory_for_photo = f"{directory}\\photo"
        os.mkdir(directory_for_photo)

        section = soup.find('section', {"class": "wrapper attend-products__swiper wrapper--white wrapper--no-padding"})
        if section:
            section.decompose()

        names = take_info(soup.find_all('a', attrs={"itemprop": "name"}))

        articles = take_info(soup.find_all('div', attrs={"class": "code"}))

        count = len(articles)
        print(count)

        prices = soup.find_all('span', attrs={"itemprop": "price"})[:len(articles) * 2]
        prices = [prices[i] for i in range(len(prices)) if i % 2 == 1]
        for i in range(len(prices)):
            curr = BeautifulSoup(str(prices[i]), "html.parser")
            prices[i] = curr.find('span', itemprop='price').get('content')

        references = soup.find_all('a', attrs={"itemprop": "name"})
        for i in range(len(references)):
            curr = BeautifulSoup(str(references[i]), "html.parser")
            references[i] = [f"https://instrument.ru{curr.find('a', itemprop='name').get('href')}", articles[i]]

        with open(f"{directory}\\{title}.csv", "w", encoding="utf-8") as f:
            f.write('"name : Название";"supplier : Поставщик";"article : Артикул";"price : Цена";"currency : Валюта";"body : Описание"\n')
            i = 0
            count = 1
            index = 100
            for item in references:
                try:
                    characteristic = get_characterstic(item[0], browser)
                except Exception as e:
                    print(f"Характеристики для товара с артикулом {item[1]}")
                    print(e)

                f.write(f'"{names[i]}";"мир инструмента";"{articles[i]}";{prices[i]};RUB;"{characteristic}"\n')

                try:
                    get_images(item, directory_for_photo, browser, index)
                except Exception as e:
                    print(f"Фото для товара с артикулом {item[1]}")
                    print(e)

                print(f"Товар №{count} с артикулом {item[1]}!")
                i += 1
                count += 1
                index += 3

        browser.close()
