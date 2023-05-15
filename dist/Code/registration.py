from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Code.work_with_login_password import WorkWithLoginPassword
from Design.registration import Ui_Registration
from Code.notification import signal


class Registration(Ui_Registration, QMainWindow, WorkWithLoginPassword):
    def __init__(self, connect) -> None:
        super().__init__()
        self.setupUi(self)  # подключение к дизайну
        self.connect = connect  # подключение к БД
        self.name_edit.textEdited.connect(self.name_changed)
        self.surname_edit.textEdited.connect(self.surname_changed)
        self.patronymic_edit.textEdited.connect(self.patronymic_changed)
        self.login_edit.textEdited.connect(self.login_changed)
        self.password_edit.textEdited.connect(self.password_changed)
        # флажки для разблоикровки кнопки сохранения
        self.cor_name = self.cor_surname = self.cor_patronymic = \
            self.cor_login = self.cor_password = False
        self.pushButton.clicked.connect(self.check)
        self.hide_password_btn.clicked.connect(self.hide_show_password)
        self.open_btn()

    def hide_show_password(self):
        """Скрытие или открытие пароля"""
        if self.hide_password_btn.text() == 'Скрыть пароль':
            self.hide_password_btn.setText('Показать пароль')
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.hide_password_btn.setText('Скрыть пароль')
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)

    def check(self) -> None:
        """Регистрация преподавателя"""
        name = ' '.join(
            [self.surname_edit.text(), self.name_edit.text(), self.patronymic_edit.text()])
        cursor = self.connect.cursor()
        command = f'select count(login) ' \
                  f'from teachers ' \
                  f'where login = \'{self.login_edit.text()}\''
        res = cursor.execute(command).fetchone()
        # проверка на занятость выбранного логина
        if res[0]:
            QMessageBox.critical(self, 'Ошибка',
                                 'Профиль с таким логином уже существует', QMessageBox.Ok)
        else:
            command = f'select login, password ' \
                      f'from teachers ' \
                      f'where name = \'{name}\''
            res = cursor.execute(command).fetchone()  # уже зарегистрированные логин и пароль учителя
            if res == (None, None):
                # добавления логина и пароля преподавателя
                command = f'update teachers ' \
                          f'set login = \'{self.login_edit.text()}\', ' \
                          f'password = \'{self.password_edit.text()}\' ' \
                          f'where name = \'{name}\''
                cursor.execute(command)
                self.connect.commit()
                signal()
                self.close()
            elif res is None:
                QMessageBox.critical(self, 'Ошибка',
                                     'Преподавателя с таким именем не существует',
                                     QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Ошибка',
                                     'Преподаватель уже зарегистрирован', QMessageBox.Ok)

    def name_changed(self) -> None:
        """Проверка на правильность написания имени"""
        res = self.fio_check(self.name_edit.text())
        self.error_label.setText(res[0].replace('ФИО', 'Имя'))
        self.name_edit.setStyleSheet('border-radius: 2px;\n'
                                     'border-width: 1px;\n'
                                     'border-style: solid;\n'
                                     'border-color: ' + res[1] + ';')
        if res[1] == '':
            self.name_edit.setStyleSheet('')
        self.cor_name = True if res[1] == 'green' else False
        self.open_btn()

    def surname_changed(self) -> None:
        """Проверка на правильность написания фамилии"""
        res = self.fio_check(self.surname_edit.text())
        self.error_label.setText(res[0].replace('ФИО', 'Фамилия'))
        self.surname_edit.setStyleSheet('border-radius: 2px;\n'
                                        'border-width: 1px;\n'
                                        'border-style: solid;\n'
                                        'border-color: ' + res[1] + ';')
        if res[1] == '':
            self.surname_edit.setStyleSheet('')
        self.cor_surname = True if res[1] == 'green' else False
        self.open_btn()

    def patronymic_changed(self) -> None:
        """Проверка на правильность написания отчества"""
        res = self.fio_check(self.patronymic_edit.text())
        self.error_label.setText(res[0].replace('ФИО', 'Отчество'))
        self.patronymic_edit.setStyleSheet('border-radius: 2px;\n'
                                           'border-width: 1px;\n'
                                           'border-style: solid;\n'
                                           'border-color: ' + res[1] + ';')
        if res[1] == '':
            self.patronymic_edit.setStyleSheet('')
        self.cor_patronymic = True if res[1] == 'green' else False
        self.open_btn()

    @staticmethod
    def fio_check(text) -> tuple:
        """Проверка на правильность написания ФИО"""
        if text:
            if text.replace('-', '').isalpha() and '--' not in text:
                return '', 'green'
            else:
                if not text.replace('-', '').isalpha():
                    return ' может содержать только буквы и "-"', 'red'
                else:
                    return ' не может содержать 2 "-" подряд', 'red'
        else:
            return '', ''
