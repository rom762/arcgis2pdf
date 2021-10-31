from weasyprint import HTML

HTML('section03.html').write_pdf('result.pdf')
