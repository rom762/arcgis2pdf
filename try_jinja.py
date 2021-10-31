import glob
import json
import os
import time
from pathlib import Path
from pprint import pprint
from parse_txt import parse_txt

from jinja2 import Environment, Template, FileSystemLoader
import webbrowser
import random
import pdfkit

"""
    площадь берем из area
    если полигон один заполняем ТОЛЬКО раздел 2, раздел 3 пустая шапка
    если из одной части то заполняется пункт 2
    если частей больше то третий пункт. 
    если полигона два заполняем ТОЛЬКО раздел 3, раздел 2 пустая шапка

    считаем исходы:
    один полигон - 2 раздел
        сколько частей?
            одна часть - 2 раздел 2 пункт 
            две и больше  - 2 раздел 3 пункт
               
    
    два полигона - 3 раздел
        сколько частей?
            одна часть - 3 раздел 2 пункт 
            две и больше  - 3 раздел 3 пункт
        
    вопрос есть ли частей более 2?
    
"""


def generate_empty_values(pattern='&mdash;', length=6) -> list:
    return [pattern for _ in range(length)]


def get_json():
    """временная функция для получения уже спарсенного json"""
    with open(r'c:\Users\nickr\YandexDisk\Coding\Python\Work\Shell_Projects\arcgis2pdf\data\data.json') as f:
        data = json.load(f)
    return data


def make_section_template(
        data, output_name,
        template_name="section_03_template.html",
        output_type='file'):

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    tm = env.get_template(template_name)
    html_filled = tm.render(data=data)
    if output_type == 'file':
        with open(output_name, 'w') as f:
            f.write(html_filled)
        return output_name
    return html_filled


def get_section_data(data, section=2, point=2):
    if section == 1:
        section_data = {
                'title': "ОПИСАНИЕ МЕСТОПОЛОЖЕНИЯ ГРАНИЦ",
                'subtitle': f"Территориальная зона №{data['filename']}",
                'subtitle2': "Раздел 1",
                'characteristics': {
                    'Местоположение объекта': 'г. Москва',
                    """Площадь объекта +/- величина погрешности 
                    определения площади (Р+/- Дельта Р)""": f'{data["area"]}',
                    'Иные характеристики объекта': 'отсутствуют'
                }
        }

    elif section == 2:
        section_data = {2: [generate_empty_values(length=6), ],
                        3: [generate_empty_values(
                            length=6), ]}
        number = 1
        section_data[point] = []
        for ring in data['poligon1']['rings']:
            for coords in ring:
                section_data[point].append(
                    [number, coords[0], coords[1], 'Картометрический метод', '0.10',
                     '-'])
                number += 1
            section_data[point].append(
                [number - len(ring), ring[0][0], ring[0][1],
                 'Картометрический метод', '0.10', '-'])
            section_data[point].append(generate_empty_values(pattern='&nbsp;', length=6))

    elif section == 3:
        section_data = {2: [generate_empty_values(length=8), ],
                        3: [generate_empty_values(length=8), ]
                        }

        r1 = data['poligon1']['rings']
        r2 = data['poligon2']['rings']
        number = 1
        for i, r in enumerate(r1):
            for j, c in enumerate(r):
                c.extend(r2[i][j])
                section_data[point].append([number, *c, 'Картографический', 0.10, '&mdash;'])
                number += 1
            section_data[point].append(
                [number - len(r), r1[i][0][0], r1[i][0][1], r2[i][0][0],
                 r2[i][0][1], 'Картографический', 0.10, '&mdash;'])
            section_data[point].append(['&nbsp;' for _ in range(8)])

    elif section == 4:
        # here will be the image
        pass
    else:
        # what ever?
        pass
    return section_data


def main():
    datadir = os.path.join(os.getcwd(), 'data', 'RES', '*.txt')
    files = glob.glob(datadir)
    for filepath in files:
        if filepath.find("77-01-02-000696") > 0:
            start = time.time()
            # filepath = 'c:\\Users\\nickr\\YandexDisk\\Coding\\Python\\Work\\Shell_Projects\\arcgis2pdf\\data\\RES\\77-01-02-000696.txt'
            # filepath = r'C:\Users\nickr\YandexDisk\Coding\Python\Work\Shell_Projects\arcgis2pdf\data\RES\77-01-01-000173.txt'
            data = parse_txt(filepath=filepath)
            image = data['image']

            first_section_data = get_section_data(data, 1)

            if data['poligon2']['parts'] == 0:
                # заполняем второй раздел.
                # раздел три пустая шапка
                empty_string = generate_empty_values(pattern='&mdash;', length=8)
                third_section_data = {2: [empty_string, ],
                                      3: [empty_string, ]}
                if data['poligon1']['parts'] == 1:
                    # заполняем только второй пункт
                    second_section_data = get_section_data(data, 2, 2)
                elif data['poligon1']['parts'] > 1:
                    second_section_data = get_section_data(data, 2, 3)

            elif data['poligon2']['parts'] == 1:
                # заполняем третий раздел
                # раздел два пустая шапка
                empty_string = generate_empty_values(pattern='&mdash;', length=6)
                second_section_data = {2: [empty_string, ],
                                       3: [empty_string, ]}
                third_section_data = get_section_data(data, 3, 2)

            elif data['poligon2']['parts'] > 1:
                empty_string = generate_empty_values(pattern='&mdash;', length=6)
                second_section_data = {2: [empty_string, ],
                                       3: [empty_string, ]}
                third_section_data = get_section_data(data, 3, 3)

            path2wkthmltopdf = r'c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path2wkthmltopdf)

            first_section_html = make_section_template(data=first_section_data, output_name='section01.html', template_name='section_01_template.html')
            second_section_html = make_section_template(data=second_section_data, output_name='section02.html', template_name='section_02_template.html')
            third_section_html = make_section_template(data=third_section_data, output_name='section03.html', template_name='section_03_template.html')
            fourth_section_html = make_section_template(data={'image': image}, output_name='section04.html', template_name='section_04_template.html')

            sections = [
                first_section_html,
                second_section_html,
                third_section_html,
                fourth_section_html
            ]
            options = {
                'page-size': 'A4',
                'margin-top': '0.3in',
                'margin-right': '0.3in',
                'margin-bottom': '0.3in',
                'margin-left': '0.3in',
                'page-offset': 1,
            }
            final_file_name = data['filename'] + '.pdf'
            output_path = os.path.join(os.getcwd(), 'pdf', final_file_name)
            pdfkit.from_file(input=sections, output_path=output_path, configuration=config, options=options)
            end = time.time()
            print(f'{final_file_name} is done for {start - end}!')
            webbrowser.open_new_tab(output_path)


if __name__ == "__main__":
    main()
