# В данной задаче Вам необходимо реализовать метод Хука — Дживса для функций двух типов:
# f0(x) = c0x14+c1x23+c2x22+c3x1+c4
# f1(x) = x12 + c0x1x2 + c1(x2-3)2
# Параметры для запуска: delta = [1,1], alpha = 2, lambda = 1. Можете воспользоваться шаблоном (https://gist.github.com/evkonovalov/404b07ba8f83e99a30936b1eec0bfa22).
#
# Формат ввода
# t - тип функции (0 или 1)
# с0...cn - коэффициенты целевой функции, где n это 4 или 1, в зависимости от типа
# x1 x2 - координаты начальной точки
# k - критерий остановки ( < k)
#
# Формат вывода
# Две координаты найденной точки, через пробел.
# Проверяется точность до первых двух знаков после запятой.

import numpy as np


def f0(x, coef):
    return coef[0]*x[0]**4 + coef[1]*x[1]**3 + coef[2]*x[1]**2 + coef[3]*x[0] + coef[4]


def f1(x,coef):
    return x[0]**2 + coef[0]*x[0]*x[1] + coef[1]*(x[1]-3)**2


def Hooke_Jeeves(f, x0, tol, coef):
    xs = list()
    xs.append(x0)
    delta = np.array([1.0, 1.0])
    al = 2
    lam = 1
    d = np.eye(2)
    y = [0, 0, 0]
    y[0] = x0
    k = 0
    i = 0
    while np.any(delta >= tol):
        if f(y[i] + delta * d[:, i], coef) < f(y[i], coef):
            y[i + 1] = y[i] + delta * d[:, i]
        elif f(y[i] - delta * d[:, i], coef) < f(y[i], coef):
            y[i + 1] = y[i] - delta * d[:, i]
        else:
            y[i + 1] = y[i]
        if i < 1:
            i += 1
        else:
            if f(y[2], coef) < f(xs[k], coef):
                xs.append(y[2])
                y = [0, 0, 0]
                y[0] = xs[k+1] + lam * (xs[k+1] - xs[k])
                i = 0
                k += 1
                continue
            else:
                if np.any(delta <= tol):
                    return xs[k]
                else:
                    delta[delta > tol] /= al
                    y = [0, 0, 0]
                    y[0] = xs[k]
                    xs.append(xs[k])
                    k += 1
                    i = 0
                    continue
    return xs[-1]


typ = int(input())
f = f0 if (typ == 0) else f1
coef = [i for i in map(float, input().split())]
x0 = np.array([i for i in map(float, input().split())])
tol = float(input())
r1 = Hooke_Jeeves(f, x0, tol, coef)
print("{:.10f} {:.10f}".format(r1[0], r1[1]))
