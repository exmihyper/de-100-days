# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def get_number(prompt):
    """Запрашивает у пользователя число с защитой от неверного ввода.
    
    Аргументы:
        prompt (str): Текст подсказки, что показать пользователю
    
    Возвращает:
        int: Целое число, которое ввёл пользователь
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите число!")


def show_menu():
    """Выводит главное меню калькулятора."""
    print("=== КАЛЬКУЛЯТОР ===")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. История операций")
    print("6. Выход")


# ========== ОСНОВНАЯ ЛОГИКА ==========

def main():
    """Главная функция: цикл меню, обработка выбора, история операций."""
    
    # Список для хранения истории операций
    history = []

    while True:
        show_menu()

        # Защищённый ввод пункта меню
        try:
            choice = int(input("Выберите действие (1-6): "))
        except ValueError:
            print("Ошибка: введите число от 1 до 6!")
            continue  # Возврат в начало цикла

        # --- Сложение ---
        if choice == 1:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            result = a + b
            print(f"Результат: {result}")
            history.append(f"{a} + {b} = {result}")

        # --- Вычитание ---
        elif choice == 2:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            result = a - b
            print(f"Результат: {result}")
            history.append(f"{a} - {b} = {result}")

        # --- Умножение ---
        elif choice == 3:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            result = a * b
            print(f"Результат: {result}")
            history.append(f"{a} * {b} = {result}")

        # --- Деление ---
        elif choice == 4:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            if a == 0 or b == 0:
                print("Ошибка: деление на ноль!")
                history.append(f"{a} / {b} = ОШИБКА (деление на ноль)")
            else:
                result = a / b
                print(f"Результат: {result}")
                history.append(f"{a} / {b} = {result}")

        # --- История ---
        elif choice == 5:
            if len(history) == 0:
                print("История пуста")
            else:
                print("=== ИСТОРИЯ ОПЕРАЦИЙ ===")
                for record in history:
                    print(record)

        # --- Выход ---
        elif choice == 6:
            print("До свидания!")
            break  # Выход из цикла while, завершение программы

        # --- Неверный пункт ---
        else:
            print("Ошибка: выберите число от 1 до 6!")


# ========== ТОЧКА ВХОДА ==========

# Эта конструкция означает: "Запусти main(), только если файл выполняется напрямую,
# а не импортируется как модуль в другом скрипте"
# __name__ — специальная переменная Python. Когда файл запущен напрямую, она равна "__main__"
if __name__ == "__main__":
    main()