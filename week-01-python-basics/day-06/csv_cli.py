import sys
import csv
import os


def show_menu():
    """Выводит меню действий."""
    print("\n=== CSV АНАЛИЗАТОР ===")
    print("1. Показать все данные")
    print("2. Показать заголовки столбцов")
    print("3. Показать сумму по числовому столбцу")
    print("4. Отфильтровать строки")
    print("5. Выход")


def is_number(value):
    """Проверяет, можно ли превратить строку в число."""
    value = value.strip()
    if not value:
        return False
    try:
        int(value)
        return True
    except ValueError:
        pass
    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите имя CSV-файла!")
        print("Пример: python csv_cli.py sales.csv")
        return
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден!")
        return
    
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        rows = list(reader)
    
    print(f"\nФайл: {filename}")
    print(f"Столбцы: {', '.join(headers)}")
    print(f"Строк: {len(rows)}")
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Выберите действие (1-5): "))
        except ValueError:
            print("Ошибка: введите число от 1 до 5!")
            continue
        
        if choice == 1:
            print(f"\n=== ВСЕ ДАННЫЕ ({len(rows)} строк) ===")
            print("\t".join(headers))
            print("-" * 50)
            for row in rows:
                print("\t".join(row))
        
        elif choice == 2:
            print(f"\n=== ЗАГОЛОВКИ СТОЛБЦОВ ===")
            for i, header in enumerate(headers, start=1):
                print(f"{i}. {header}")
        
        elif choice == 3:
            print(f"\n=== СУММА ПО СТОЛБЦУ ===")
            for i, header in enumerate(headers, start=1):
                print(f"{i}. {header}")
            
            try:
                col_choice = int(input("Выберите номер столбца: "))
                if col_choice < 1 or col_choice > len(headers):
                    print("Ошибка: неверный номер столбца!")
                    continue
            except ValueError:
                print("Ошибка: введите число!")
                continue
            
            col_index = col_choice - 1
            column_name = headers[col_index]
            
            total = 0
            count_numbers = 0
            count_skipped = 0
            
            for row in rows:
                value = row[col_index]
                if is_number(value):
                    total += float(value)
                    count_numbers += 1
                else:
                    count_skipped += 1
            
            print(f"\nСтолбец: {column_name}")
            print(f"Сумма: {total}")
            print(f"Числовых значений: {count_numbers}")
            if count_skipped > 0:
                print(f"Пропущено (не числа): {count_skipped}")
        
        elif choice == 4:
            # Фильтрация строк
            print(f"\n=== ФИЛЬТРАЦИЯ СТРОК ===")
            for i, header in enumerate(headers, start=1):
                print(f"{i}. {header}")
            
            try:
                col_choice = int(input("Выберите номер столбца для фильтрации: "))
                if col_choice < 1 or col_choice > len(headers):
                    print("Ошибка: неверный номер столбца!")
                    continue
            except ValueError:
                print("Ошибка: введите число!")
                continue
            
            col_index = col_choice - 1
            column_name = headers[col_index]
            
            # Запрашиваем значение для поиска
            search_value = input(f"Введите значение для поиска в столбце '{column_name}': ")
            
            # Ищем строки, где значение в столбце СОДЕРЖИТ искомую подстроку
            # .lower() для регистронезависимого поиска
            found_rows = []
            for row in rows:
                if search_value.lower() in row[col_index].lower():
                    found_rows.append(row)
            
            # Выводим результат
            if len(found_rows) == 0:
                print(f"\nСтрок со значением '{search_value}' в столбце '{column_name}' не найдено.")
            else:
                print(f"\n=== НАЙДЕНО СТРОК: {len(found_rows)} ===")
                print("\t".join(headers))
                print("-" * 50)
                for row in found_rows:
                    print("\t".join(row))
        
        elif choice == 5:
            print("До свидания!")
            break
        
        else:
            print("Ошибка: выберите число от 1 до 5!")


if __name__ == "__main__":
    main()