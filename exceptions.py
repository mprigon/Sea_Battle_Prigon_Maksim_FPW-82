# классы исключений

class MyCustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            # можно вывести значение, вызвавшее прерывание
            return f'MyCustomError, {0} '.format(self.message)
        else:
            return 'MyCustomError has been raised'


class FieldException(MyCustomError):
    def __str__(self):
        return 'Ошибка при вводе хода'


class ShouldBeTwoException(MyCustomError):
    def __str__(self):
        return 'В ходе должно быть два аргумента'


class FieldOutException(MyCustomError):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за границами поля'


class FieldShotException(MyCustomError):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class NotRealizedAtPlayerError(MyCustomError):
    def __str__(self):
        return 'На уровне класса Player метод не реализован, переопределяется в наследниках'


class ValueError(MyCustomError):
    def __str__(self):
        return 'Некорректный ввод хода игрока!'


class MyValueOutException(MyCustomError):
    pass


class FieldWrongShipException(MyCustomError):
    def __str__(self):
        return 'Ошибка размещения корабля'
