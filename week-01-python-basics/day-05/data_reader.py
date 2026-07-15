import csv
import json  



def read_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Ошибка: файл конфигурации '{config_file}' не найден!")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка: '{config_file}' содержит некорректный JSON!")
        return None



def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Результат сохранён в '{filename}'")



def main():
    config = read_config('config.json')
    if config is None:
        return
    
    
    filename = config['input_file']
    output_file = config['output_file']
    
    
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        
        
        total_rows = 0
        total_quantity = 0
        total_revenue = 0
        region_stats = {}
        
        
        for row in reader:
            total_rows += 1
            
            quantity = int(row[2])
            price = int(row[3])
            region = row[4]
            
            total_quantity += quantity
            total_revenue += quantity * price
            
            
            if region not in region_stats:
                region_stats[region] = {
                    'quantity': 0,
                    'revenue': 0
                }
            
            
            region_stats[region]['quantity'] += quantity
            region_stats[region]['revenue'] += quantity * price
    
    
    result = {
        'summary': {
            'total_rows': total_rows,
            'total_quantity': total_quantity,
            'total_revenue': total_revenue
        },
        'by_region': region_stats
    }
    
   
   
    print(f"\n=== ОБЩАЯ СТАТИСТИКА ===")
    print(f"Всего записей: {total_rows}")
    print(f"Всего продано товаров: {total_quantity}")
    print(f"Общая выручка: {total_revenue} руб.")
    
    print(f"\n=== СТАТИСТИКА ПО РЕГИОНАМ ===")
    for region, stats in region_stats.items():
        print(f"{region}: продано {stats['quantity']} шт., выручка {stats['revenue']} руб.")
    
  
    save_json(result, output_file)




if __name__ == "__main__":
    main()