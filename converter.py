import os
from datetime import datetime
import sys
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json, base64
import webbrowser


def get_pdf_from_html(path, chromedriver='./driver/chromedriver.exe', print_options = {}):
    # запускаем Chrome
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument('--enable-logging')
    driver = webdriver.Chrome(chromedriver, options=webdriver_options)

    # открываем заданный url
    driver.get(path)

    # задаем параметры печати
    calculated_print_options = {
    'landscape': False,
    'displayHeaderFooter': True,
    'printBackground': False,
    'preferCSSPageSize': True,
    }

    calculated_print_options.update(print_options)

    # запускаем печать в pdf файл
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    driver.quit()

    # ответ приходит в base64 - декодируем
    return base64.b64decode(result['data'])


def send_devtools(driver, cmd, params={}):
    resource = f"/session/{driver.session_id}/chromium/send_command_and_get_result"
    print(resource)
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    if response['status']:
        raise Exception(response.get('value'))
    return response.get('value')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: converter.py <html_page_sourse> <filename_to_save>")
        exit()

    result = get_pdf_from_html(sys.argv[1])
    with open(sys.argv[2], 'wb') as file:
        file.write

    # template = os.path.join(os.getcwd(), 'section03.html')
    # print(f'template: {template}')
    # # result = get_pdf_from_html(sys.argv[1])
    # result = get_pdf_from_html(template)
    #
    # output = os.path.join(r'c:\users\nickr\downloads', 'result.pdf')
    # print(f'output name: {output}')
    # with open(output, 'wb') as file:
    #     file.write(result)

    # webbrowser.open_new_tab(output_name)
