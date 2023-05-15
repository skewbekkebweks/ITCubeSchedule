from abc import abstractmethod
from Code.password_check import password_check


class WorkWithLoginPassword:
    """Базовый класс для работы с логином и паролем"""

    def __init__(self) -> None:
        """Объявление всех используемых атрибутов"""
        self.hide_password_btn = None
        self.password_edit = None
        self.error_label = None
        self.login_edit = None
        self.pushButton = None
        self.cor_patronymic = None
        self.cor_surname = None
        self.cor_name = None

    def open_btn(self) -> None:
        """Разблокировка кнопки сохранения"""
        if all([self.cor_name, self.cor_surname, self.cor_patronymic, self.cor_login,
                self.cor_password]):  # проверка на удовлетворение всех полей условиям
            self.pushButton.setEnabled(1)
        else:
            self.pushButton.setEnabled(0)

    def login_changed(self, text: str) -> None:
        """Проверка корректности логина"""
        if text:
            self.cor_login = True
            self.login_edit.setStyleSheet('border-radius: 2px;\n'
                                          'border-width: 1px;\n'
                                          'border-style: solid;\n'
                                          'border-color: green;')
        else:
            self.cor_login = False
            self.login_edit.setStyleSheet('')
        self.open_btn()

    def password_changed(self, text: str) -> None:
        """Проверка корректности пароля"""
        res = password_check(text)
        self.error_label.setText(res[0])
        self.password_edit.setStyleSheet('border-radius: 2px;\n'
                                         'border-width: 1px;\n'
                                         'border-style: solid;\n'
                                         'border-color: ' + res[1] + ';')
        if res[1] == '':
            self.password_edit.setStyleSheet('')
        self.cor_password = res[2]
        self.open_btn()

    @abstractmethod
    def check(self) -> None:
        pass
