# В данной задаче Вам необходимо реализовать метод Секущих для функций двух типов:
# f0(x) = (c0x-1)2+4*(4-c1x)4
# f1(x) = c0(x-c1)+(x-c2)2
# Можете воспользоваться шаблоном (https://gist.github.com/evkonovalov/18cb3714ec48cc9b06313bbdc6120d9b).
#
# Формат ввода
# t - тип функции (0 или 1)
# с0...cn - коэффициенты целевой функции, где n это 1 или 2, в зависимости от типа
# x0 x1 k - первые две точки поиска и критерий остановки (|x - xnew| < k)
#
# Формат вывода
# Координата найденной точки.
# Проверяется точность до первых двух знаков после запятой.


def f0(x, coef):
    return (coef[0]*x-1)**2+4*(4-coef[1]*x)**4


def df0(x, coef):
    return 2*coef[0]*(coef[0]*x-1)-16*coef[1]*(4-coef[1]*x)**3


def f1(x, coef):
    return coef[0]*(x - coef[1]) + (x - coef[2])**2


def df1(x, coef):
    return coef[0] - 2*coef[2] + 2*x


def secant_search(f, df, x0, x1, coef, tol):
    x = x1
    ddf = (df(x, coef) - df(x0, coef)) / (x - x0)
    x_new = x - df(x, coef) / ddf

    while abs(x - x_new) >= tol:
        x_old = x
        x = x_new
        ddf = (df(x, coef) - df(x_old, coef)) / (x - x_old)
        x_new = x - df(x, coef) / ddf
    return x_new


typ = int(input())
f = f0 if (typ == 0) else f1
df = df0 if (typ == 0) else df1
coef = [i for i in map(float, input().split())]
x0, x1, tol = map(float, input().split())
r1 = secant_search(f, df, x0, x1, coef, tol)
print("{:.10f}".format(r1))
