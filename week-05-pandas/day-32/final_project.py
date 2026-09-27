import pandas as pd
import matplotlib.pyplot as plt
import json


df = pd.read_csv('orders_dirty.csv')

print("=== ФОРМА ===")
print(f"Строк: {df.shape[0]}, Столбцов: {df.shape[1]}")
print()

print("=== ТИПЫ ===")
print(df.dtypes)
print()

print("=== ПРОПУСКИ ===")
print(df.isnull().sum())
print()

print(f"Всего пропусков: {df.isnull().sum().sum()}")

print("\n" + "=" * 50)
print("ЭТАП 2: ОЧИСТКА")
print("=" * 50)

rows_before = df.shape[0]

df = df.drop_duplicates(subset=['order_id'])
print(f"После удаления дубликатов: {df.shape[0]} (было {rows_before})")

rows_before = df.shape[0]

df = df.dropna(subset=['customer_name', 'quantity', 'price'])
print(f"После удаления пропусков: {df.shape[0]} (было {rows_before})")

df['customer_name'] = df['customer_name'].str.strip().str.title()
df['status'] = df['status'].str.strip().str.lower()
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

print("\nУникальные имена:", df['customer_name'].unique())
print("Уникальные статусы:", df['status'].unique())
print("\n=== ДАННЫЕ ПОСЛЕ ОЧИСТКИ ===")
print(df)

print("\n" + "=" * 50)
print("ЭТАП 3: АНАЛИЗ")
print("=" * 50)

df['total'] = df['quantity'] * df['price']

df_delivered = df[df['status'] == 'delivered'].copy()
print(f"Доставленных заказов: {df_delivered.shape[0]} из {df.shape[0]}")

total_revenue = df_delivered['total'].sum()
total_orders = df_delivered.shape[0]
avg_check = df_delivered['total'].mean()

print(f"Общая выручка: {total_revenue:,.0f} руб.")
print(f"Доставленных заказов: {total_orders}")
print(f"Средний чек: {avg_check:,.0f} руб.")

top_customers = df_delivered.groupby('customer_name')['total'].sum().nlargest(3)
print("\nТОП-3 КЛИЕНТА:")
print(top_customers)

top_products = df_delivered.groupby('product')['quantity'].sum().nlargest(3)
print("\nТОП-3 ТОВАРА ПО КОЛИЧЕСТВУ:")
print(top_products)

print("\n" + "=" * 50)
print("ЭТАП 4: ВИЗУАЛИЗАЦИЯ")
print("=" * 50)

revenue_by_product = df_delivered.groupby('product')['total'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
plt.bar(revenue_by_product.index, revenue_by_product.values, color='steelblue', edgecolor='black')
plt.title('Выручка по товарам', fontsize=14, fontweight='bold')
plt.xlabel('Товар')
plt.ylabel('Выручка, руб.')
plt.grid(True, alpha=0.3, axis='y')

for i, v in enumerate(revenue_by_product.values):
    plt.text(i, v + 1000, f'{v:,.0f}', ha='center', fontsize=9)
    
plt.tight_layout()
plt.savefig('revenue_by_product.png', dpi=100)
plt.show()
print("Сохранён revenue_by_product.png")

revenue_by_customer = df_delivered.groupby('customer_name')['total'].sum()

plt.figure(figsize=(9, 9))
plt.pie(revenue_by_customer.values,
        labels=revenue_by_customer.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6'])
plt.title('Доля клиентов в выручке', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('revenue_by_customer.png', dpi=100)
plt.show()
print("Сохранён revenue_by_customer.png")

print("\n" + "=" * 50)
print("ЭТАП 5: ОТЧЁТ")
print("=" * 50)

report = {
    'summary': {
        'total_revenue': float(total_revenue),
        'total_orders': int(total_orders),
        'avg_check': float(avg_check)
    },
    'top_customers': [
        {'name': name, 'revenue': float(rev)}
        for name, rev in top_customers.items()
    ],
    'top_products': [
        {'name': name, 'quantity': float(qty)}
        for name, qty in top_products.items()
    ]
}

with open('report.json', 'w', encoding='utf-8') as file:
    json.dump(report, file, ensure_ascii=False, indent=2)
    
print("Отчёт сохранён в report.json")
print()
print(json.dumps(report, ensure_ascii=False, indent=2))