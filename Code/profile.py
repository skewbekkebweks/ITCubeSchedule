from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow
from Code.change_login_and_password import ChangeLoginPassword
from Design.profile import Ui_Profile
from constants import PHOTO, SIZE
from Code.notification import signal


class Profile(Ui_Profile, QMainWindow):
    """Профиль преподавателя"""

    def __init__(self, connect, main_window) -> None:
        super().__init__()
        self.setupUi(self)  # подключение дизайна
        self.connect = connect  # подключение к БД
        self.main_window = main_window  # главное окно
        self.change_photo_btn.clicked.connect(self.change_photo)
        self.delete_photo_btn.clicked.connect(self.delete_photo)
        self.change_login_password_btn.clicked.connect(self.change_login_password)
        self.update_info()  # обновление информации

    def update_info(self) -> None:
        """Обновление информации профиля"""
        cursor = self.connect.cursor()
        command = f'select name, photo ' \
                  f'from teachers ' \
                  f'where id = \'{self.main_window.cur_profile}\''
        res = cursor.execute(command).fetchone()  # полное имя и сохранённая фотография преподавателя
        if res[1] is None:  # проверка на то, сохранена ли какая-либо фотография
            pixmap = QPixmap(PHOTO).scaled(SIZE, SIZE)
        else:
            pixmap = QPixmap(res[1]).scaled(SIZE, SIZE)
        self.label_photo.setPixmap(pixmap)  # установка фотографии
        # установка имени
        self.label_name.setText(res[0].split()[1])
        self.label_surname.setText(res[0].split()[0])
        self.label_patronymic.setText(res[0].split()[2])

    def change_photo(self) -> None:
        """Смена фотографии"""
        photos_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]  # выбор фото
        cursor = self.connect.cursor()
        # проверка на то, выбрал ли преподаватель фотографию, обновление фотографии
        if photos_name:
            command = f'update teachers ' \
                      f'set photo = \'{photos_name}\' ' \
                      f'where id = \'{self.main_window.cur_profile}\''
            cursor.execute(command)
            self.connect.commit()
            signal()
            self.update_info()

    def delete_photo(self) -> None:
        """Удаление фотографии"""
        reply = QMessageBox.question(self, 'Выход',
                                     'Вы уверены, что хотите удалить фотографию?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            cursor = self.connect.cursor()
            command = f'update teachers ' \
                      f'set photo = null ' \
                      f'where id = \'{self.main_window.cur_profile}\''
            cursor.execute(command)
            self.connect.commit()
            signal()
            self.update_info()

    def change_login_password(self) -> None:
        """Смена логина и пароля"""
        self.change_login_password_ = ChangeLoginPassword(self.connect, self.main_window)
        self.change_login_password_.setWindowModality(Qt.ApplicationModal)  # установка модальности
        self.change_login_password_.show()  # показ окна
