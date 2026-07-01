import random

def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите число!")

def main():
    secret = random.randint(1, 100)
    attempts = 0
    
    print("Я загадал число от 1 до 100. Попробуй угадать!")

    while True:
        guess = get_number("Твоя догадка: ")
        attempts = attempts + 1

        if guess == secret:
            print(f"Угадали! Загадано число {secret}.")
            print(f"Попыток: {attempts}")
            break
        elif guess < secret:
            print("Больше!")            
        else:
            print("Меньше!")  



if __name__ == "__main__":
    main()