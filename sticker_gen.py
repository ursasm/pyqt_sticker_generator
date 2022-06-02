import os
import random
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

    return [f'{prefix}{i:{dl}}'.replace(' ', '0') for i in range(b, e + 1)]


def generate_stickers(model_name: str, sn_list: list):
    if len(sn_list) < 1:
        return
    pdf_file_3 = f'{model_name}_{len(sn_list)}_{random.randrange(1, 10000)}.pdf'

    pdfmetrics.registerFont(TTFont('Arial', resource_path('ArialMT.ttf')))

    can = canvas.Canvas(pdf_file_3)
    can.setPageSize((6 * cm, 4 * cm))

    for sn in sn_list:
        can.setFont('Arial', 8)
        can.drawString(25, 85, f"Модель: {model_name}")
        can.drawString(41, 61, f"S/N: {sn}")
        can.drawImage(resource_path('LTV.jpg'), 20, 16, 22.24 * mm, 10.25 * mm)
        can.drawImage(resource_path('EAC.jpg'), 117, 16, 11.69 * mm, 9.13 * mm)
        can.showPage()

    can.save()
    return pdf_file_3
