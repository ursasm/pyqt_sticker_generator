from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHBoxLayout, QWidget, QGridLayout, \
    QVBoxLayout

from sticker_gen import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Генератор наклеек')
        self.setWindowIcon(QtGui.QIcon(resource_path('LTV_icon.png')))
        self.setGeometry(100, 100, 500, 550)
        self.setMaximumWidth(1500)
        self.setMaximumHeight(1800)

        main_layout = QVBoxLayout()
        sn_layout = QGridLayout()

        # Labels =================================================================================
        self.text_model = QtWidgets.QLabel()
        self.text_model.setText('Введите название модели')
        self.text_model.adjustSize()
        sn_layout.addWidget(self.text_model, 0, 0)

        self.text_prefix = QtWidgets.QLabel()
        self.text_prefix.setText('Введите префикс серийного номера')
        self.text_prefix.adjustSize()
        sn_layout.addWidget(self.text_prefix, 1, 0)

        self.text_sticker_count = QtWidgets.QLabel()
        self.text_sticker_count.setText('Введите диапозон (от и до)')
        self.text_sticker_count.adjustSize()
        sn_layout.addWidget(self.text_sticker_count, 2, 0)

        self.text_sn_length = QtWidgets.QLabel()
        self.text_sn_length.setText('Введите длину серийного номера')
        self.text_sn_length.adjustSize()
        sn_layout.addWidget(self.text_sn_length, 3, 0)

        # Inputs =================================================================================
        self.model_input = QtWidgets.QLineEdit()
        sn_layout.addWidget(self.model_input, 0, 1)

        self.prefix_input = QtWidgets.QLineEdit()
        sn_layout.addWidget(self.prefix_input, 1, 1)

        sub_layout = QHBoxLayout()
        self.from_sn_sticker_input = QtWidgets.QLineEdit()
        self.from_sn_sticker_input.setValidator(QIntValidator(1, 2147483647, self))
        self.from_sn_sticker_input.setText('1')
        sub_layout.addWidget(self.from_sn_sticker_input, 0)

        self.to_sn_sticker_input = QtWidgets.QLineEdit(self)
        self.to_sn_sticker_input.setValidator(QIntValidator(1, 2147483647, self))
        self.to_sn_sticker_input.setText('10')
        sub_layout.addWidget(self.to_sn_sticker_input, 0)
        sn_layout.addLayout(sub_layout, 2, 1)

        self.validator_sn_l = QIntValidator(1, 30, self)
        self.sn_length_input = QtWidgets.QLineEdit()
        self.sn_length_input.setText('3')
        self.sn_length_input.setValidator(self.validator_sn_l)
        sn_layout.addWidget(self.sn_length_input, 3, 1)

        # SPECIFY SN ================================================================================
        ta_layout = QVBoxLayout()
        ta_layout.setContentsMargins(0, 5, 0, 5)
        self.enter_sn_ta = QtWidgets.QCheckBox()
        self.enter_sn_ta.setText('Ввести серийные номера')
        self.enter_sn_ta.adjustSize()
        self.enter_sn_ta.stateChanged.connect(self.check_box_changed)
        ta_layout.addWidget(self.enter_sn_ta, 0)

        self.text_sn_enter_description = QtWidgets.QLabel()
        self.text_sn_enter_description.setText('Введите серийные номера через пробел (можно `;`, `,`)')
        self.text_sn_enter_description.adjustSize()
        ta_layout.addWidget(self.text_sn_enter_description, 0)

        self.sn_text_area = QtWidgets.QPlainTextEdit()
        self.sn_text_area.setReadOnly(True)
        self.sn_text_area.setStyleSheet('background-color:#e1e1e1;')
        ta_layout.addWidget(self.sn_text_area, 2)

        # Button =====================================================================================
        self.gen_btn = QtWidgets.QPushButton(self)
        self.gen_btn.setText('Сгенерировать наклейки')
        self.gen_btn.clicked.connect(self.gen_button_handler)
        ta_layout.addWidget(self.gen_btn, 3)

        # Layouts ====================================================================================
        main_layout.addLayout(sn_layout, 0)
        main_layout.addItem(QtWidgets.QSpacerItem(200, 20))
        main_layout.addLayout(ta_layout, 1)
        self.setLayout(main_layout)

    def gen_button_handler(self):
        try:
            model_name = self.model_input.text()

            if self.enter_sn_ta.isChecked():
                sn_list = split_text(self.sn_text_area.toPlainText())
            else:
                prefix = self.prefix_input.text()

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

            f_name = generate_stickers(
                model_name,
                sn_list
            )
            msg = QMessageBox()
            msg.setWindowTitle("PDF сгенерирован")
            msg.setText(f'Название файла: {f_name}')
            msg.adjustSize()
            msg.setIcon(QMessageBox.Information)

            msg.exec_()
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
