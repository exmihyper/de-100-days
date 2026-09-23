import pandas as pd


df = pd.read_csv('employees.csv', parse_dates=['hire_date'])

print("=== ИСХОДНЫЕ ДАННЫЕ ===")
print(df)
print()

df_high = df[df['salary'] > 100000]
print("=== Зарплата > 100000 ===")
print(df_high)
print()

df_it = df[df['department'] == 'IT']
print("=== Отдел IT ===")
print(df_it)
print()

df_new = df[df['hire_date'] > '2020-01-01']
print("=== Наняты после 2020 ===")
print(df_new)
print()

df_it_high = df[(df['department'] == 'IT') & (df['salary'] > 100000)]
print("=== IT с зарплатой > 100000 ===")
print(df_it_high)
print()

df_hr_fin = df[(df['department'] == 'HR') | (df['department'] == 'Finance')]
print("=== HR или Finance ===")
print(df_hr_fin)
print()

df_not_it = df[~(df['department'] == 'IT')]
print("=== НЕ IT ===")
print(df_not_it)
print()

df_in = df[df['department'].isin(['IT', 'HR'])]
print("=== Отдел IT или HR (через isin) ===")
print(df_in)
print()

df_range = df[df['salary'].between(90000, 120000)]
print("=== Зарплата от 90000 до 120000 ===")
print(df_range)
print()

df_search = df[df['name'].str.contains('ан', case=False)]
print("=== Имя содержит 'ан' ===")
print(df_search)
print()

grouped = df.groupby('department')['salary'].mean()
print("=== Средняя зарплата по отделам ===")
print(grouped)
print()

result = df.groupby('department')['salary'].agg(['count', 'mean', 'min', 'max', 'sum'])
print("=== Полная статистика по отделам ===")
print(result)
print()

result.columns = ['кол-во', 'средняя', 'минимум', 'максимум', 'сумма']
print("=== С переименованными столбцами ===")
print(result)
print()

df_sorted = df.sort_values('salary', ascending=False)
print("=== Сортировка по зарплате (убывание) ===")
print(df_sorted)
print()

df_multi = df.sort_values(['department', 'salary'], ascending=[True, False])
print("=== Сначала отдел (А-Я), потом зарплата (убывание) ===")
print(df_multi)
print()



df_it = df[df['salary'].between(90000, 130000)]
print(df_it)
print()

df_it = df_it[df_it['department'] == 'IT']
print(df_it)
print()

df_it = df_it.groupby('department')['salary'].agg(['mean', 'count'])
print(df_it)
print()

df_it = df_it.sort_values('mean', ascending=False)
print(df_it)