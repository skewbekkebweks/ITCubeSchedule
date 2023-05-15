from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Code.add_group import AddGroup
from Code.add_office import AddOffice
from Code.add_schedule import AddSchedule
from Code.add_teacher import AddTeacher
from Design.admin import Ui_Admin
from constants import NUM_TO_WEEK_DAY, WEEK_DAY_TO_NUM


class Admin(Ui_Admin, QMainWindow):
    """Добавление занятий"""

    def __init__(self, connect, main_window) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.main_window = main_window  # главное окно
        self.teacher_box.currentTextChanged.connect(self.cur_groups_change)
        self.group_box.currentTextChanged.connect(self.cur_schedule_change)
        self.add_teacher_btn.clicked.connect(self.add_teacher)
        self.add_group_btn.clicked.connect(self.add_group)
        self.add_schedule_btn.clicked.connect(self.add_schedule)
        self.add_office_btn.clicked.connect(self.add_office)
        self.remove_teacher_btn.clicked.connect(self.remove_teacher)
        self.remove_group_btn.clicked.connect(self.remove_group)
        self.remove_schedule_btn.clicked.connect(self.remove_schedule)
        self.remove_office_btn.clicked.connect(self.remove_office)
        self.cur_teachers_change()
        self.cur_office_change()

    def cur_teachers_change(self):
        self.teacher_box.clear()
        cursor = self.connect.cursor()
        command = f'select name ' \
                  f'from teachers'
        res = cursor.execute(command).fetchall()
        res = map(lambda x: x[0], res)
        self.teacher_box.addItems(res)
        self.cur_groups_change()

    def cur_groups_change(self):
        self.group_box.clear()
        cursor = self.connect.cursor()
        command = f'select title ' \
                  f'from squads ' \
                  f'where teacher = (select id ' \
                  f'from teachers ' \
                  f'where name = \'{self.teacher_box.currentText()}\')'
        res = cursor.execute(command).fetchall()
        res = map(lambda x: x[0], res)
        self.group_box.addItems(res)
        self.cur_schedule_change()

    def cur_schedule_change(self):
        self.schdule_box.clear()
        cursor = self.connect.cursor()
        command = f'select start_date, stop_date, week_day, time_start, time_stop ' \
                  f'from schedule ' \
                  f'where squad = (select id ' \
                  f'from squads ' \
                  f'where title = \'{self.group_box.currentText()}\' ' \
                  f'and teacher = (select id ' \
                  f'from teachers ' \
                  f'where name = \'{self.teacher_box.currentText()}\'))'
        res = cursor.execute(command).fetchall()
        res = list(map(lambda x: f'{x[0]}-{x[1]}. {NUM_TO_WEEK_DAY[x[2]]}. {x[3]}-{x[4]}', res))
        self.schdule_box.addItems(res)

    def cur_office_change(self):
        self.office_box.clear()
        cursor = self.connect.cursor()
        command = f'select number, title ' \
                  f'from offices'
        res = cursor.execute(command).fetchall()
        res = list(map(lambda x: f'{x[0]}. {x[1]}', res))
        self.office_box.addItems(res)

    def add_teacher(self):
        self.add_teacher_ = AddTeacher(self.connect, self)
        self.add_teacher_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.add_teacher_.show()  # показ окна

    def add_group(self):
        self.add_group_ = AddGroup(self.connect, self)
        self.add_group_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.add_group_.show()  # показ окна

    def add_schedule(self):
        self.add_schedule_ = AddSchedule(self.connect, self)
        self.add_schedule_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.add_schedule_.show()  # показ окна

    def add_office(self):
        self.add_office_ = AddOffice(self.connect, self)
        self.add_office_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.add_office_.show()  # показ окна

    def remove_teacher(self):
        reply = QMessageBox.question(self, 'Удаление учителя',
                                     'Вы уверены, что хотите удалить данного учителя?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            cursor = self.connect.cursor()
            command = f'delete ' \
                      f'from teachers ' \
                      f'where name = \'{self.teacher_box.currentText()}\''
            cursor.execute(command)
            self.connect.commit()
            self.cur_teachers_change()

    def remove_group(self):
        reply = QMessageBox.question(self, 'Удаление группы',
                                     'Вы уверены, что хотите удалить данную группу?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            cursor = self.connect.cursor()
            command = f'delete ' \
                      f'from squads ' \
                      f'where teacher = (select id ' \
                      f'from teachers ' \
                      f'where name = \'{self.teacher_box.currentText()}\') ' \
                      f'and title = \'{self.group_box.currentText()}\''
            cursor.execute(command)
            self.connect.commit()
            self.cur_groups_change()

    def remove_schedule(self):
        reply = QMessageBox.question(self, 'Удаление циклического урока',
                                     'Вы уверены, что хотите удалить данную группу?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            text = self.schdule_box.currentText().split('. ')
            start_date, stop_date = text[0].split('-')
            week_day = int(WEEK_DAY_TO_NUM[text[1]])
            time_start, time_stop = text[2].split('-')
            cursor = self.connect.cursor()
            command = f'delete ' \
                      f'from schedule ' \
                      f'where start_date = \'{start_date}\' ' \
                      f'and stop_date = \'{stop_date}\' ' \
                      f'and week_day = {week_day} ' \
                      f'and time_start = \'{time_start}\' ' \
                      f'and time_stop = \'{time_stop}\' ' \
                      f'and squad = (select id ' \
                      f'from squads ' \
                      f'where title = \'{self.group_box.currentText()}\')'
            cursor.execute(command)
            self.connect.commit()
            self.cur_schedule_change()

    def remove_office(self):
        reply = QMessageBox.question(self, 'Удаление кабинета',
                                     'Вы уверены, что хотите удалить этот кабинет?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            number = self.office_box.currentText().split('. ')[0]
            cursor = self.connect.cursor()
            command = f'delete ' \
                      f'from offices ' \
                      f'where number = {number}'
            cursor.execute(command)
            self.connect.commit()
            self.cur_office_change()
