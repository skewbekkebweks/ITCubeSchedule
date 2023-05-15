from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Code.work_with_login_password import WorkWithLoginPassword
from Design.registration import Ui_Registration
from Code.notification import signal


class ChangeLoginPassword(Ui_Registration, QMainWindow,
                          WorkWithLoginPassword):
    """Смена логина или пароля преподавателем"""

    def __init__(self, connect, main_window) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение к БД
        self.main_window = main_window  # главное окно
        self.setWindowTitle('Изменения логина и пароля')
        self.pushButton.setText('Готово')
        cursor = self.connect.cursor()
        command = f'select name ' \
                  f'from teachers ' \
                  f'where id = {self.main_window.cur_profile}'
        res = cursor.execute(command).fetchone()[0].split()  # полное имя преподавателя
        # заполнение ФИО преподавателя
        self.name_edit.setText(res[1])
        self.surname_edit.setText(res[0])
        self.patronymic_edit.setText(res[2])
        # изменение цвета заполненных полей (ФИО)
        self.name_edit.setStyleSheet('border-radius: 2px;\n'
                                     'border-width: 1px;\n'
                                     'border-style: solid;\n'
                                     'border-color: green;')
        self.surname_edit.setStyleSheet('border-radius: 2px;\n'
                                        'border-width: 1px;\n'
                                        'border-style: solid;\n'
                                        'border-color: green;')
        self.patronymic_edit.setStyleSheet('border-radius: 2px;\n'
                                           'border-width: 1px;\n'
                                           'border-style: solid;\n'
                                           'border-color: green;')
        # блокировка полей ФИО
        self.name_edit.setEnabled(0)
        self.surname_edit.setEnabled(0)
        self.patronymic_edit.setEnabled(0)
        # флажки для разблоикровки кнопки сохранения
        self.cor_name = self.cor_surname = self.cor_patronymic = True
        self.cor_login = self.cor_password = False
        self.pushButton.clicked.connect(self.check)
        # вызов функции при изменении текста
        self.login_edit.textEdited.connect(self.login_changed)
        self.password_edit.textEdited.connect(self.password_changed)

    def check(self) -> None:
        """Изменение логина и пароля преподавателя"""
        cursor = self.connect.cursor()
        command = f'select login, id ' \
                  f'from teachers ' \
                  f'where login = \'{self.login_edit.text()}\''
        res = cursor.execute(command).fetchone()
        # проверка на занятость выбранного логина
        if not (res is None) and res[0] and res[1] != self.main_window.cur_profile:
            QMessageBox.critical(self, 'Ошибка',
                                 'Профиль с таким логином уже существует',
                                 QMessageBox.Ok)
        else:
            # изменение иинформации
            command = f'update teachers ' \
                      f'set login = \'{self.login_edit.text()}\', ' \
                      f'password = \'{self.password_edit.text()}\' ' \
                      f'where id = \'{self.main_window.cur_profile}\''
            cursor.execute(command)
            self.connect.commit()
            signal()
            self.close()
