def hanoi(n, source, target, auxiliary, state):
    if n == 1:
        # Перемістити один диск безпосередньо
        print(f"Перемістити диск з {source} на {target}: {state[source][-1]}")
        state[target].append(state[source].pop())
        print(f"Проміжний стан: {state}")
    else:
        # Рекурсивно переміщуємо n-1 дисків на допоміжний стрижень
        hanoi(n - 1, source, auxiliary, target, state)
        
        # Переміщуємо найбільший диск на кінцевий стрижень
        print(f"Перемістити диск з {source} на {target}: {state[source][-1]}")
        state[target].append(state[source].pop())
        print(f"Проміжний стан: {state}")
        
        # Рекурсивно переміщуємо n-1 дисків з допоміжного на кінцевий стрижень
        hanoi(n - 1, auxiliary, target, source, state)


# Введення кількості дисків
n = int(input("Введіть кількість дисків: "))

# Початковий стан стрижнів
state = {
    'A': list(range(n, 0, -1)),  # Всі диски на стрижні A
    'B': [],  # Порожній стрижень B
    'C': []   # Порожній стрижень C
    }

print(f"Початковий стан: {state}")

# Виклик функції для вирішення Ханойських башт
hanoi(n, 'A', 'C', 'B', state)

print(f"Кінцевий стан: {state}")