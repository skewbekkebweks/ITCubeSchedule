from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Design.add_group import Ui_AddGroup
from Code.notification import signal


class AddGroup(Ui_AddGroup, QMainWindow):
    def __init__(self, connect, admin) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.admin = admin
        self.pushButton.clicked.connect(self.check)

    def check(self):
        cursor = self.connect.cursor()
        command = f'select count() ' \
                  f'from squads ' \
                  f'where title = \'{self.title_of_group.text()}\''
        res = cursor.execute(command).fetchone()[0]
        if res == 0:
            command = f'select id ' \
                      f'from teachers ' \
                      f'where name = \'{self.admin.teacher_box.currentText()}\''
            teacher = cursor.execute(command).fetchone()[0]
            command = f'insert into ' \
                      f'squads(title, teacher) ' \
                      f'values(\'{self.title_of_group.text()}\', {teacher})'
            cursor.execute(command)
            self.connect.commit()
            self.admin.cur_groups_change()
            signal()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Группа с таким названием уже существует',
                                 QMessageBox.Ok)
