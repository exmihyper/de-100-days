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