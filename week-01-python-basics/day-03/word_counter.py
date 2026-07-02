def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return None



def clean_words(text):
    words = text.split()
    cleaned = []
    for word in words:
        clean = word.lower().strip('.,!?()[]{}"\'')
        cleaned.append(clean)
    return cleaned



def count_words(word_list):
    counts = {}
    for word in word_list:
        if word in counts:
            counts[word] += 1 
        else:
            counts[word] = 1
    return counts



def get_top_words(word_counts, min_length=4, top_n=10):
    filtered = []
    for word, count in word_counts.items():
        if len(word) >= min_length:
            filtered.append((word, count))
            
    sorted_words = sorted(filtered, key=lambda x: x[1], reverse=True)
    return sorted_words[:top_n]



def main():
    filename = 'sample.txt'
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