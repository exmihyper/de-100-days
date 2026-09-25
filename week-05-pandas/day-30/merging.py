import pandas as pd

users = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'name': ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий'],
    'city': ['Москва', 'СПб', 'Казань', 'Москва', 'СПб']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106],
    'user_id': [1, 1, 2, 3, 3, 99],  
    'product': ['Ноутбук', 'Мышь', 'Клавиатура', 'Монитор', 'Принтер', 'Флешка'],
    'amount': [80000, 3000, 7000, 45000, 25000, 2000]
})

print("=== USERS ===")
print(users)
print()
print("=== ORDERS ===")
print(orders)
print()

merged_inner = pd.merge(users, orders, on='user_id', how='inner')
print("=== INNER JOIN ===")
print(merged_inner)
print()


merged_left = pd.merge(users, orders, on='user_id', how='left')
print("=== LEFT JOIN ===")
print(merged_left)
print()

merged_right = pd.merge(users, orders, on='user_id', how='right')
print("=== RIGHT JOIN ===")
print(merged_right)
print()

merged_outer = pd.merge(users, orders, on='user_id', how='outer')
print("=== OUTER JOIN ===")
print(merged_outer)
print()

orders_renamed = orders.rename(columns={'user_id': 'customer_id'})

merged_diff = pd.merge(
    users, orders_renamed,
    left_on='user_id',
    right_on='customer_id',
    how='inner'
)
print("=== JOIN С РАЗНЫМИ ИМЕНАМИ ===")
print(merged_diff)
print()

df1 = pd.DataFrame({
    'city': ['Москва', 'Москва', 'СПб', 'СПб'],
    'region': ['Центр', 'Юг', 'Север', 'Центр'],
    'population': [12_000_000, 5_000_000, 5_500_000, 2_000_000]
})

df2 = pd.DataFrame({
    'city': ['Москва', 'Москва', 'СПб'],
    'region': ['Центр', 'Юг', 'Центр'],
    'area': [1000, 500, 800]
})

merged_multi = pd.merge(df1, df2, on=['city', 'region'], how='inner')
print("=== MERGE ПО ДВУМ СТОЛБЦАМ ===")
print(merged_multi)
print()

january = pd.DataFrame({
    'product': ['Ноутбук', 'Мышь'],
    'amount': [80000, 3000]
})

february = pd.DataFrame({
    'product': ['Клавиатура', 'Монитор', 'Мышь'],
    'amount': [7000, 45000, 2500]
})

concat_rows = pd.concat([january, february], ignore_index=True)
print("=== CONCAT (по строкам) ===")
print(concat_rows)
print()

merged = pd.merge(users, orders, on='user_id', how='inner')

total_by_user = merged.groupby('name')['amount'].agg(['sum', 'count'])
total_by_user.columns = ['сумма', 'кол-во_заказов']
total_by_user = total_by_user.sort_values('сумма', ascending=False)

print("=== СУММА ЗАКАЗОВ ПО ПОЛЬЗОВАТЕЛЯМ ===")
print(total_by_user)
print()

products = pd.DataFrame({
    'product_id': [1, 2, 3, 4],
    'name': ['Ноутбук', 'Мышь', 'Клавиатура', 'Монитор'],
    'price': [80000, 3000, 7000, 45000]
})

order_items = pd.DataFrame({
    'order_id': [101, 101, 102, 103, 103, 104],
    'product_id': [1, 2, 3, 1, 4, 99],   # 99 — нет такого товара
    'quantity': [1, 2, 1, 1, 2, 5]
})


merged = pd.merge(products, order_items, on='product_id', how='inner')
print(merged)
print()

merged['total'] = merged['price'] * merged['quantity']
print(merged)

merged = merged.groupby('name')['total'].agg(['sum'])
print(merged)

merged = merged.sort_values('sum', ascending=False)
print(merged)