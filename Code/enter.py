from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Code.admin import Admin
from Design.enter import Ui_Enter
from Code.notification import signal
from Code.work_with_login_password import WorkWithLoginPassword


class Enter(Ui_Enter, QMainWindow, WorkWithLoginPassword):
    """Вход в систему"""

    def __init__(self, connect, main_window) -> None:
        super().__init__()
        self.setupUi(self)  # пожключение дизайна
        self.connect = connect  # подключение к БД
        self.main_window = main_window  # главное окно
        self.pushButton.clicked.connect(self.check)
        self.teacher_btn.clicked.connect(self.teacher_enter)
        self.student_btn.clicked.connect(self.student_enter)
        self.hide_password_btn.clicked.connect(self.hide_show_password)
        # скрытие виджетов до выбора статуса
        self.login_label.hide()
        self.login_edit.hide()
        self.password_label.hide()
        self.password_edit.hide()
        self.group_label.hide()
        self.group_box.hide()
        self.hide_password_btn.hide()

    def hide_show_password(self):
        """Скрытие или открытие пароля"""
        if self.hide_password_btn.text() == 'Скрыть пароль':
            self.hide_password_btn.setText('Показать пароль')
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.hide_password_btn.setText('Скрыть пароль')
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)

    def teacher_enter(self) -> None:
        """Открытие виджетов для учителей"""
        self.login_label.show()
        self.login_edit.show()
        self.password_label.show()
        self.password_edit.show()
        self.group_label.hide()
        self.group_box.hide()
        self.hide_password_btn.show()

    def student_enter(self) -> None:
        """Открытие виджетов для ученика """
        cursor = self.connect.cursor()
        self.login_label.hide()
        self.login_edit.hide()
        self.password_label.hide()
        self.password_edit.hide()
        self.group_label.show()
        self.group_box.show()
        self.hide_password_btn.hide()
        command = f'select title, teacher ' \
                  f'from squads'
        result = cursor.execute(command).fetchall()  # все существующие группы
        for elem in result:
            command = f'select name ' \
                      f'from teachers ' \
                      f'where id = {elem[1]}'
            name = cursor.execute(command).fetchone()  # учитель текущей группы
            self.group_box.addItem(f'{elem[0]}: {name[0]}')

    def check(self) -> None:
        """Вход в систему"""
        if self.teacher_btn.isChecked():
            if self.login_edit.text() == self.password_edit.text() == 'admin':
                # вход под статусом админа
                self.close()
                self.admin_ = Admin(self.connect, self.main_window)
                self.admin_.setWindowModality(Qt.ApplicationModal)  # установка модальности
                self.admin_.show()  # показ окна
            else:
                # проверка для учителя
                cursor = self.connect.cursor()
                command = f'select id ' \
                          f'from teachers ' \
                          f'where login = \'{self.login_edit.text()}\' ' \
                          f'and password = \'{self.password_edit.text()}\''
                result = cursor.execute(command).fetchone()
                if result:
                    self.main_window.cur_profile = result[0]
                    self.main_window.change_status(2)  # статус: учитель
                    signal()
                    self.close()
                else:
                    QMessageBox.critical(self, 'Ошибка', 'Профиль не найден', QMessageBox.Ok)
        elif self.student_btn.isChecked():
            # проверка для ученика
            cursor = self.connect.cursor()
            title = self.group_box.currentText().split(':')[0]
            command = f'select id ' \
                      f'from squads ' \
                      f'where title = \'{title}\''
            result = cursor.execute(command).fetchone()
            self.main_window.cur_group = result[0]
            self.main_window.change_status(1)  # статус: ученик
            signal()
            self.close()
        else:
            # вывод ошибки
            QMessageBox.critical(self, 'Ошибка', 'Заполните необходимые поля',
                                 QMessageBox.Ok)
