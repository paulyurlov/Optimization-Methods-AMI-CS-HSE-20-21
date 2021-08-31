# В данной задаче Вам необходимо найти минимум функции при помощи методов интервального анализа для функций:
#
# Критерии остановки:
# ширина интервала значения целевой функции меньше
# количество итераций меньше 1000
# Можете воспользоваться шаблоном (https://gist.github.com/evkonovalov/fa49c81d2b5ee91aeb9db640ce4c5660)
# Формат ввода
# t - тип функции
# a b - коэффициенты
#  - критерии остановки
# x0 x1 x2 x3 - начало и конец интервалов [x0,x1] и [x2,x3] - области поиска
#
# Формат вывода
# Минимальное значение целевой функции на заданном пространстве.

import math
import numpy as np
from queue import PriorityQueue


class Interval:

    def __init__(self, x):
        self.x = x.copy()

    def __repr__(self):
        return "[" + str(round(self.x[0], 3)) + ", " + str(round(self.x[1], 3)) + "]"

    def mid(self):
        return 0.5 * (self.x[0] + self.x[1])

    def width(self):
        return self.x[1] - self.x[0]

    def scale(self, factor):
        m = 0.5 * (self.x[0] + self.x[1])
        r = 0.5 * (self.x[1] - self.x[0])
        self.x[0] = m - factor * r
        self.x[1] = m + factor * r

    def isIn(self, other):
        return (self.x[0] >= other.x[0]) and (self.x[1] <= other.x[1])

    def isNoIntersec(self, other):
        return (self.x[0] > other.x[1]) or (self.x[1] < other.x[0])

    def intersec(self, other):
        if self.x[0] > self.x[1]:
            raise ValueError(other.x[0], other.x[1], "results in wrong bounds:", self.x[0], self.x[1])
        return Interval([max(self.x[0], other.x[0]), min(self.x[1], other.x[1])])

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x.__setitem__(key, value)

    def __neg__(self):
        ninterval = Interval(self.x)
        ninterval.x[0] = - self.x[1]
        ninterval.x[1] = - self.x[0]
        return ninterval

    def __add__(self, other):
        ointerval = valueToInterval(other)
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] + ointerval.x[0]
        ninterval.x[1] = self.x[1] + ointerval.x[1]
        return ninterval

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ointerval = valueToInterval(other)
        ninterval = Interval(self.x)
        ninterval.x[0] = self.x[0] - ointerval.x[1]
        ninterval.x[1] = self.x[1] - ointerval.x[0]
        return ninterval

    def __rsub__(self, other):
        ointerval = valueToInterval(other)
        return ointerval.__sub__(self)

    def __pow__(self, other):
        ninterval = Interval(self.x)
        u = self.x[0] ** other
        v = self.x[1] ** other
        if other == 0:
            ninterval.x[0] = 1
            ninterval.x[1] = 1
        elif other % 2 == 0:
            ninterval.x[1] = max(u, v)
            if self.x[0] <= 0 and self.x[1] >= 0:
                ninterval.x[0] = 0
            else:
                ninterval.x[0] = min(u, v)
        else:
            ninterval.x[0] = u
            ninterval.x[1] = v
        return ninterval

    def __mul__(self, other):
        ointerval = valueToInterval(other)
        v = [self.x[0] * ointerval.x[0], self.x[0] * ointerval.x[1], self.x[1] * ointerval.x[0],
             self.x[1] * ointerval.x[1]]
        b = [min(v), max(v)]
        return Interval(b)

    def __truediv__(self, other):
        ointerval = valueToInterval(other)
        v = [self.x[0] / ointerval.x[0], self.x[0] / ointerval.x[1], self.x[1] / ointerval.x[0],
             self.x[1] / ointerval.x[1]]
        b = [min(v), max(v)]
        return Interval(b)

    def __floordiv__(self, other):
        ointerval = valueToInterval(other)
        v = [self.x[0] // ointerval.x[0], self.x[0] // ointerval.x[1], self.x[1] // ointerval.x[0],
             self.x[1] // ointerval.x[1]]
        b = [min(v), max(v)]
        return Interval(b)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __lt__(self, other):
        if self.width() < other.width():
            return True
        return False


def valueToInterval(expr):
    if isinstance(expr, int):
        etmp = Interval([expr, expr])
    elif isinstance(expr, float):
        etmp = Interval([expr, expr])
    else:
        etmp = expr
    return etmp


def sin(x):
    if isinstance(x, (int, np.integer)):
        return math.sin(x)
    elif isinstance(x, (float, np.float)):
        return math.sin(x)
    else:
        y = [math.sin(x[0]), math.sin(x[1])]
        pi2 = 2 * math.pi
        pi05 = math.pi / 2
        if math.ceil((x[0] - pi05) / pi2) <= math.floor((x[1] - pi05) / pi2):
            b = 1
        else:
            b = max(y)

        if math.ceil((x[0] + pi05) / pi2) <= math.floor((x[1] + pi05) / pi2):
            a = -1
        else:
            a = min(y)
        return Interval([a, b])


def cos(x):
    if isinstance(x, (int, np.integer)):
        return math.cos(x)
    elif isinstance(x, (float, np.float)):
        return math.cos(x)
    else:
        y = [math.cos(x[0]), math.cos(x[1])]
        pi2 = 2 * math.pi
        if math.ceil(x[0] / pi2) <= math.floor(x[1] / pi2):
            b = 1
        else:
            b = max(y)
        if math.ceil((x[0] - math.pi) / pi2) <= math.floor((x[1] - math.pi) / pi2):
            a = -1
        else:
            a = min(y)
        return Interval([a, b])


def exp(x):
    return Interval([math.exp(x[0]), math.exp(x[1])])


def abs(x):
    if x[1] < 0:
        return Interval([-x[0], -x[1]])
    elif x[0] < 0 and x[1] > 0:
        if -x[0] > x[1]:
            return Interval([x[1], -x[0]])
        else:
            return Interval([-x[0], x[1]])
    else:
        return Interval([x[0], x[1]])


def log(x, base):
    if base > 1:
        return Interval([math.log(x[0], base), math.log(x[1], base)])
    else:
        return Interval([math.log(x[1], base), math.log(x[0], base)])


def f1(x, a, b):
    return (x[0] - x[1] ** 2) ** 2 + (a - x[0]) ** 2 + b


def f2(x, a, b):
    return a * sin(x[0]) + b * cos(x[1])


def dev(inter):
    tmp = inter.mid()
    return Interval([inter[0], tmp]), Interval([tmp, inter[1]])


def halve(lst):
    if lst[0].width() >= lst[1].width():
        left, right = dev(lst[0])
        return [left, lst[1]], [right, lst[1]]
    left, right = dev(lst[1])
    return [lst[0], left], [lst[0], right]


def bnb_ival_glob(f, ini_box, eps=1e-12, M=1e3):
    queue_ = PriorityQueue(maxsize=0)
    queue_.put([f(ini_box)[0], ini_box])
    for step in range(int(M)):
        best_ = queue_.get()[1]
        if f(best_).width() < eps:
            return f(best_)[0]
        left, right = halve(best_)
        queue_.put([f(left)[0], left])
        queue_.put([f(right)[0], right])
    return queue_.get()[0]


typ = int(input())
a, b = map(int, input().split())
if typ == 0:
    f = lambda x_: f1(x_, a, b)
else:
    f = lambda x_: f2(x_, a, b)
eps1 = float(input())
a1, a2, a3, a4 = map(int, input().split())
x1 = Interval([a1, a2])
x2 = Interval([a3, a4])
x = [x1, x2]
print(bnb_ival_glob(f, x, eps1))
