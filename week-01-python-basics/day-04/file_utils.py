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