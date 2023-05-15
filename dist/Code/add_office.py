from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Code.notification import signal
from Design.add_office import Ui_AddOffice


class AddOffice(Ui_AddOffice, QMainWindow):
    def __init__(self, connect, admin) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.admin = admin
        self.pushButton.clicked.connect(self.check)

    def check(self):
        try:
            num = int(self.number_edit.text())
            title = self.title_edit.text()
            cursor = self.connect.cursor()
            command = f'select count() ' \
                      f'from offices ' \
                      f'where title = \'{title}\' ' \
                      f'or number = {num}'
            res = cursor.execute(command).fetchone()[0]
            if res:
                QMessageBox.critical(self, 'Ошибка', 'Кабинет с таким именем или номером существует',
                                     QMessageBox.Ok)
            else:
                command = f'insert into ' \
                          f'offices(number, title) values({num}, \'{title}\')'
                cursor.execute(command)
                self.connect.commit()
                self.admin.cur_office_change()
                signal()
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Номер кабинета должен состоять только из цифр',
                                 QMessageBox.Ok)
