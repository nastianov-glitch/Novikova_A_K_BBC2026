# Программа с выбором уровня

def level_upper():
    

    print("Уровень 1. Метод:upper()")
    print("Описание: upper() делает все буквы заглавными.")
    print("Пример: привет -> привет".upper())

    text = input("Введи слово: ")
    result = text.upper()

    print("Вход: строка =", text, ", метод = upper()")
    print("Выход:", result)

def level_lower():

    print("\nУровень 2. Метод:lower()")
    print("Описание: lower() делает все буквы строчными.")
    print("Пример: ПРИВЕТ -> ПРИВЕТ".lower())

    text = input("Введи слово: ")
    result = text.lower()

    print("Вход: строка =", text, ", метод = lower()")
    print("Выход:", result)

def level_capitalize():
  

    print("\nУровень 3. Метод: capitalize()")
    print("Описание: capitalize() делает первую букву заглавной, остальные — строчными.")
    print("Пример: привет мир ->", "привет мир".capitalize())

    text = input("Введи слово: ")
    result = text.capitalize()

    print("Вход: строка =", text, ", метод = capitalize()")
    print("Выход:", result)

#Меню слота
def u1():
    while True:
        print("ВЫБОР НА 1-М УРОВНЕ")
        print("1 - upper()")
        print("2 - lower()")
        print("3 - capitalize()")
        print("0 - выход")

        choice = input("Твой выбор: ")

        if choice == "1":
            level_upper()
        elif choice == "2":
            level_lower()
        elif choice == "3":
            level_capitalize()
        elif choice == "0":
            print("BREAK")
            break
        else:
            print("Нет такого уровня.")


def level_find():

    print("Уровень 2. Метод:find()")
    print("Описание: find() ищет подстроку и возвращает её позицию (или -1, если не найдено).")
    print("Пример:привет мир.find('мир') ->", "привет мир".find("мир"))

    text = input("Введи строку: ")
    sub = input("Что искать: ")
    result = text.find(sub)

    print("Вход: строка =", text, ", метод = find()")
    print("Выход:", result)

def level_replace():

    print("\nУровень 2. Метод: replace()")
    print("Описание: replace() заменяет одну подстроку на другую.")
    print("Пример: мама мыла раму ->", "мама мыла раму".replace("мама", "папа"))

    text = input("Введи строку: ")
    old = input("Что заменить: ")
    new = input("На что заменить: ")
    result = text.replace(old, new)

    print("Вход: строка =", text, ", метод = replace()")
    print("Выход:", result)

def level_count():

    print("\nУровень 3. Метод:count()")
    print("Описание: count() считает, сколько раз подстрока встречается в строке.")
    print("Пример: абракадабра.count('а') ->", "абракадабра".count("а"))

    text = input("Введи строку: ")
    sub = input("Что считать: ")
    result = text.count(sub)

    print("Вход: строка =", text, ", метод =c ount()")
    print("Выход:", result)

def u2():
    while True:
        print("ВЫБОР НА 1-М УРОВНЕ")
        print("1 - find()")
        print("2 - replace()")
        print("3 - count()")
        print("0 - выход")

        choice = input("Твой выбор: ")

        if choice == "1":
            level_find()
        elif choice == "2":
            level_replace()
        elif choice == "3":
            level_count()
        elif choice == "0":
            print("BREAK!")
            break
        else:
            print("Нет такого уровня.")

while True:
    print("ВЫБОР УРОВНЯ")
    print("1 - Уровень 1 (upper, lower, capitalize)")
    print("2 - Уровень 2 (find, replace, count)")
    print("0 - выход")

    choice = input("Твой выбор: ")

    if choice == "1":
        u1()
    elif choice == "2":
        u2()
    elif choice == "0":
        print("Пока!")
        break
    else:
        print("Нет такого слота.")