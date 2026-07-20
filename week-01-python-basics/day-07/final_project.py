import sys
import csv
import json
import os


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        rows = list(reader)
    return headers, rows


def is_number(value):
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


def get_numeric_columns(headers, rows):
    numeric_cols = []
    
    for col_index, header in enumerate(headers):
        sample_size = min(5, len(rows))
        is_numeric = True
        
        for row in rows[:sample_size]:
            if not is_number(row[col_index]):
                is_numeric = False
                break
        
        if is_numeric and sample_size > 0:
            numeric_cols.append((col_index, header))
    
    return numeric_cols


def calculate_stats(rows, col_index):
    values = []
    for row in rows:
        value = row[col_index]
        if is_number(value):
            values.append(float(value))
    
    if not values:
        return {'sum': 0, 'avg': 0, 'min': 0, 'max': 0, 'count': 0}
    
    return {
        'sum': sum(values),
        'avg': sum(values) / len(values),
        'min': min(values),
        'max': max(values),
        'count': len(values)
    }


def get_top_products(rows, product_col, quantity_col):
    product_totals = {}
    
    for row in rows:
        product = row[product_col]
        quantity_str = row[quantity_col]
        
        if is_number(quantity_str):
            quantity = int(quantity_str)
            if product in product_totals:
                product_totals[product] += quantity
            else:
                product_totals[product] = quantity
    
    sorted_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_products


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"\nОтчёт сохранён в '{filename}'")


def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите имя CSV-файла!")
        print("Пример: python final_project.py sales.csv")
        return
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден!")
        return
    
    headers, rows = read_csv(filename)
    
    print(f"\nФайл: {filename}")
    print(f"Столбцы: {headers}")
    print(f"Строк: {len(rows)}")
    
    numeric_cols = get_numeric_columns(headers, rows)
    
    if not numeric_cols:
        print("В файле нет числовых столбцов!")
        return
    
    print(f"\n=== СТАТИСТИКА ПО ЧИСЛОВЫМ СТОЛБЦАМ ===")
    
    all_stats = {}
    for col_index, col_name in numeric_cols:
        col_stats = calculate_stats(rows, col_index)
        all_stats[col_name] = col_stats
        
        print(f"\n{col_name}:")
        print(f"  Сумма: {col_stats['sum']}")
        print(f"  Среднее: {col_stats['avg']:.2f}")
        print(f"  Минимум: {col_stats['min']}")
        print(f"  Максимум: {col_stats['max']}")
        print(f"  Количество: {col_stats['count']}")
    
    product_col = None
    quantity_col = None
    
    for i, header in enumerate(headers):
        if header.lower() in ['product', 'товар', 'продукт']:
            product_col = i
        if header.lower() in ['quantity', 'количество', 'qty']:
            quantity_col = i
    
    top_products = []
    if product_col is not None and quantity_col is not None:
        print(f"\n=== ТОП-3 ТОВАРОВ ПО КОЛИЧЕСТВУ ===")
        top_products = get_top_products(rows, product_col, quantity_col)
        
        for i, (product, total_qty) in enumerate(top_products[:3], start=1):
            print(f"{i}. {product}: {total_qty} шт.")
    else:
        print(f"\nСтолбцы 'product' и 'quantity' не найдены — пропускаем топ товаров.")
    
    report = {
        'source_file': filename,
        'total_rows': len(rows),
        'columns': headers,
        'numeric_stats': all_stats,
        'top_products': [{'product': p, 'total_quantity': q} for p, q in top_products[:3]]
    }
    
    output_file = 'report.json'
    save_json(report, output_file)


if __name__ == "__main__":
    main()