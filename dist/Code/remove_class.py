from PyQt5.QtWidgets import QMainWindow

from Design.remove_class import Ui_RemoveClass
from Code.notification import signal


class RemoveClass(Ui_RemoveClass, QMainWindow):
    """Удаление занятий"""

    def __init__(self, connect, main_window, ) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение к БД
        self.main_window = main_window  # главное окно
        self.date = self.main_window.calendarWidget.selectedDate()  # выбранная дата
        self.cur_day, self.cur_date = self.date.dayOfWeek(), self.date.toPyDate()
        self.cur_date = '.'.join(reversed(str(self.cur_date).split('-')))
        self.pushButton.clicked.connect(self.del_class)
        self.fill_box()

    def fill_box(self) -> None:
        """Заполнение бокса всеми занятиями, которые проходят в выбранный день"""
        self.classes_box.clear()
        if self.main_window.classes_list.count():
            for x in range(self.main_window.classes_list.count()):
                self.classes_box.addItem(self.main_window.classes_list.item(x).text())
        else:
            self.close()

    def del_class(self):
        """Перенаправления сигнала с кнопки"""
        text = self.classes_box.currentText()
        self.check(text)

    def check(self, text) -> None:
        """Удаление занятия"""
        # проверка наличия занятий в выбранный день.
        if text == '':
            return
        cursor = self.connect.cursor()
        command = f'select id, title ' \
                  f'from squads ' \
                  f'where teacher = {self.main_window.cur_profile}'
        res = cursor.execute(command).fetchall()  # все группы преподавателя
        group_title_to_id = {}  # словарь title: id
        for elem in res:
            # заполнение словаря
            group_title_to_id[elem[1]] = elem[0]
        time_start, time_stop = text.split('. Группа: ')[0].split('-')
        group = group_title_to_id[text.split('. Группа: ')[1]]
        cursor = self.connect.cursor()
        command = f'select count() ' \
                  f'from exceptions ' \
                  f'where time_start = \'{time_start}\' ' \
                  f'and time_stop = \'{time_stop}\' ' \
                  f'and squad = {group} ' \
                  f'and status = 1'
        res = cursor.execute(command).fetchone()[0]
        if res:  # проверка на то, было ли добавлено это занятие прежде
            command = f'delete from exceptions ' \
                      f'where time_start = \'{time_start}\' ' \
                      f'and time_stop = \'{time_stop}\' ' \
                      f'and day = \'{self.cur_date}\'' \
                      f'and squad = {group} ' \
                      f'and status = 1'
        else:
            command = f'insert into exceptions values' \
                      f'(\'{self.cur_date}\', {group}, \'{time_start}\', \'{time_stop}\', 0)'
        cursor.execute(command)
        self.connect.commit()
        self.main_window.page_change(*map(int, str(self.date.toPyDate()).split('-')[:2]))
        self.main_window.date_change()
        signal()
        self.main_window.classes_info()
        self.fill_box()
