# В данной задаче Вам необходимо решить задачу упаковки ящиков (https://ru.wikipedia.org/wiki/Задача_об_упаковке_в_контейнеры).
#
# Формат ввода
# Количество предметов
# Веса предметов через пробел
# Вместимость одного ящика
#
# Формат вывода
# Минимальное количество ящиков, необходимое для упаковки всех предметов.

def get_data():
    return int(input()), list(map(int, input().split())), int(input())


def fill_containers(n, w, c):
    w.sort(reverse=True)
    containers = [c]
    answer = 1
    for i in range(n):
        flag_not_found = True
        for j in range(len(containers)):
            if containers[j] - w[i] >= 0:
                containers[j] -= w[i]
                flag_not_found = False
                break
        if flag_not_found:
            containers.append(c - w[i])
            answer += 1
    return answer


print(fill_containers(*get_data()))
