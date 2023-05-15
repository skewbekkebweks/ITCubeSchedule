def password_check(text: str) -> tuple:
    """Проверка пароля по критериям"""
    if text:
        sequence = 'qwertyuiop asdfghjkl zxcvbnm йцукенгшщзхъ фывапролджэё ячсмитьбю'
        if len(text) <= 8:
            return 'Длина пароля должна быть больше 8 символов', 'red', 0
        elif not text.isalnum():
            return 'В пароле могут содержаться только буквы и цифры', 'red', 0
        elif text.isalpha():
            return 'В пароле должна быть хотя бы одна цифра', 'red', 0
        elif text.isdigit() or text.islower() or text.isupper():
            return 'В пароле должны присутсвовать большие ' \
                   'и маленькие буквы любого алфавита', 'red', 0
        elif any([text[i:i + 3].lower() in sequence for i in
                  range(len(text) - 2)]):
            return 'В пароле нет ни одной комбинации из 3 буквенных символов, стоящих рядом ' \
                   'в строке клавиатуры независимо от того, русская раскладка выбрана ' \
                   'или английская', 'red', 0
        else:
            return '', 'green', 1
    else:
        return '', '', 0
