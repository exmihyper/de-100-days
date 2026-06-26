def show_menu():
    print("=== КАЛЬКУЛЯТОР ===")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. История операций")
    print("6. Выход")

def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите число!")

def main():          
    history = []
    
    while True:
        show_menu()
        try:
            choice = int(input("Выберите действие (1-6): "))
            print(f"Вы выбрали: {choice}")
        except ValueError:
            print("Ошибка: введите число от 1 до 6!")
            continue

        if choice == 1:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")      
            print(f"Результат: {a + b}")
            history.append(f"{a} + {b} = {a + b}")
                
        elif choice == 2:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            print(f"Результат: {a - b}")
            history.append(f"{a} - {b} = {a - b}")
            
        elif choice == 3:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            print(f"Результат: {a * b}")
            history.append(f"{a} * {b} = {a * b}")
            
        elif choice == 4:
            a = get_number("Первое число: ")
            b = get_number("Второе число: ")
            if b == 0:
                print("Ошибка: деление на ноль!")
            else:
                print(f"Результат: {a / b}")
                history.append(f"{a} / {b} = {a / b}")
                
        elif choice == 5:
            if len(history) == 0:
                print("История пуста")
            else:
                for record in history:
                    print(record)

        elif choice == 6:
            print("Выход")
            break        
        
        else:
            print("Ошибка: выберите число от 1 до 6!") 
            
                   
if __name__ == "__main__":
    main()