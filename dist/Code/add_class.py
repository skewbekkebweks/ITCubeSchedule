from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Design.add_class import Ui_AddClass
from Code.notification import signal


class AddClass(Ui_AddClass, QMainWindow):
    """Добавление занятий"""

    def __init__(self, connect, main_window) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.main_window = main_window  # главное окно
        self.date = self.main_window.calendarWidget.selectedDate()  # выбранная на календаре дата
        self.pushButton.clicked.connect(self.new_class)
        cursor = self.connect.cursor()
        command = f'select title ' \
                  f'from squads ' \
                  f'where teacher = {self.main_window.cur_profile}'
        groups = cursor.execute(command).fetchall()  # все группы зайденного преподавателя
        self.group_box.addItems(map(lambda x: x[0], groups))

    def new_class(self):
        """Перенаправления сигнала с кнопки"""
        self.check(self.date.dayOfWeek(), '.'.join(reversed(str(self.date.toPyDate()).split('-'))),
                   ':'.join(str(self.time_start.time().toPyTime()).split(':')[:2]),
                   ':'.join(str(self.time_stop.time().toPyTime()).split(':')[:2]))

    def check(self, cur_day, cur_date, time_start, time_stop) -> None:
        """Добавление занятия"""
        cursor = self.connect.cursor()
        command = f'select id ' \
                  f'from squads ' \
                  f'where title = \'{self.group_box.currentText()}\''
        group = cursor.execute(command).fetchone()[0]  # группа, у которой добавляется занятие
        command = f'select id ' \
                  f'from squads ' \
                  f'where teacher in (select id ' \
                  f'from teachers ' \
                  f'where id  = {self.main_window.cur_profile})'
        groups = cursor.execute(command).fetchall()  # все группы, обучающиеся в кабинете учителя
        groups = list(map(lambda x: str(x[0]), groups))
        command = f'select time_start, time_stop ' \
                  f'from schedule ' \
                  f'where week_day = {cur_day} ' \
                  f'and start_date <= \'{cur_date}\' ' \
                  f'and stop_date > \'{cur_date}\'' \
                  f'and squad in ({", ".join(groups)})'
        schedule = cursor.execute(command).fetchall()  # расписание этих групп
        command = f'select time_start, time_stop, status ' \
                  f'from exceptions ' \
                  f'where day = \'{cur_date}\' ' \
                  f'and squad in ({", ".join(groups)})'
        exceptions = cursor.execute(command).fetchall()  # уже добавленные изменения в группах
        for elem in exceptions:
            # итоговое расписание группы на выбранный день
            if elem[2] == 1:
                schedule.append(elem[:2])
            else:
                schedule.remove(elem[:2])
        if time_start == time_stop:
            # пустое занятие (длится 0 минут)
            QMessageBox.critical(self, 'Ошибка', 'Вы добавили занятие длиной 0 минут',
                                 QMessageBox.Ok)
        elif time_start > time_stop:
            QMessageBox.critical(self, 'Ошибка', 'Конец занятия не может быть раньше его начала',
                                 QMessageBox.Ok)
        else:
            for elem in schedule:

                if time_start <= elem[0] < time_stop or time_start < elem[1] <= time_stop:
                    QMessageBox.critical(self, 'Ошибка', 'Ваши занятия буду пересекаться',
                                         QMessageBox.Ok)
                    break
            else:
                # добвление занятия
                command = f'select count() ' \
                          f'from exceptions ' \
                          f'where time_start = \'{time_start}\' ' \
                          f'and time_stop = \'{time_stop}\' ' \
                          f'and squad = {group} ' \
                          f'and status = 0'
                res = cursor.execute(command).fetchone()[0]
                if res:  # проверка на то, было ли удалено это занятие прежде
                    command = f'delete from exceptions ' \
                              f'where time_start = \'{time_start}\' ' \
                              f'and time_stop = \'{time_stop}\' ' \
                              f'and squad = {group} ' \
                              f'and status = 0'
                else:
                    command = f'insert into exceptions values' \
                              f'(\'{cur_date}\', {group}, \'{time_start}\', \'{time_stop}\', 1)'
                cursor.execute(command)
                self.connect.commit()
                self.main_window.page_change(*map(int, cur_date.split('.')[2:0:-1]))
                self.main_window.date_change()
                signal()
                self.main_window.classes_info()  # обновление информации
