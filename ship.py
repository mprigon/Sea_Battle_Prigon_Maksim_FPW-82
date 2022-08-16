# Dot - класс точек на поле, координаты точки - x, y - новый тип данных
# Ship - класс корабля
class Dot:
    def __init__(self, x_dot, y_dot):
        self.x_dot = x_dot
        self.y_dot = y_dot

    # примеры на сайте https://pythonworld.ru/osnovy/peregruzka-operatorov.html
    # переопределяем метод равенства, чтобы сравнивать объекты Dot
    def __eq__(self, other):
        return self.x_dot == other.x_dot and self.y_dot == other.y_dot

    # наглядная печать объекта Dot
    def __repr__(self):
        return f'Dot({self.x_dot}, {self.y_dot})'

    # введем условное "расстояние" между клеткой 1 и клеткой 2
    # если это расстояние равно 1, тогда клетка 2 входит в периметр клетки 1
    def in_perimeter(self, other):
        delta_x = abs(self.x_dot - other.x_dot)
        delta_y = abs(self.y_dot - other.y_dot)

        return (delta_x == 0 and delta_y == 1 or delta_x == 1 and delta_y == 0
                or delta_x == 1 and delta_y == 1)


class Ship:
    # в конструктор передается информация
    # x, y координаты кормы корабля
    # ship_length - длина, измеряется в клетках от кормы
    # ship_direction - направление: 0 - вертикально, 1 - горизонтально
    # life - количество жизней

    def __init__(self, x, y, ship_length, ship_direction):
        self.x = x
        self.y = y
        self.ship_length = ship_length
        self.ship_direction = ship_direction
        self.life = ship_length  # начальная величина

    # возвращает список Dot всех точек корабля: [Dot(x,y), Dot(x1, y1), ]
    def dots(self):
        ship_dots = []
        if self.ship_length == 1:
            ship_dots.append(Dot(self.x, self.y))  # подводная лодка
        else:
            if self.ship_direction == 0:  # корабль вертикально
                for i in range(0, self.ship_length):
                    ship_dots.append(Dot(self.x + i, self.y))
            else:  # корабль горизонтально
                for i in range(0, self.ship_length):
                    ship_dots.append(Dot(self.x, self.y + i))
        return ship_dots

    # определяет попадание выстрела в клетку корабля
    def hit(self, _shot):
        return _shot in self.dots()
