def read_file(filename):
    """Читает текстовый файл и возвращает его содержимое.
    
    Аргументы:
        filename (str): путь к файлу
    
    Возвращает:
        str: содержимое файла или None, если файл не найден
    """
    try:
        # with — конструкция, которая автоматически закроет файл
        # Даже если внутри блока возникнет ошибка
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return None


def clean_words(text):
    """Разбивает текст на слова, приводит к нижнему регистру, убирает пунктуацию.
    
    Аргументы:
        text (str): исходный текст
    
    Возвращает:
        list: список очищенных слов
    """
    words = text.split()
    cleaned = []
    for word in words:
        # Очищаем слово от знаков пунктуации и приводим к нижнему регистру
        clean = word.lower().strip('.,!?()[]{}"\'')
        cleaned.append(clean)
    return cleaned


def count_words(word_list):
    """Подсчитывает частоту каждого слова в списке.
    
    Аргументы:
        word_list (list): список слов
    
    Возвращает:
        dict: словарь {слово: количество}
    """
    counts = {}
    for word in word_list:
        if word in counts:
            counts[word] += 1  # Короткая запись counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts


def get_top_words(word_counts, min_length=4, top_n=10):
    """Отбирает топ-N самых частых слов длиной не менее min_length.
    
    Аргументы:
        word_counts (dict): словарь {слово: количество}
        min_length (int): минимальная длина слова
        top_n (int): сколько слов вернуть
    
    Возвращает:
        list: список кортежей (слово, количество)
    """
    filtered = []
    for word, count in word_counts.items():
        if len(word) >= min_length:
            filtered.append((word, count))
    
    # Сортировка по количеству (второй элемент кортежа), по убыванию
    sorted_words = sorted(filtered, key=lambda x: x[1], reverse=True)
    
    # Возвращаем первые top_n элементов
    return sorted_words[:top_n]


def main():
    """Главная функция: читает файл, считает слова, выводит результат."""
    
    # Имя файла — можно изменить на любое
    filename = 'sample.txt'
    
    # Читаем файл
    text = read_file(filename)
    
    # Если файл не прочитался (None) — выходим
    if text is None:
        return
    
    # Очищаем слова
    words = clean_words(text)
    print(f"Всего слов в файле: {len(words)}")
    
    # Считаем частоту
    counts = count_words(words)
    print(f"Уникальных слов: {len(counts)}")
    
    # Получаем топ-10
    top_words = get_top_words(counts, min_length=4, top_n=10)
    
    # Выводим результат
    print("\n=== ТОП-10 СЛОВ (длиной от 4 букв) ===")
    for i, (word, count) in enumerate(top_words, start=1):
        print(f"{i}. {word}: {count}")


if __name__ == "__main__":
    main()