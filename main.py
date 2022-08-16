# Итоговое практическое задание по модулю C2.5
# Игра "Морской бой"
# выполнил: Пригон Максим, FPW-82

# класс игры
# параметры - игрок, его доска, ИИ, его доска
from player import *
from field import *
from exceptions import *
from ship import *
import random


class Game:

    def __init__(self):
        print('Игра Морской Бой. Вашим противником будет компьютер.')
        print('Сейчас компьютер размещает корабли на своем поле')
        computer = self.random_field()
        computer.hide = True
        print('Приступим к размещению Ваших кораблей:')
        manual = int(input('0 - Ваши корабли размещает компьютер \n1 - Вы вручную сами размещаете свои корабли: '))
        if not manual:
            player = self.random_field()
        else:
            player = self.manual_field()

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def random_field(self):
        field = None
        while field is None:
            field = self.try_random_field()
        return field

    # создание случайного расположения кораблей
    def try_random_field(self):
        attempts = 0
        field = FieldSeaBattle()
        _busy_dot = []
        _perimeter_dot = []
        for _i in [1, 2, 2, 3, 3, 3, 3]:
            while True:
                attempts += 1
                if attempts > 2000:
                    print('Выполнено более 2000 неудачных попыток разместить корабли случайным образом')
                    return None
                _ship_data = field.random_x_y_direction(_i)
                x, y, _direction = _ship_data[0], _ship_data[1], _ship_data[2]
                _length = field.list_ships[_i - 1][2]
                _ship = Ship(x, y, _length, _direction)
                try:
                    _ship_add = field.random_add_ship(_i, _ship, _busy_dot, _perimeter_dot)
                    _busy_dot += _ship_add
                    _ship_perimeter = field.list_dot_perimeter(_ship_add)
                    _perimeter_dot += _ship_perimeter
                    field.ships.append(_ship)
                    break
                except FieldWrongShipException:
                    pass

        print('все корабли размещены автоматически!')
        field.busy_and_perimeter = [_busy_dot, _perimeter_dot]

        return field

    # создаем игровое поле Игрока, который сам расставляет корабли
    def manual_field(self):
        field = None
        while field is None:
            field = self.try_manual_field()
        return field

    # расставляем корабли вручную
    def try_manual_field(self):
        all_placed = False  # становится True, когда все 7 кораблей размещены
        field = FieldSeaBattle()
        _busy_dot = []
        _perimeter_dot = []

        while not all_placed:  # цикл размещения кораблей вручную
            print('Устанавливаем в следующем порядке: '
                  '1 - Крейсер, 2 - Эсминец (2 шт.), 3 - Подводная лодка (4 шт.)')
            print('Сначала разместите корабли на бумаге в клеточку')

            _j, _k = 0, 0  # счетчики кораблей по типам
            for _i in [1, 2, 2, 3, 3, 3, 3]:
                if _i == 1:  # Крейсер
                    print('размещаем Крейсер')
                if _i == 2:  # эсминец - 2 корабля
                    _j += 1
                    print(f'размещаем 2 эсминца: {_j}')
                if _i == 3:  # подводная лодка - 4 корабля
                    _k += 1
                    print(f'размещаем 4 подводные лодки: {_k}')

                try:
                    _ship_data = field.ask_x_y_direction(_i)
                    x, y, _direction = _ship_data[0], _ship_data[1], _ship_data[2]
                    _length = field.list_ships[_i - 1][2]
                    _ship = Ship(x, y, _length, _direction)

                    _ship_add = field.manual_add_ship(_i, _ship, _busy_dot, _perimeter_dot)
                    # print(_ship_add)
                    _busy_dot += _ship_add  # дополняем список объектов Dot занятых кораблями клеток
                    # print(f'список занятых кораблями клеток {_busy_dot}')
                    list_ship_perimeter = field.list_dot_perimeter(_ship_add)
                    _perimeter_dot += list_ship_perimeter  # дополняем точками периметра
                    # print(f'список занятых клеток периметра {_perimeter_dot}')
                    field.ships.append(_ship)
                    print(f'Вы успешно установили {field.list_ships[_i - 1][3]}')
                except FieldWrongShipException:
                    print('попробуйте еще раз')
                    _ship_data = field.ask_x_y_direction(_i)
                    x, y, _direction = _ship_data[0], _ship_data[1], _ship_data[2]
                    _length = field.list_ships[_i - 1][2]
                    _ship = Ship(x, y, _length, _direction)

            if len(field.ships) == 7:
                print('Все корабли размещены Вами вручную!')
                print(field)
                all_placed = True
                field.busy_and_perimeter = [_busy_dot, _perimeter_dot]
                break

            print(f'Корабли не установлены, только {len(field.ships)} из 7, попробуйте еще раз')

        return field

    # привествие пользователю, информация
    def hello(self):

        print('Компьютер стреляет случайно, но не может повторять свои выстрелы, как и Вы')
        print('ход вводится двумя координатами через пробел: x y')
        print('x - строка, y - столбец.')

        return 0

    def game_cycle(self, who_moves_first):
        num = 0
        while True:
            print('-' * 20)
            print('Ваше игровое поле:')
            print(self.us.player)
            print('-' * 20)
            print('Игровое поле Компьютера:')
            print(self.ai.player)

            if who_moves_first:
                if num % 2 == 0:
                    print("-" * 20)
                    print("Ходит пользователь!")
                    repeat = self.us.move()
                else:
                    print("-" * 20)
                    print("Ходит компьютер!")
                    repeat = self.ai.move()
                if repeat:
                    num -= 1
            else:
                if num % 2 == 0:
                    print("-" * 20)
                    print("Ходит компьютер!")
                    repeat = self.ai.move()
                else:
                    print("-" * 20)
                    print("Ходит пользователь!")
                    repeat = self.us.move()
                if repeat:
                    num -= 1

            if self.ai.player.count == 7:
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.us.player.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    # начало игры, случайным образом выбирается, кто ходит первым
    def start(self):
        choice = random.randint(1, 2)
        if choice == 1:
            print('Ваш ход первый.')
            player_begins = True
        else:
            print('Компьютер ходит первым.')
            player_begins = False

        self.hello()
        self.game_cycle(player_begins)


mygame = Game()
mygame.start()
