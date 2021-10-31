import glob
import os
import sys
import time
from decimal import Decimal
from pprint import pprint

from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import \
    FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from parse_txt import parse_txt
from try_jinja import get_section_data


def get_data():
    datadir = os.path.join(os.getcwd(), 'data', 'RES', '*.txt')
    files = glob.glob(datadir)
    for filepath in files:
        if filepath.find("77-01-02-000696") > 0:
            start = time.time()
            # filepath = 'c:\\Users\\nickr\\YandexDisk\\Coding\\Python\\Work\\Shell_Projects\\arcgis2pdf\\data\\RES\\77-01-02-000696.txt'
            # filepath = r'C:\Users\nickr\YandexDisk\Coding\Python\Work\Shell_Projects\arcgis2pdf\data\RES\77-01-01-000173.txt'
            data = parse_txt(filepath=filepath)
            image = data['image']
    return data


def main():
    data = get_data()
    pprint(data)
    doc: Document = Document()
    page: Page = Page()
    doc.append_page(page)

    layout: PageLayout = SingleColumnLayout(page)

    first_section_data = get_section_data(data, 1)
    layout.add(Paragraph(first_section_data['title']))
    layout.add(Paragraph(first_section_data['subtitle']))
    layout.add(Paragraph(first_section_data['subtitle2']))

    layout.add(
        FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=6)
            .add(TableCell(Paragraph("Сведения об объекте"), col_span=3))
            .add(TableCell(Paragraph(""), col_span=3))
            .add(Paragraph("№ п.п"))
            .add(Paragraph("Характеристики объекта"))
            .add(Paragraph("Описание характеристик"))
            for ch,v in first_section_data['characteristics']:
                .add
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2)))
    with open("output.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, doc)


if __name__ == "__main__":
	main()
