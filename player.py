# класс игрока

from field import *


class Player:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    # запрос хода у игрока
    def ask(self):
        raise NotRealizedAtPlayerError()

    def move(self):
        while True:
            try:
                _move = self.ask()
                _move_again = self.enemy.shot(_move)  # True, если по правилам игры ход можно повторить
                return _move_again
            except FieldException as error:
                print(error)


class User(Player):
    player_moves = []  # список ранее сделанных ходов

    def ask(self):

        # список допустимых цифр в ходе в виде строковых переменных
        possible_moves = ['1', '2', '3', '4', '5', '6']
        try:
            # insert_move - список строковых переменных хода
            print('Введите свой ход:')
            insert_move = list(map(str, input('номер строки и номер '
                                              'столбца, между ними пробел:').split()))

            # проверка ввода хода из двух допустимых цифр и без повтора хода
            inserted_ = len(insert_move)
            if inserted_ != 2:
                raise ShouldBeTwoException()
            if insert_move[0] not in possible_moves:
                raise FieldOutException('номер строки должен быть от 1 до 6')
            if insert_move[1] not in possible_moves:
                raise FieldOutException('Номер столбца должен быть от 1 до 6')
            if Dot(int(insert_move[0]), int(insert_move[1])) in self.player_moves:
                raise FieldShotException()

        except ShouldBeTwoException:
            print('Должно быть два аргумента x и y')
            print('Повторно введите ход:')
            while True:
                insert_move = list(map(str, input('строка, пробел и столбец:').split()))
                inserted_ = len(insert_move)
                if inserted_ == 2:
                    break
        except FieldOutException:
            print('Попытка выстрелить за пределы поля')
            print('Повторно введите ход, диапазон клеток от 1 до 6:')
            while True:
                insert_move = list(map(str, input('строка, пробел и столбец:').split()))
                if insert_move[0] in possible_moves and insert_move[1] in possible_moves:
                    break
        except FieldShotException:
            print('Вы уже стреляли в эту клетку')
            print('Повторно введите ход, посмотрите, куда Вы уже стреляли:')
            while True:
                insert_move = list(map(str, input('строка, пробел и столбец:').split()))
                if Dot(int(insert_move[0]), int(insert_move[1])) not in self.player_moves:
                    break
        else:
            print('ход принят')

        x = int(insert_move[0])
        y = int(insert_move[1])
        self.player_moves.append(Dot(x, y))

        return Dot(x, y)


class AI(Player):
    ai_moves = []  # список ранее сделанных ходов

    # переопределяем метод, чтобы ход ИИ был случайным
    # запрещено стрелять туда, куда уже стреляли
    def ask(self):
        while True:
            x = random.randint(1, 6)
            y = random.randint(1, 6)
            move_ai = Dot(x, y)
            if move_ai not in self.ai_moves:
                break

        print(f'Ход Компьютера: {x} {y}')

        return move_ai
