import sqlite3
import sys
from datetime import datetime
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QCloseEvent, QColor
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Code.add_class import AddClass
from Code.enter import Enter
from Code.profile import Profile
from Code.registration import Registration
from Code.remove_class import RemoveClass
from Design.main_window import Ui_MainWindow
from constants import *


class MyWindow(QMainWindow, Ui_MainWindow):
    """Главное окно"""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = sqlite3.connect(DATA_BASE)  # подключение к БД
        self.connect.execute("PRAGMA foreign_keys = ON")
        self.registration_profile_btn.clicked.connect(self.registration_profile)
        self.enter_exit_btn.clicked.connect(self.enter_exit)
        self.change_status(0)  # статус: без профиля
        self.add_class_btn.clicked.connect(self.add_class)
        self.remove_class_btn.clicked.connect(self.remove_class)
        self.calendarWidget.currentPageChanged.connect(self.page_change)
        self.calendarWidget.selectionChanged.connect(self.date_change)

    def classes_info(self) -> None:
        """Информация о занятиях"""
        cursor = self.connect.cursor()
        command = f'select distinct day ' \
                  f'from exceptions'
        days = cursor.execute(command).fetchall()  # все различные даты занятий
        days = list(map(lambda x: x[0], days))
        today = str(datetime.today().date())
        correct_days = []
        for elem in days:
            cor_elem = '-'.join(reversed(elem.split('.')))
            if cor_elem < today:
                correct_days.append(elem)
        days = correct_days
        str_days = "(\"" + "\", \"".join(days) + "\")"
        command = f'delete from exceptions ' \
                  f'where day in {str_days}'  # удаление изменений в занятиях прошедших дней
        cursor.execute(command)
        self.connect.commit()
        self.listWidget.clear()
        if self.status == 1:
            # информация для учеников
            command = f'select title, teacher ' \
                      f'from squads ' \
                      f'where id = {self.cur_group}'
            group, teacher_id = cursor.execute(command).fetchone()  # название группы, id учителя
            command = f'select name ' \
                      f'from teachers ' \
                      f'where id = {teacher_id}'
            name = cursor.execute(command).fetchone()[0]  # имя преподавателя
            command = f'select office ' \
                      f'from teachers ' \
                      f'where id = {teacher_id}'
            office_id = cursor.execute(command).fetchone()[0]
            print(office_id)
            command = f'select number, title ' \
                      f'from offices ' \
                      f'where id = {office_id}'
            office_number, office_title = cursor.execute(command).fetchone()  # № и название кабинета
            command = f'select start_date, stop_date, week_day, time_start, time_stop ' \
                      f'from schedule ' \
                      f'where squad = {self.cur_group}'
            schedule = cursor.execute(command).fetchall()  # расписание
            command = f'select day, time_start, time_stop, status ' \
                      f'from exceptions ' \
                      f'where squad = {self.cur_group}'
            exceptions = cursor.execute(command).fetchall()  # запланированные изменения
            # формирование итоговой информации
            items = [f'Преподаватель: {name}', f'Кабинет: {office_title}({office_number})',
                     f'Группа: {group}', 'Запланированное расписание:',
                     *[f'{elem[0]}-{elem[1]}. {NUM_TO_WEEK_DAY[elem[2]]}: {elem[3]}-{elem[4]}'
                       for elem in sorted(schedule)]]
            if exceptions:
                items.append('Запланированные изменения:')
                items.extend([f'{elem[0]}: {elem[1]}-{elem[2]}. '
                              f'{"Добавлено" if elem[3] else "Удалено"} занятие'
                              for elem in sorted(exceptions)])
            self.listWidget.addItems(items)
        elif self.status == 2:
            # информация для преподавателей
            command = f'select office ' \
                      f'from teachers ' \
                      f'where id = {self.cur_profile}'
            office_id = cursor.execute(command).fetchone()[0]
            command = f'select number, title ' \
                      f'from offices ' \
                      f'where id = {office_id}'
            office_number, office_title = cursor.execute(command).fetchone()  # № и название кабинета
            command = f'select start_date, stop_date, week_day, time_start, time_stop, squad ' \
                      f'from schedule ' \
                      f'where squad in (select id ' \
                      f'from squads ' \
                      f'where teacher = {self.cur_profile})'
            schedule = cursor.execute(command).fetchall()  # расписание групп преподавателя
            command = f'select day, time_start, time_stop, squad, status ' \
                      f'from exceptions ' \
                      f'where squad in (select id ' \
                      f'from squads ' \
                      f'where teacher = {self.cur_profile})'
            exceptions = cursor.execute(command).fetchall()  # исключения в группах преподавателя
            command = f'select id, title ' \
                      f'from squads ' \
                      f'where teacher = {self.cur_profile}'
            groups = cursor.execute(command).fetchall()  # id и название всех групп данного учителя
            group_id_to_title = {}  # словарь id: title
            for elem in groups:
                group_id_to_title[elem[0]] = elem[1]
            # формирование итоговой информации
            items = [f'Кабинет: {office_title}({office_number})', 'Запланированное расписание:',
                     *[f'{elem[0]}-{elem[1]}. {NUM_TO_WEEK_DAY[elem[2]]}: {elem[3]}-{elem[4]}. '
                       f'{group_id_to_title[elem[5]]}' for elem in sorted(schedule)]]
            if exceptions:
                items.append('Запланированные изменения:')
                items.extend([f'{elem[0]}: {elem[1]}-{elem[2]}. '
                              f'{"Добавлено" if elem[4] else "Удалено"} занятие. '
                              f'{group_id_to_title[elem[3]]}' for elem in sorted(exceptions)])
            self.listWidget.addItems(items)

    def registration_profile(self) -> None:
        """Перенаправление на нужную функцию"""
        if self.status:
            self.profile()
        else:
            self.registration()

    def profile(self) -> None:
        """Профиль преподавателя"""
        self.profile_ = Profile(self.connect, self)
        self.profile_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.profile_.show()  # показ окна

    def registration(self) -> None:
        """Регистрация для преподавателя"""
        self.registration_ = Registration(self.connect)
        self.registration_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.registration_.show()  # показ окна

    def enter_exit(self) -> None:
        """Перенаправление на нужную функцию"""
        if self.status:
            self.exit()
        else:
            self.enter()

    def enter(self) -> None:
        """Вход в систему"""
        self.enter_ = Enter(self.connect, self)
        self.enter_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.enter_.show()  # показ окна

    def exit(self) -> None:
        """Выход из системы"""
        reply = QMessageBox.question(self, 'Выход',
                                     'Вы уверены, что хотите выйти?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.change_status(0)  # статус: без профиля

    def change_status(self, value: int) -> None:
        """Смена статуса вместе с изменением дизайна"""
        self.status = value  # изменение статуса
        if self.status == 0:
            self.enter_exit_btn.setText('Войти')
            self.registration_profile_btn.show()
            self.registration_profile_btn.setText('Зарегистрироваться')
            self.calendarWidget.setEnabled(0)
            cur_date = datetime.today()
            begin_date = QDate(cur_date.year, cur_date.month, 1)
            while int(str(begin_date.toPyDate()).split('-')[1]) == cur_date.month:
                self.calendarWidget.setDateTextFormat(begin_date, QTextCharFormat())
                begin_date = begin_date.addDays(1)
            self.add_class_btn.setEnabled(0)
            self.remove_class_btn.setEnabled(0)
            self.classes_list.clear()
            self.listWidget.clear()
        elif self.status == 1:
            self.enter_exit_btn.setText('Выйти')
            self.registration_profile_btn.hide()
            self.calendarWidget.setEnabled(1)
            self.add_class_btn.setEnabled(0)
            self.remove_class_btn.setEnabled(0)
            self.classes_list.clear()
            self.day_with_class = QTextCharFormat()
            self.day_with_class.setBackground(QColor(0, 255, 0))
            cur_date = datetime.today()
            self.page_change(cur_date.year, cur_date.month)
            self.classes_info()
        elif self.status == 2:
            self.enter_exit_btn.setText('Выйти')
            self.registration_profile_btn.show()
            self.registration_profile_btn.setText('Профиль')
            self.calendarWidget.setEnabled(1)
            self.add_class_btn.setEnabled(1)
            self.remove_class_btn.setEnabled(1)
            self.classes_list.clear()
            self.day_with_class = QTextCharFormat()
            self.day_with_class.setBackground(QColor(0, 255, 0))
            cur_date = datetime.today()
            self.page_change(cur_date.year, cur_date.month)
            self.classes_info()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Дейсвтие окна после нажатия на крестик"""
        self.connect.close()
        event.accept()

    def page_change(self, year, month):
        begin_date = QDate(year, month, 1)
        cursor = self.connect.cursor()
        if self.status == 1:
            groups = ((self.cur_group,),)
        else:
            command = f'select id ' \
                      f'from squads ' \
                      f'where teacher = {self.cur_profile}'
            groups = cursor.execute(command).fetchall()  # все группы преподавателя
        groups = list(map(lambda x: str(x[0]), groups))
        command = f'select day, status ' \
                  f'from exceptions ' \
                  f'where squad in ({", ".join(groups)}) '
        exceptions = cursor.execute(command).fetchall()  # исключения
        while int(str(begin_date.toPyDate()).split('-')[1]) == month:
            if begin_date < QDate.currentDate():
                begin_date = begin_date.addDays(1)
                continue
            command = f'select week_day, start_date, stop_date ' \
                      f'from schedule ' \
                      f'where squad in ({", ".join(groups)}) '
            schedule = cursor.execute(command).fetchall()  # все дни, в которые есть уроки
            cor_schedule = []
            for elem in schedule:
                if "-".join(reversed(str(elem[1]).split("."))) <= str(
                        begin_date.toPyDate()) < "-".join(reversed(str(elem[2]).split("."))):
                    cor_schedule.append(int(elem[0]))
            schedule = cor_schedule
            # подсчет количества уроков
            count = schedule.count(begin_date.dayOfWeek())
            for elem in exceptions:
                if elem[0] == '.'.join(reversed(str(begin_date.toPyDate()).split('-'))):
                    count += 1 if elem[1] else -1
            if count >= 1:
                # обозначения дня на календаре
                self.calendarWidget.setDateTextFormat(begin_date, self.day_with_class)
            else:
                self.calendarWidget.setDateTextFormat(begin_date, QTextCharFormat())
            begin_date = begin_date.addDays(1)

    def date_change(self):
        self.classes_list.clear()
        date = self.calendarWidget.selectedDate()
        if date < QDate.currentDate():
            return
        cursor = self.connect.cursor()
        if self.status == 1:
            command = f'select id, title ' \
                      f'from squads ' \
                      f'where id = {self.cur_group}'
            res = cursor.execute(command).fetchall()  # id текущей группы
        else:
            command = f'select id, title ' \
                      f'from squads ' \
                      f'where teacher = {self.cur_profile}'
            res = cursor.execute(command).fetchall()  # все группы преподавателя
        group_id_to_title = {}  # словарь id: title
        for elem in res:
            # заполнение словаря
            group_id_to_title[elem[0]] = elem[1]
        groups = list(map(str, group_id_to_title.keys()))
        command = f'select squad, time_start, time_stop, start_date, stop_date ' \
                  f'from schedule ' \
                  f'where week_day = {date.dayOfWeek()} ' \
                  f'and squad in ({", ".join(groups)})'
        schedule = cursor.execute(command).fetchall()  # расписание на выбранный день
        cor_schedule = []
        for elem in schedule:
            if "-".join(reversed(str(elem[3]).split("."))) <= str(
                    date.toPyDate()) < "-".join(reversed(str(elem[4]).split("."))):
                cor_schedule.append(elem[:3])
        schedule = cor_schedule
        command = f'select squad, time_start, time_stop, status ' \
                  f'from exceptions ' \
                  f'where day = \'{".".join(reversed(str(date.toPyDate()).split("-")))}\' ' \
                  f'and squad in ({", ".join(groups)}) '
        exceptions = cursor.execute(command).fetchall()  # исключения на выбранный день
        for elem in exceptions:
            # итоговое расписание группы на выбранный день
            if elem[3] == 1:
                schedule.append(elem[:3])
            else:
                schedule.remove(elem[:3])
        if self.status == 1:
            schedule = list(map(lambda x: f'{x[1]}-{x[2]}.', schedule))
        else:
            schedule = list(
                map(lambda x: f'{x[1]}-{x[2]}. Группа: {group_id_to_title[x[0]]}', schedule))
        self.classes_list.addItems(schedule)

    def add_class(self) -> None:
        """Добавление занятий"""
        today = datetime.today().date()
        selected_date = self.calendarWidget.selectedDate().toPyDate()
        if selected_date < today:  # проверка на корректность добавленного занятия
            QMessageBox.critical(self, 'Ошибка', 'Вы добавляете занятие на прошедший день',
                                 QMessageBox.Ok)
        else:
            self.add_class_ = AddClass(self.connect, self)
            self.add_class_.setWindowModality(Qt.ApplicationModal)  # установка модальности
            self.add_class_.show()  # показ окна

    def remove_class(self) -> None:
        """Удаление занятий"""
        if self.classes_list.count():
            today = datetime.today().date()
            selected_date = self.calendarWidget.selectedDate().toPyDate()
            if selected_date < today:  # проверка на корректность удаленного занятия
                QMessageBox.critical(self, 'Ошибка', 'Вы удаляете занятие с прошедшего дня',
                                     QMessageBox.Ok)
            else:
                self.remove_class_ = RemoveClass(self.connect, self)
                self.remove_class_.setWindowModality(Qt.ApplicationModal)  # установка модальности
                self.remove_class_.show()  # показ окна
        else:
            QMessageBox.critical(self, 'Ошибка', 'В этот день занятия отсутствуют',
                                 QMessageBox.Ok)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
