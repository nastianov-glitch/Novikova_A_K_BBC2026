import pandas as pd

# Загружаем файл
df = pd.read_csv('/Users/anastasiia/Novikova_A_K_BBC2026/titanic/tested.csv')
print("Файл успешно загружен!")

# --- ЧАСТЬ II ---
print("\n--- ЧАСТЬ II ---")
n = int(input("Сколько первых строк показать? Введите число: "))
print(df.head(n))  # Показываем первые n строк

print("\nПоследние 5 строк:")
print(df.tail(5))

print("\nРазмер таблицы (строк, столбцов):", df.shape)
print("Названия столбцов:", list(df.columns))
print("\nТипы данных:")
print(df.dtypes)

# Статистика (среднее, медиана, мин, макс, стандартное отклонение)
print("\nСтатистика числовых столбцов:")
print(df[['Age', 'Fare', 'Pclass']].describe().loc[['mean', '50%', 'min', 'max', 'std']])

print("\nСколько пассажиров в каждом классе:")
print(df['Pclass'].value_counts())

print("\nУникальные порты посадки (Embarked):")
print(df['Embarked'].unique())


# --- ЧАСТЬ III ---
print("\n--- ЧАСТЬ III ---")
print("Пропуски в столбцах:")
print(df.isna().sum())

# Заполняем пропуски в возрасте медианой
median_age = df['Age'].median()
df['Age'] = df['Age'].fillna(median_age)
print("\nПропуски в Age заполнены медианой:", median_age)

# Удаляем пустые Embarked и столбец Cabin
df = df.dropna(subset=['Embarked'])
df = df.drop(columns=['Cabin'])
print("Удален столбец Cabin и пустые строки Embarked.")
print("Новый размер таблицы:", df.shape)


# --- ЧАСТЬ IV ---
print("\n--- ЧАСТЬ IV ---")
print("Общий процент выживших:", df['Survived'].mean() * 100)

print("\nВыживаемость по полу (в %):")
print(df.groupby('Sex')['Survived'].mean() * 100)

print("\nСредний возраст по полу:")
print(df.groupby('Sex')['Age'].mean())

print("\nЦена билета (мин, макс, средняя):")
print(df['Fare'].min(), df['Fare'].max(), df['Fare'].mean())


# --- ЧАСТЬ V ---
print("\n--- ЧАСТЬ V ---")
# Мужчины старше 30 в 1 классе
q1 = df[(df['Sex'] == 'male') & (df['Age'] > 30) & (df['Pclass'] == 1)]
print("Мужчин >30 лет в 1 классе:", len(q1))

# Женщины или дети, которые выжили
q2 = df[((df['Age'] < 18) | (df['Sex'] == 'female')) & (df['Survived'] == 1)]
print("Выживших женщин и детей:", len(q2))

# 3 класс, билет дороже среднего
avg_fare_3 = df[df['Pclass'] == 3]['Fare'].mean()
q3 = df[(df['Pclass'] == 3) & (df['Fare'] > avg_fare_3)]
print("Пассажиров 3 класса с дорогим билетом:", len(q3))

# Возраст 20-40, порт S
q4 = df[(df['Age'] >= 20) & (df['Age'] <= 40) & (df['Embarked'] == 'S')]
print("Пассажиров 20-40 лет из порта S:", len(q4))


# --- ЧАСТЬ VI ---
print("\n--- ЧАСТЬ VI ---")
print("Группировка по классу и полу:")
print(df.groupby(['Pclass', 'Sex'])['Survived'].mean() * 100)

print("\nГруппировка по порту (процент выживших):")
print(df.groupby('Embarked')['Survived'].mean() * 100)


# --- ЧАСТЬ VII ---
print("\n--- ЧАСТЬ VII ---")
df.to_csv('titanic_processed.csv', index=False)
print("Сохранено в файл titanic_processed.csv")