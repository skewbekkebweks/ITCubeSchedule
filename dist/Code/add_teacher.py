from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Code.notification import signal
from Design.add_teacher import Ui_AddTeacher


class AddTeacher(Ui_AddTeacher, QMainWindow):
    def __init__(self, connect, admin) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.admin = admin
        self.name_edit.textEdited.connect(self.name_changed)
        self.surname_edit.textEdited.connect(self.surname_changed)
        self.patronymic_edit.textEdited.connect(self.patronymic_changed)
        self.cor_name = self.cor_surname = self.cor_patronymic = False
        self.pushButton.setEnabled(0)
        self.pushButton.clicked.connect(self.check)

    def open_btn(self):
        if self.cor_name and self.cor_surname and self.cor_patronymic:
            self.pushButton.setEnabled(1)

    def check(self):
        name = self.surname_edit.text() + ' ' + \
               self.name_edit.text() + ' ' + self.patronymic_edit.text()
        cursor = self.connect.cursor()
        command = f'select count() ' \
                  f'from teachers ' \
                  f'where name = \'{name}\''
        res = cursor.execute(command).fetchone()[0]
        if res == 0:
            num_of_office = int(self.admin.office_box.currentText().split('. ')[0])
            command = f'select id ' \
                      f'from offices ' \
                      f'where number = \'{num_of_office}\''
            office = cursor.execute(command).fetchone()[0]
            command = f'insert into ' \
                      f'teachers(name, office) values(\'{name}\', {office})'
            cursor.execute(command)
            self.connect.commit()
            self.admin.cur_teachers_change()
            signal()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Преподаватель с таким именем существует',
                                 QMessageBox.Ok)

    def name_changed(self) -> None:
        """Проверка на правильность написания имени"""
        res = self.fio_check(self.name_edit.text())
        self.name_edit.setStyleSheet('border-radius: 2px;\n'
                                     'border-width: 1px;\n'
                                     'border-style: solid;\n'
                                     'border-color: ' + res + ';')
        if res == '':
            self.name_edit.setStyleSheet('')
        self.cor_name = True if res == 'green' else False
        self.open_btn()

    def surname_changed(self) -> None:
        """Проверка на правильность написания фамилии"""
        res = self.fio_check(self.surname_edit.text())
        self.surname_edit.setStyleSheet('border-radius: 2px;\n'
                                        'border-width: 1px;\n'
                                        'border-style: solid;\n'
                                        'border-color: ' + res + ';')
        if res == '':
            self.surname_edit.setStyleSheet('')
        self.cor_surname = True if res == 'green' else False
        self.open_btn()

    def patronymic_changed(self) -> None:
        """Проверка на правильность написания отчества"""
        res = self.fio_check(self.patronymic_edit.text())
        self.patronymic_edit.setStyleSheet('border-radius: 2px;\n'
                                           'border-width: 1px;\n'
                                           'border-style: solid;\n'
                                           'border-color: ' + res + ';')
        if res == '':
            self.patronymic_edit.setStyleSheet('')
        self.cor_patronymic = True if res == 'green' else False
        self.open_btn()

    @staticmethod
    def fio_check(text) -> str:
        """Проверка на правильность написания ФИО"""
        if text:
            if text.replace('-', '').isalpha() and '--' not in text:
                return 'green'
            else:
                if not text.replace('-', '').isalpha():
                    return 'red'
                else:
                    return 'red'
        else:
            return ''
