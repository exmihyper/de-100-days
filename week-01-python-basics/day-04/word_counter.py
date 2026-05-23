# from модуль import функция — импортирует конкретную функцию
# Теперь можно вызывать её напрямую, без имени модуля
from file_utils import read_file
from text_utils import clean_words, count_words, get_top_words


def main():
    """Главная функция: читает файл, считает слова, выводит результат."""
    
    filename = 'sample.txt'
    
    # Вызываем функции напрямую, без префикса модуля
    text = read_file(filename)
    
    if text is None:
        return
    
    words = clean_words(text)
    print(f"Всего слов в файле: {len(words)}")
    
    counts = count_words(words)
    print(f"Уникальных слов: {len(counts)}")
    
    top_words = get_top_words(counts, min_length=4, top_n=10)
    
    print("\n=== ТОП-10 СЛОВ (длиной от 4 букв) ===")
    for i, (word, count) in enumerate(top_words, start=1):
        print(f"{i}. {word}: {count}")


if __name__ == "__main__":
    main()