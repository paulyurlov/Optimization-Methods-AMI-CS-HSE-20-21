# В данной задаче Вам необходимо реализовать метод Фибоначчи для функций двух типов:
# f0(x) = c0x2+c1x+c2
# f1(x) = c0x4+c1x3+c2x2+c3x+c4
# В качестве параметра  для последнего шага возьмите значение  = 0.01. На последнем шаге Вы должны отнять  от p = 0.5 и сделать последнюю итерацию алгоритма.
# Можете воспользоваться шаблоном (https://gist.github.com/evkonovalov/8b532b16ed954b95dfc2768130d62175).
#
# Формат ввода
# t - тип функции (0 или 1)
# с0...cn - коэффициенты целевой функции, где n это 3 или 5, в зависимости от типа
# l r k - границы интервала поиска и критерий остановки (|r - l| ≤ k)
#
# Формат вывода
# Cередина интервала неопределенности.
# Проверяется с точностью 1.0E-2.




def f0(x, coef):
    return coef[0]*x**2 + coef[1]*x + coef[2]


def f1(x, coef):
    return coef[0]*x**4 + coef[1]*x**3 + coef[2]*x**2 + coef[3]*x + coef[4]


def fib(n):
    if n in [0, 1]:
        return 1
    return fib(n - 1) + fib(n - 2)


def best_fib(bounds, length):
    aim = abs(bounds[1] - bounds[0]) / length
    for i in range(int(aim)):
        if fib(i) > aim:
            return i


def fib_search(f, bounds, tol, coef, max_eps=0.01):
    n = best_fib(bounds, tol)
    y = 0
    z = 0
    for k in range(n + 1):
        if k == 0:
            y = bounds[0] + fib(n-2) / fib(n) * (bounds[1] - bounds[0])
            z = bounds[0] + fib(n-1) / fib(n) * (bounds[1] - bounds[0])
        f_y = f(y, coef)
        f_z = f(z, coef)

        if f_y <= f_z:
            bounds[1] = z
            z = y
            y = bounds[0] + fib(n-k-3) / fib(n-k-1) * (bounds[1] - bounds[0])
        else:
            bounds[0] = y
            y = z
            z = bounds[0] + fib(n-k-2) / fib(n-k-1) * (bounds[1] - bounds[0])

        if k == n - 3:
            y_1 = y
            z_1 = y_1 + max_eps
            f_y = f(y_1, coef)
            f_z = f(z_1, coef)

            if f_y <= f_z:
                bounds[1] = z_1
            else:
                bounds[0] = y_1
            return (bounds[1] + bounds[0]) / 2

    return 0


inlet = int(input())
f = f0 if (inlet == 0) else f1
coef = [i for i in map(float, input().split())]
bounds = [0, 0]
bounds[0], bounds[1], tol = map(float, input().split())

r1 = fib_search(f, bounds, tol, coef)
print("{:.10f}".format(r1))
