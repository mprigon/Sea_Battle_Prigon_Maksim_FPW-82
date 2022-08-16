# FieldSeaBattle - класс игрового поля
import random
from ship import *
from exceptions import *


# поле игры
class FieldSeaBattle:
    # размер поля 6 * 6
    field_length = 6  # строки, х максимальное точки
    field_width = 6  # столбцы, y максимальное точки
    list_ships = [[1, 1, 3, 'Крейсер', 'К'], [2, 2, 2, 'Эсминец', 'Э'], [3, 4, 1, 'Подводная лодка', 'П']]
    # список возможных состояний клетки
    status_cell = [['free', 'o', 0], ['ship_acting', '■', 1], ['perimeter', '.', 2],
                   ['miss', 'T', 3], ['hit', 'X', 4]]
    # разрешенные значения координат x и y
    _x_y = [1, 2, 3, 4, 5, 6]

    def __init__(self, hide=False):
        self.hide = hide
        self.count = 0
        self.field = [[self.status_cell[0][1]] * self.field_width
                      for _i in range(0, self.field_length)]
        self.busy = []
        self.ships = []
        self.busy_and_perimeter = []
        self._list_shots = []

    # случайный выбор кормы корабля для случайного поля
    def random_x_y_direction(self, _ship_type):
        # _ship - тип корабля 1 - Крейсер, 2 - Эсминец, 3 - Подводная лодка
        # выбираем точку кормы (x, y), от которой вниз или вправо "растут" многопалубные корабли
        x = random.randint(1, self.field_length)
        y = random.randint(1, self.field_width)
        if _ship_type != 3:  # для крейсера и эсминца
            _direction = random.randint(0, 1)
        else:
            _direction = 0  # для подводной лодки условно 0

        _ship_input = [x, y, _direction]
        return _ship_input

    # создаем корабль как список Dot, с проверкой
    def random_add_ship(self, _ship_type, _ship, _field_busy_dot, _field_perimeter_dot):
        # _ship - тип корабля 1 - Крейсер, 2 - Эсминец, 3 - Подводная лодка

        _ship_name = self.list_ships[_ship_type - 1][3]
        _list_of_ship_dots = _ship.dots()  # список Dot клеток корабля

        # если неудачно, то исключение
        cond1 = self.is_place_for_ship(_list_of_ship_dots)
        cond2 = self.place_not_busy(_list_of_ship_dots, _field_busy_dot, _field_perimeter_dot)
        # print(f'{_ship_name} проверка условий есть место {cond1} место уже не занято {cond2}')
        if not cond1 or not cond2:
            # print(f'неудача с размещением {_ship_name}')
            # print(_list_of_ship_dots, _field_busy_dot, _field_perimeter_dot)
            raise FieldWrongShipException
        # print(f'успешно разместили {_ship_name}')
        for _i in _list_of_ship_dots:
            self.field[_i.x_dot - 1][_i.y_dot - 1] = self.status_cell[1][1]  # корабль '■'

        return _list_of_ship_dots

    # функция печати поля игры в консоль
    # на входе списки точек, занятых кораблями, входящих в периметр
    # печатается преобразованием списка-строки в строковую переменную
    def __str__(self):
        result = ''
        _rows = self.field_length
        _columns = self.field_width

        result += '  |\t1 |\t2 |\t3 |\t4 |\t5 |\t6 |'
        _i = 0
        for _row in self.field:
            _i += 1
            result += f"\n{str(_i)}" + " |\t" + " |\t".join(_row) + " |"

        if self.hide:
            result = result.replace('■', 'o')  # скрываем корабли для игрового поля противника

        return result

    # список точек периметра по списку точек корабля
    def list_dot_perimeter(self, _dots_ship):
        _perimeter_dot_list = []
        _length = self.field_length
        _width = self.field_width
        # список Dot всех клеток поля
        dot_list_field = [Dot(i, j) for i in range(1, _length + 1) for j in range(1, _width + 1)]
        for _i in _dots_ship:
            for _j in range(0, len(dot_list_field)):
                if _i.in_perimeter(dot_list_field[_j]) and (dot_list_field[_j] not in _dots_ship):
                    _perimeter_dot_list.append(dot_list_field[_j])

        # убираем повторяющиеся Dot из списка
        _perimeter = [_perimeter_dot_list[0]]
        for _i in range(1, len(_perimeter_dot_list)):
            if _perimeter_dot_list[_i] not in _perimeter:
                _perimeter.append(_perimeter_dot_list[_i])
        return _perimeter

    def show_perimeter(self, _perimeter, show=False):
        if show:
            for _i in _perimeter:
                self.field[_i.x_dot - 1][_i.y_dot - 1] = self.status_cell[2][1]  # по периметру '.'
        return 0

    # проверка вводимых координат на корректность - должно быть целое число от 1 до 6
    def permitted_x_y(self, direction):
        try:
            value = input(f'Введите координаты кормы корабля по {direction}: ')
            if not value.isdigit():
                print('некорректный ввод, может быть только целое число от 1 до 6')
                raise MyValueOutException
            else:
                if int(value) not in self._x_y:
                    print('некорректный ввод, может быть только целое число от 1 до 6')
                raise MyValueOutException
        except:
            while not value.isdigit() or int(value) not in self._x_y:
                value = input(f'повторно введите координаты кормы корабля по {direction}: ')
        finally:
            value_permitted = int(value)
            return value_permitted

    # запрос данных о корабле - координаты и направление
    def ask_x_y_direction(self, _ship):
        # _ship - тип корабля 1 - Крейсер, 2 - Эсминец, 3 - Подводная лодка
        # выбираем точку кормы (x, y), от которой вниз или вправо "растут" многопалубные корабли
        x = self.permitted_x_y('горизонтали')
        y = self.permitted_x_y('вертикали')
        print(f'Вы ввели точку кормы по горизонтали {x} по вертикали {y}')
        if _ship != 3:  # для крейсера и эсминца выбрать направление и добавить палубы (клетки)
            _direction = int(input('Задайте направление: 0 - вертикальное (палубы добавятся вниз)'
                                   '\n                     1 горизонтальное (палубы добавятся вправо)'))
        else:
            _direction = 0  # для подводной лодки условно 0

        _ship_input = [x, y, _direction]
        return _ship_input

    # проверяем, поместится ли корабль в пределах поля
    def is_place_for_ship(self, _ship_dot):
        is_place = False
        # проверка, находятся ли все клетки корабля в поле
        for _i in _ship_dot:
            if _i.x_dot > self.field_length or _i.y_dot > self.field_width:
                raise FieldWrongShipException
            else:
                is_place = True
        return is_place

    # проверка занятости клеток корабля клетками и периметрами других кораблей
    # сравниваются объекты класса Dot
    def place_not_busy(self, _ship_dot, _busy_dot, perimeter_dot):
        _place = True
        for _i in _ship_dot:
            if (_i in _busy_dot) or (_i in perimeter_dot):
                _place = False
                break  # как только одна клетка занята, либо в периметре - можно выходить
        return _place

    # постановка корабля на поле
    def manual_add_ship(self, _ship_type, _ship, _field_busy_dot, _field_perimeter_dot):
        # _ship_type - тип корабля 1 - Крейсер, 2 - Эсминец, 3 - Подводная лодка
        _ship_name = self.list_ships[_ship_type - 1][3]
        _list_of_ship_dots = _ship.dots()  # список Dot клеток корабля

        # если неудачно, то исключение
        cond1 = self.is_place_for_ship(_list_of_ship_dots)
        cond2 = self.place_not_busy(_list_of_ship_dots, _field_busy_dot, _field_perimeter_dot)
        # print(f'{_ship_name} проверка условий есть место {cond1} место уже не занято {cond2}')
        if not cond1 or not cond2:
            # print(f'неудача с размещением {_ship_name}')
            # print(_list_of_ship_dots, _field_busy_dot, _field_perimeter_dot)
            raise FieldWrongShipException
        # print(f'успешно разместили {_ship_name}')
        for _i in _list_of_ship_dots:
            self.field[_i.x_dot - 1][_i.y_dot - 1] = self.status_cell[1][1]  # корабль '■'

        return _list_of_ship_dots

    # клетка за пределами поля
    def out(self, _dot):
        _x_out = (1 <= _dot.x_dot <= self.field_length)
        _y_out = (1 <= _dot.y_dot <= self.field_length)
        _out = not (_x_out and _y_out)
        return _out

    # выстрел
    def shot(self, _d_shot):
        if self.out(_d_shot):
            raise FieldException()

        if _d_shot in self._list_shots:
            raise FieldException()

        self._list_shots.append(_d_shot)

        for _ship in self.ships:
            if _d_shot in _ship.dots():
                _ship.life -= 1
                self.field[_d_shot.x_dot - 1][_d_shot.y_dot - 1] = self.status_cell[4][1]  # попадание 'X'
                if _ship.life == 0:
                    self.count += 1
                    self.show_perimeter(self.list_dot_perimeter(_ship.dots()), True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[_d_shot.x_dot - 1][_d_shot.y_dot - 1] = self.status_cell[3][1]  # выстрел мимо, символ 'T'
        print('Мимо!')
        return False

    def begin(self):
        self._list_shots = []
