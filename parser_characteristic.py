from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_characterstic(ref, browser):
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={'width': 800, 'height': 600},
        locale='ru-RU',
        no_viewport=False
    )

    time_out = 120000

    page = context.new_page()

    page.goto(ref, timeout=time_out)
    page.mouse.wheel(0, 1000)
    try:
        locator = page.locator('[id="DetailDescription"]').locator('[class="detail-dropdown__header"]')
        locator.click(timeout=10000)
        page.wait_for_selector('.detail-dropdown__body article.detail-desc', state="visible", timeout=30000)
        flag = True
    except:
        flag = False

    html = str(page.content())
    page.close()
    context.close()
    soup = BeautifulSoup(html, "html.parser")

    if flag:
        description = BeautifulSoup(str(soup.find('p', {"class": "detail-desc__text detail-desc__text--main"})), "html.parser")
        for _ in range(2):
            description.p.unwrap()

    characterstics = BeautifulSoup(str(soup.find('article', {"class": "detail-full-specs"})).replace('<!-- -->', ""), 'html.parser')

    for tag in characterstics.find_all():
        tag.attrs = {}

    characterstics.article.unwrap()
    while characterstics.find('div') != None:
        characterstics.div.unwrap()
    while characterstics.find('span') != None:
        characterstics.span.unwrap()

    if flag:
        return str(description) + "\n" + str(characterstics)
    else:
        return str(characterstics)


if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print(get_characterstic("https://instrument.ru/gidrouroven-l-10-m-d-8-mm-so-shkaloy-rossiya-sibrtekh-37048/", browser))
        browser.close()
