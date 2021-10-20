from jinja2 import Environment, Template, FileSystemLoader
import webbrowser
import random
import pdfkit

first_section_data = {
    'title': "ОПИСАНИЕ МЕСТОПОЛОЖЕНИЯ ГРАНИЦ",
    'subtitle': """Особо охраняемая природная территория 
    регионального значения "Ландшафтный заказник "Долина реки Сходни в 
    районе Молжаниновский" (наименование объекта, 
    местоположение границ которого описано (далее - объект)""",
    'subtitle2': "Раздел 1",
    'characteristics': {
        'Местоположение объекта': 'г. Москва',
        """Площадь объекта +/- величина погрешности 
        определения площади (Р+/- Дельта Р)""": '181787 кв.м ± 86 кв.м',
        'Иные характеристики объекта': """На территории "Ландшафтного заказника "Долина 
    реки Сходни в районе Молжаниновский" 
    устанавливаются режимы охраны и использования 
    территории, запрещающие или допускающие 
    проведение тех или иных мероприятий и работ в 
    установленных границах отдельных 
    функциональных зон ООПТ. 
    Описания режимов особой охраны особо охраняемой 
    природной территории регионального значения 
    "Ландшафтного заказника "Долина реки Сходни в 
    районе Молжаниновский" приводятся в 
    Постановлении Правительства Москвы от 20.07.2020 
    №1000-ПП "Об особо охраняемой природной 
    территории регионального значения "Ландшафтный 
    заказник "Долина реки Сходни в районе 
    Молжаниновский". 
    Помимо требований режимов особой охраны особо 
    охраняемой природной территории регионального 
    значения "Ландшафтный заказник "Долина реки 
    Сходни в районе Молжаниновский", так же должны 
    соблюдаться требования, установленные 
    федеральными законами, иными нормативными 
    правовыми актами Российской Федерации, законами 
    города Москвы, иными нормативными правовыми 
    актами города Москвы"""
    }
}
second_section_data = [tuple([random.randint(28000, 29000) for _ in range(2)] + [random.randint(-9500, -9300) for _ in range(2)]) for j in range(100)]


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


def main():
    path2wkthmltopdf = r'c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path2wkthmltopdf)

    first_section_html = make_section_template(data=first_section_data, output_name='section01.html', template_name='section_01_template.html')
    second_section_html = make_section_template(data=second_section_data, output_name='section_03.html', template_name='section_03_template.html')

    pdfkit.from_file([first_section_html, second_section_html], "result.pdf", configuration=config)
    webbrowser.open_new_tab('result.html')


if __name__ == "__main__":
    main()
