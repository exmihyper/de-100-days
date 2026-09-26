import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sales_data = pd.DataFrame({
    'month': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
    'revenue': [120000, 135000, 98000, 150000, 175000, 160000],
    'orders': [45, 52, 38, 61, 70, 65]
})

print("=== ДАННЫЕ ===")
print(sales_data)
print()

plt.figure(figsize=(10, 5))

plt.plot(sales_data['month'], sales_data['revenue'],
         marker='o',          
         color='steelblue',
         linewidth=2,
         label='Выручка')

plt.title('Выручка по месяцам', fontsize=14, fontweight='bold')
plt.xlabel('Месяц')
plt.ylabel('Выручка, руб.')

plt.grid(True, alpha=0.3)

plt.legend()

plt.tight_layout()
plt.savefig('line_chart.png', dpi=100)
plt.show()
print("Сохранён line_chart.png")

plt.figure(figsize=(10, 5))

plt.bar(sales_data['month'], sales_data['orders'],
        color='coral',
        edgecolor='black',
        linewidth=1)

plt.title('Количество заказов по месяцам', fontsize=14, fontweight='bold')
plt.xlabel('Месяц')
plt.ylabel('Заказов')

for i, v in enumerate(sales_data['orders']):
    plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
    
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('bar_chart.png', dpi=100)
plt.show()
print("Сохранён bar_chart.png")

plt.figure(figsize=(10, 5))

plt.barh(sales_data['month'], sales_data['revenue'],
         color='mediumseagreen')

plt.title('Выручка по месяцам (горизонтально)', fontsize=14, fontweight='bold')
plt.xlabel('Выручка, руб.')
plt.ylabel('Месяц')

plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('barh_chart.png', dpi=100)
plt.show()
print("Сохранён barh_chart.png")


np.random.seed(42)
salaries = np.random.normal(loc=100000, scale=25000, size=500)

plt.figure(figsize=(10, 5))

plt.hist(salaries, bins=30, color='purple', alpha=0.7, edgecolor='black')

plt.axvline(salaries.mean(), color='red', linestyle='--',
            linewidth=2, label=f'Среднее: {salaries.mean():.0f}')

plt.title('Распределение зарплат', fontsize=14, fontweight='bold')
plt.xlabel('Зарплата, руб.')
plt.ylabel('Количество сотрудников')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('histogram.png', dpi=100)
plt.show()
print("Сохранён histogram.png")

categories = ['Электроника', 'Одежда', 'Книги', 'Спорт']
revenues = [450000, 180000, 95000, 220000]

plt.figure(figsize=(8, 8))

plt.pie(revenues,
        labels=categories,
        autopct='%1.1f%%',          
        startangle=90,               
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
        explode=[0.05, 0, 0, 0])    

plt.title('Доля выручки по категориям', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('pie_chart.png', dpi=100)
plt.show()
print("Сохранён pie_chart.png")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(sales_data['month'], sales_data['revenue'],
             marker='o', color='steelblue', linewidth=2)
axes[0].set_title('Выручка по месяцам')
axes[0].set_xlabel('Месяц')
axes[0].set_ylabel('Выручка, руб.')
axes[0].grid(True, alpha=0.3)

axes[1].bar(sales_data['month'], sales_data['orders'], color='coral')
axes[1].set_title('Заказы по месяцам')
axes[1].set_xlabel('Месяц')
axes[1].set_ylabel('Заказов')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('subplots.png', dpi=100)
plt.show()
print("Сохранён subplots.png")


df = pd.read_csv('employees.csv')

avg_by_dept = df.groupby('department')['salary'].mean()
plt.figure(figsize=(8, 5))
plt.bar(avg_by_dept.index, avg_by_dept.values)
plt.title('Средняя зарплата по отделам')
plt.xlabel('Отдел')
plt.ylabel('Зарплата, руб.')
plt.savefig('avg_salary_by_dept.png')
plt.show()

counts = df['department'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
plt.title('Доля сотрудников по отделам')
plt.savefig('employees_by_dept.png')
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(df['salary'], bins=10)
plt.title('Распределение зарплат')
plt.xlabel('Зарплата, руб.')
plt.ylabel('Количество сотрудников')
plt.savefig('salary_distribution.png')
plt.show()