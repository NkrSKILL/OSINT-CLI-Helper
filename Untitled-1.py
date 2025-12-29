def factorial(n):
    if n < 0:
        return None
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# Пример использования
number = int(input("Введите число для вычисления факториала: "))
result = factorial(number)
if result is not None:
    print(f"Факториал {number} равен {result}")
else:
    print("Ошибка: введено отрицательное число.") 