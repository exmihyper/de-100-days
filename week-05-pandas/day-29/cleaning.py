import pandas as pd

df = pd.read_csv('dirty_data.csv')

print("=== ИСХОДНЫЕ ДАННЫЕ ===")
print(df)
print()

print(f"Размер: {df.shape}")
print(f"Столбцы: {list(df.columns)}")
print()

print("=== МАСКА ПРОПУСКОВ ===")
print(df.isnull())
print()

print("=== КОЛИЧЕСТВО ПРОПУСКОВ ПО СТОЛБЦАМ ===")
print(df.isnull().sum())
print()

print(f"Всего пропусков: {df.isnull().sum().sum()}")
print()

print("=== СТРОКИ С ПРОПУСКАМИ ===")
print(df[df.isnull().any(axis=1)])
print()

df_dropped = df.dropna()
print(f"После dropna(): {df_dropped.shape[0]} строк (было {df.shape[0]})")
print()

df_salary = df.dropna(subset=['salary'])
print(f"После dropna(subset=['salary']): {df_salary.shape[0]} строк")
print()

df_filled = df.copy()
df_filled['department'] = df_filled['department'].fillna('Unknown')
print("После fillna('Unknown') в department:")
print(df_filled['department'])
print()

df_mean = df.copy()
mean_salary = df_mean['salary'].mean()
df_mean['salary'] = df_mean['salary'].fillna(mean_salary)
print(f"Средняя зарплата: {mean_salary:.2f}")
print("После fillna(mean) в salary:")
print(df_mean['salary'])
print()

print(f"Строк с полными дубликатами: {df.duplicated().sum()}")
print()

print("=== ДУБЛИКАТЫ ===")
print(df[df.duplicated(keep=False)])  # keep=False показывает все вхождения
print()

df_unique = df.drop_duplicates()
print(f"После drop_duplicates(): {df_unique.shape[0]} строк (было {df.shape[0]})")
print()

duplicates = df.drop(columns=['id']).duplicated(keep=False)
print(f"Строк с дубликатами (без учёта id): {duplicates.sum()}")
print()
print("=== ДУБЛИКАТЫ ===")
print(df[duplicates])
print()


df_unique = df.drop_duplicates(subset=['name', 'department', 'salary', 'hire_date', 'email'])
print(f"После drop_duplicates(): {df_unique.shape[0]} строк (было {df.shape[0]})")
print()
print(df_unique)

df_clean = df_unique.copy()

df_clean['department'] = df_clean['department'].str.strip().str.capitalize()
print("Уникальные отделы после нормализации:")
print(df_clean['department'].unique())
print()

df_clean['name'] = df_clean['name'].str.strip()
print("Имена после strip:")
print(df_clean['name'].tolist())
print()

df_clean['hire_date'] = pd.to_datetime(df_clean['hire_date'], errors='coerce')
print("Типы после to_datetime:")
print(df_clean.dtypes)
print()

df_renamed = df_clean.rename(columns={
    'name': 'employee_name',
    'hire_date': 'start_date',
    'salary': 'monthly_salary'
})

print("После переименования:")
print(df_renamed.columns.tolist())
print()


df_final = (
    pd.read_csv('dirty_data.csv')
    .drop_duplicates(subset=['name', 'department', 'salary', 'hire_date', 'email'])
    .dropna(subset=['name', 'salary'])
    .assign(
        department=lambda x: x['department'].str.strip().str.lower().map({
            'it': 'IT',
            'hr': 'HR',
            'finance': 'Finance',
            'sales': 'Sales'
        }),
        hire_date=lambda x: pd.to_datetime(x['hire_date'], errors='coerce')
    )
)

print("=== ФИНАЛЬНЫЕ ДАННЫЕ ===")
print(df_final)
print()
print(f"Строк: {df_final.shape[0]}")
print(f"Пропусков: {df_final.isnull().sum().sum()}")
print()


df = pd.read_csv('dirty_data.csv')
rows_before = df.shape[0]
print(f"Строк до очистки: {rows_before}")
print()

df_clean = (
    df
    .drop_duplicates(subset=['name', 'department', 'salary', 'hire_date', 'email'])
    .dropna(subset=['name', 'salary'])
    .assign(department=lambda x: x['department'].str.strip().str.lower().map({
        'it': 'IT',
        'hr': 'HR',
        'finance': 'Finance',
        'sales': 'Sales'
    }))
    .query("department in ['IT', 'Finance']")
)

rows_after = df_clean.shape[0]
print(f"Строк после очистки: {rows_after}")
print(f"Удалено: {rows_before - rows_after}")
print()

print("=== ЧИСТЫЕ ДАННЫЕ ===")
print(df_clean)
print()

df_clean.to_csv('clean_data.csv', index=False, encoding='utf-8')
print("Сохранено в clean_data.csv")