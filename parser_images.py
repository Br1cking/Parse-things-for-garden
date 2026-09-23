import requests
from bs4 import BeautifulSoup


def get_images(ref, path, browser, index):
    page = browser.new_page()

    time_out = 15000

    while True:
        try:
            page.goto(ref[0], timeout=time_out)
            page.wait_for_load_state("networkidle", timeout=time_out)
            break
        except Exception:
            page.wait_for_timeout(5000)

    html = str(page.content())
    page.close()
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all('source', attrs={"type":"image/webp"})[:3]

    if len(images) >= 1:
        for image in images:
            curr = BeautifulSoup(str(image), "html.parser")
            part_url = curr.find('source').get('srcset')
            url = f"https://instrument.ru{part_url}"
            response = requests.get(url)
            filename = f"{path}\\{ref[1]}({index}).webp"
            filename_2 = f"Товары\\Фото для загрузки\\{ref[1]}({index}).webp"
            index += 1

            with open(filename, 'wb') as f:
                f.write(response.content)

            with open(filename_2, 'wb') as f:
                f.write(response.content)
