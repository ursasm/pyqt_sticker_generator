import random

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def split_text(serial_numbers: str):
    serial_numbers = serial_numbers.replace('\n', ' ')
    serial_numbers = serial_numbers.replace(',', ' ')
    serial_numbers = serial_numbers.replace(';', ' ')
    while '  ' in serial_numbers:
        serial_numbers = serial_numbers.replace('  ', ' ')

    return serial_numbers.split(' ')


def generate_sn(prefix: str, b: int, e: int, str_length: int):
    if e < b:
        b, e = e, b
    dl = str_length - len(prefix)
    if dl < len(str(e)):
        dl = len(str(e))

    # res = []
    #
    # for i in range(b, e + 1):
    #     res.append(f'{prefix}{i}')
    #
    # return res
    return [f'{prefix}{i:{dl}}'.replace(' ', '0') for i in range(b, e + 1)]


def generate_stickers(model_name: str, sn_list: list):
    if len(sn_list) < 1:
        return
    pdf_file_3 = f'{model_name}_{len(sn_list)}_{random.randrange(1, 10000)}.pdf'

    pdfmetrics.registerFont(TTFont('Arial', 'ArialMT.ttf'))

    can = canvas.Canvas(pdf_file_3)
    can.setPageSize((6 * cm, 4 * cm))

    for sn in sn_list:
        can.setFont('Arial', 8)
        can.drawString(25, 85, f"Модель: {model_name}")
        can.drawString(41, 61, f"S/N: {sn}")
        can.drawImage('LTV.jpg', 20, 16, 22.24 * mm, 10.25 * mm)
        can.drawImage('EAC.jpg', 117, 16, 11.69 * mm, 9.13 * mm)
        can.showPage()

    can.save()
