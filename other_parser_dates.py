from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from parser_characteristic import get_characterstic

def take_info(date):
    for i in range(len(date)):
        curr = BeautifulSoup(str(date[i]), "html.parser")
        date[i] = curr.string

    return date

def parser(rqest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            no_viewport=False
        )

        time_out = 120000

        page = context.new_page()

        while True:
            try:
                page.goto("https://instrument.ru/login/", timeout=time_out)
                page.wait_for_load_state("load", timeout=time_out)
                page.fill("input[type='email']", "login")
                page.fill("input[type='password']", "password")
                page.click("button[type='submit']")
                page.wait_for_url(lambda url: "login" not in url, timeout=time_out)
                break
            except Exception as e:
                print(e)

        while True:
            try:
                page.goto(rqest, timeout=time_out)
                page.wait_for_load_state("networkidle", timeout=time_out)
                break
            except Exception as e:
                print(e)
                page.wait_for_timeout(5000)

        load_more_btn = 'button[class="button button--transparent-gray"]'
        while page.locator(load_more_btn).count() > 0:
            page.click(load_more_btn)
            page.wait_for_timeout(5000)
        html = str(page.content())
        page.close()
        context.close()
        soup = BeautifulSoup(html, "html.parser")

        directory = "обновлённые товары.csv"

        section = soup.find('section', {"class": "wrapper attend-products__swiper wrapper--white wrapper--no-padding"})
        if section:
            section.decompose()

        names = take_info(soup.find_all('a', attrs={"itemprop": "name"}))

        articles = take_info(soup.find_all('div', attrs={"class": "code"}))

        prices = soup.find_all('span', attrs={"itemprop": "price"})[:len(articles) * 2]
        prices = [prices[i] for i in range(len(prices)) if i % 2 == 1]
        for i in range(len(prices)):
            curr = BeautifulSoup(str(prices[i]), "html.parser")
            prices[i] = curr.find('span', itemprop='price').get('content')

        references = soup.find_all('a', attrs={"itemprop": "name"})
        for i in range(len(references)):
            curr = BeautifulSoup(str(references[i]), "html.parser")
            references[i] = [f"https://instrument.ru{curr.find('a', itemprop='name').get('href')}", articles[i]]

        with open(directory, "a", encoding="utf-8") as f:
            i = 0
            count = 1
            index = 100
            for item in references:
                try:
                    characteristic = get_characterstic(item[0], browser)
                except Exception as e:
                    print(f"Характеристики для товара с артикулом {item[1]}")
                    print(e)

                f.write(f'\n"{names[i]}";"мир инструмента";"{articles[i]}";{prices[i]};RUB;"{characteristic}"')

                print(f"Товар №{count} с артикулом {item[1]}!")
                i += 1
                count += 1
                index += 3

        browser.close()
