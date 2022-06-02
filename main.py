from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

import sys
from sticker_gen import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Генератор наклеек')
        self.setGeometry(100, 100, 550, 530)
        self.setFixedSize(self.size())

        # Labels ====================================================
        self.text_model = QtWidgets.QLabel(self)
        self.text_model.setText('Введите название модели')
        self.text_model.move(20, 37)
        self.text_model.adjustSize()

        self.text_prefix = QtWidgets.QLabel(self)
        self.text_prefix.setText('Введите префикс серийного номера')
        self.text_prefix.move(20, 77)
        self.text_prefix.adjustSize()

        self.text_sticker_count = QtWidgets.QLabel(self)
        self.text_sticker_count.setText('Введите диапозон (от и до)')
        self.text_sticker_count.move(20, 117)
        self.text_sticker_count.adjustSize()

        self.text_sn_length = QtWidgets.QLabel(self)
        self.text_sn_length.setText('Введите длину серийного номера')
        self.text_sn_length.move(20, 157)
        self.text_sn_length.adjustSize()

        # Inputs ====================================================
        self.model_input = QtWidgets.QTextEdit(self)
        self.model_input.move(300, 20)
        self.model_input.setFixedWidth(220)
        self.model_input.setFixedHeight(30)

        self.prefix_input = QtWidgets.QTextEdit(self)
        self.prefix_input.move(300, 65)
        self.prefix_input.setFixedWidth(220)

        self.from_sn_sticker_input = QtWidgets.QLineEdit(self)
        self.from_sn_sticker_input.move(300, 110)
        self.from_sn_sticker_input.setFixedWidth(100)
        self.from_sn_sticker_input.setValidator(QIntValidator(1, 2147483647, self))
        self.from_sn_sticker_input.setText('1')

        self.to_sn_sticker_input = QtWidgets.QLineEdit(self)
        self.to_sn_sticker_input.move(420, 110)
        self.to_sn_sticker_input.setFixedWidth(100)
        self.to_sn_sticker_input.setValidator(QIntValidator(1, 2147483647, self))
        self.to_sn_sticker_input.setText('10')

        self.validator_sn_l = QIntValidator(1, 30, self)
        self.sn_length_input = QtWidgets.QLineEdit(self)
        self.sn_length_input.move(300, 150)
        self.sn_length_input.setText('3')
        self.sn_length_input.setFixedWidth(220)
        self.sn_length_input.setValidator(self.validator_sn_l)

        # SPECIFY SN ====================================================================
        self.enter_sn_ta = QtWidgets.QCheckBox(self)
        self.enter_sn_ta.move(20, 210)
        self.enter_sn_ta.setText('Ввести серийные номера')
        self.enter_sn_ta.adjustSize()
        self.enter_sn_ta.stateChanged.connect(self.check_box_changed)

        self.text_sn_enter_description = QtWidgets.QLabel(self)
        self.text_sn_enter_description.setText('Введите серийные номера через пробел (можно `;`, `,`)')
        self.text_sn_enter_description.move(20, 235)
        self.text_sn_enter_description.adjustSize()

        self.sn_text_area = QtWidgets.QPlainTextEdit(self)
        self.sn_text_area.move(20, 260)
        self.sn_text_area.resize(500, 200)
        self.sn_text_area.setReadOnly(True)
        self.sn_text_area.setStyleSheet('background-color:#e1e1e1;')

        # Button ========================================================================
        self.gen_btn = QtWidgets.QPushButton(self)
        self.gen_btn.move(180, 480)
        self.gen_btn.setText('Сгенерировать наклейки')
        self.gen_btn.setFixedWidth(200)
        self.gen_btn.clicked.connect(self.gen_button_handler)

    def gen_button_handler(self):
        try:
            model_name = self.model_input.toPlainText()

            if self.enter_sn_ta.isChecked():
                sn_list = split_text(self.sn_text_area.toPlainText())
            else:
                prefix = self.prefix_input.toPlainText()

                begin = self.from_sn_sticker_input.text()
                if begin == '':
                    raise Exception('Введите число - начало диапазона серийных номеров')
                b = int(begin)

                end = self.to_sn_sticker_input.text()
                if end == '':
                    raise Exception('Введите число - конец диапазона серийных номеров')
                e = int(end)

                size = self.sn_length_input.text()
                if size == '':
                    raise Exception('Введите длину серийного номера')
                sz = int(size)

                sn_list = generate_sn(prefix, b, e, sz)

            generate_stickers(
                model_name,
                sn_list
            )
            print(sn_list)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Что можно было сделать не так?")
            msg.setText(str(e))
            msg.adjustSize()
            msg.setIcon(QMessageBox.Warning)

            msg.exec_()

    def check_box_changed(self, d):
        if self.enter_sn_ta.isChecked():
            self.from_sn_sticker_input.setReadOnly(True)
            self.from_sn_sticker_input.setStyleSheet('background-color:#e1e1e1;')

            self.to_sn_sticker_input.setReadOnly(True)
            self.to_sn_sticker_input.setStyleSheet('background-color:#e1e1e1;')

            self.sn_length_input.setReadOnly(True)
            self.sn_length_input.setStyleSheet('background-color:#e1e1e1;')

            self.prefix_input.setReadOnly(True)
            self.prefix_input.setStyleSheet('background-color:#e1e1e1;')

            self.sn_text_area.setReadOnly(False)
            self.sn_text_area.setStyleSheet('background-color: white;')
        else:
            self.from_sn_sticker_input.setReadOnly(False)
            self.from_sn_sticker_input.setStyleSheet('background-color:white;')

            self.to_sn_sticker_input.setReadOnly(False)
            self.to_sn_sticker_input.setStyleSheet('background-color:white;')

            self.sn_length_input.setReadOnly(False)
            self.sn_length_input.setStyleSheet('background-color:white;')

            self.prefix_input.setReadOnly(False)
            self.prefix_input.setStyleSheet('background-color: white;')

            self.sn_text_area.setReadOnly(True)
            self.sn_text_area.setStyleSheet('background-color:#e1e1e1;')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
