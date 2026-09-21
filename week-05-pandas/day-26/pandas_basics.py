import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print("Series из списка:")
print(s)
print()

s2 = pd.Series([100, 200, 300], index=['a', 'b', 'c'])
print("Series с индексами:")
print(s2)
print()

s3 = pd.Series({'Анна': 25, 'Борис': 30, 'Виктор': 35})
print("Series из словаря:")
print(s3)
print()

print(f"Значение по индексу 'b': {s2['b']}")
print(f"Значение по позиции 1: {s2.iloc[1]}")

print("\n" + "=" * 50)
print("DATAFRAME")
print("=" * 50 + "\n")

data = {
    'name': ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий'],
    'age': [25, 30, 35, 28, 42],
    'city': ['Москва', 'СПб', 'Казань', 'Москва', 'СПб'],
    'salary': [80000, 95000, 120000, 70000, 110000]
}

df = pd.DataFrame(data)
print("DataFrame из словаря:")
print(df)
print()

print("Форма (строки, столбцы):", df.shape)
print("Столбцы:", list(df.columns))
print("Типы данных:")
print(df.dtypes)
print()

print("Первые 3 строки:")
print(df.head(3))
print()

print("Последние 2 строки:")
print(df.tail(2))

print("\n" + "=" * 50)
print("ДОСТУП К ДАННЫМ")
print("=" * 50 + "\n")

print("Столбец 'name':")
print(df['name'])
print()

print("Столбцы 'name' и 'salary':")
print(df[['name', 'salary']])
print()

print("Строка 0:")
print(df.iloc[0])
print()

print("Строка с индексом 2:")
print(df.loc[2])
print()

print(f"Имя в строке 1: {df.loc[1, 'name']}")
print(f"Зарплата в строке 3: {df.loc[3, 'salary']}")

print("\n" + "=" * 50)
print("СТАТИСТИКА")
print("=" * 50 + "\n")

print("Сводка по числовым столбцам:")
print(df.describe())
print()

print(f"Средняя зарплата: {df['salary'].mean():.2f}")
print(f"Максимальная зарплата: {df['salary'].max()}")
print(f"Минимальная зарплата: {df['salary'].min()}")
print(f"Сумма зарплат: {df['salary'].sum()}")
print(f"Медиана возраста: {df['age'].median()}")

print("\n" + "=" * 50)
print("ПРОВЕРКА")
print("=" * 50 + "\n")

data_v2 = {
    'product': ['Ноутбук', 'Мышь', 'Клавиатура', 'Монитор', 'Принтер'],
    'price': [80000, 3000, 7000, 45000, 25000],
    'quantity': [15, 100, 50, 20, 10],
    'category': ['Электроника', 'Аксессуары', 'Аксессуары', 'Электроника', 'Электроника']
}

df_v2 = pd.DataFrame(data_v2)

print("Первые 3 строки:")
print(df_v2.head(3))
print()

print("Столбцы 'product' и 'price':")
print(df_v2[['product', 'price']])
print()

print(f"Средняя цена: {df_v2['price'].mean():.2f}")

df_v2['total'] = df_v2['price'] * df_v2['quantity']
print(df_v2)