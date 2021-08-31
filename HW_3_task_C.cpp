// В данной задаче Вам необходимо решить классическую задачу о рюкзаке.
//
// Формат ввода
// Количество предметов
// Веса предметов
// Ценность предметов
// Размер рюкзака
//
// Формат вывода
// Вес оптимального рюкзака и его ценность через пробел

#include <iostream>
#include <vector>

int kp(const std::vector<int>& prices, const std::vector<int>& weights, int n, int W){

    std::vector<std::vector<int>> F(2, std::vector<int>(W+1));
    for (int i = 0; i < n; ++i)  {
        if (i % 2 != 0) {
            for (int j = 0; j < W+1; ++j) {
                if (weights[i] <= j) {
                    F[1][j] = std::max(prices[i] + F[0][j - weights[i]],
                                         F[0][j]);
                }
                else {
                    F[1][j] = F[0][j];
                }
            }

        }
        else
        {
            for (int j = 0; j < W+1; ++j)  {
                if (weights[i] <= j) {
                    F[0][j] = std::max(prices[i] + F[1][j - weights[i]],
                                    F[1][j]);
                }
                else {
                    F[0][j] = F[1][j];
                }
            }
        }
    }

    return (n%2 != 0)? F[0][W] : F[1][W];
}

int main() {
    int n = 0;
    int c = 0;
    std::cin >> n;
    std::vector<int> w;
    w.reserve(n);
    std::vector<int> p;
    p.reserve(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> w[i];
    }
    for (int i = 0; i < n; ++i) {
        std::cin >> p[i];
    }
    std::cin >> c;
    int ans = kp(p,w,n, c);
    std::cout << c << ' ' << ans;
    return 0;
}
