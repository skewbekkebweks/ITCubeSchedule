from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Code.notification import signal
from Design.add_schedule import Ui_AddSchedule


class AddSchedule(Ui_AddSchedule, QMainWindow):
    def __init__(self, connect, admin) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение БД
        self.admin = admin
        self.pushButton.clicked.connect(self.check)

    def check(self):
        date_start = '-'.join(reversed(self.start_date.text().split('.')))
        date_stop = '-'.join(reversed(self.stop_date.text().split('.')))
        if date_stop <= date_start:
            QMessageBox.critical(self, 'Ошибка', 'Конец периода должен быть больше его начала',
                                 QMessageBox.Ok)
            return
        time_start = self.start_time.text().rjust(5, '0')
        time_stop = self.stop_time.text().rjust(5, '0')
        if time_stop <= time_start:
            QMessageBox.critical(self, 'Ошибка', 'Конец занятия должен быть больше его начала',
                                 QMessageBox.Ok)
            return
        cursor = self.connect.cursor()
        command = f'select id ' \
                  f'from squads ' \
                  f'where teacher = (select id ' \
                  f'from teachers ' \
                  f'where name  = \'{self.admin.teacher_box.currentText()}\')'
        groups = cursor.execute(command).fetchall()  # все группы, обучающиеся в кабинете учителя
        groups = list(map(lambda x: str(x[0]), groups))
        command = f'select time_start, time_stop, start_date, stop_date ' \
                  f'from schedule ' \
                  f'where week_day = {self.week_day_box.text()} ' \
                  f'and squad in ({", ".join(groups)})'
        schedule = cursor.execute(command).fetchall()  # расписание этих групп
        for elem in schedule:
            schedule_start = '-'.join(reversed(elem[2].split('.')))
            schedule_stop = '-'.join(reversed(elem[3].split('.')))
            if schedule_stop <= date_start or schedule_start >= date_stop:
                pass
            elif elem[1] <= time_start or elem[0] >= time_stop:
                pass
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ваши занятия будут пересекаться',
                                     QMessageBox.Ok)
                return
        else:
            if date_stop <= str(datetime.now().date()):
                QMessageBox.critical(self, 'Ошибка', 'Этот период уже прошел',
                                     QMessageBox.Ok)
                return
            command = f'select id ' \
                      f'from squads ' \
                      f'where title = \'{self.admin.group_box.currentText()}\''
            squad = cursor.execute(command).fetchone()[0]
            week_day = self.week_day_box.text()
            date_start = self.start_date.text()
            date_stop = self.stop_date.text()
            command = f'insert into ' \
                      f'schedule(week_day, time_start, time_stop, squad, start_date, stop_date) ' \
                      f'values(\'{week_day}\', \'{time_start}\', \'{time_stop}\', ' \
                      f'\'{squad}\', \'{date_start}\', \'{date_stop}\')'
            cursor.execute(command)
            self.connect.commit()
            signal()
            self.admin.cur_schedule_change()

