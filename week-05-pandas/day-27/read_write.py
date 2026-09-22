import pandas as pd

df = pd.read_csv("employees.csv")

print("=== DataFrame из CSV ===")
print(df)
print()

print("Типы данных:")
print(df.dtypes)
print()

df = pd.read_csv("employees.csv", parse_dates=["hire_date"])

print("Типы после parse_dates:")
print(df.dtypes)
print()

df_names = pd.read_csv("employees.csv", usecols=['name', 'salary'])
print("Только name и salary:")
print(df_names)
print()

df_indexed = pd.read_csv('employees.csv', index_col='id')
print("С индексом по id:")
print(df_indexed)
print()

df_head = pd.read_csv('employees.csv', nrows=3)
print("Первые 3 строки:")
print(df_head)
print()

df = pd.read_csv('employees.csv', parse_dates=['hire_date'])

print(df)

df.to_csv('employees_out.csv', index=False, encoding='utf-8')
print("Сохранено в employees_out.csv")

df.to_json('employees.json', orient='records', force_ascii=False, indent=2)
print("Сохранено в employees.json")

df.to_excel('employees.xlsx', sheet_name='Employees', index=False)
print("Сохранено в employees.xlsx")

print()

df_from_json = pd.read_json('employees.json')
print("Данные из JSON:")
print(df_from_json)
print()

print("Типы данных из JSON:")
print(df_from_json.dtypes)

df_from_excel = pd.read_excel('employees.xlsx', sheet_name='Employees')
print("Данные из Excel:")
print(df_from_excel)
print()

df = pd.read_csv('employees.csv')
df_it = df[df['department'] == 'IT']
df_it = df_it[['name', 'salary']]
df_it = df_it.sort_values('salary', ascending=False)
df_it.to_json('it_employees.json', orient='records', force_ascii=False, indent=2)

print("IT-сотрудники (отсортированы по зарплате):")
print(df_it)
print()
print("Сохранено в it_employees.json")