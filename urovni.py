def level_1():
    print(' Уровень 1: upper, lower, capitalize ')
    print('lower      - нижний регистр')
    print('upper      - верхний регистр')
    print('capitalize - первая буква заглавная, остальные строчные')
    print('Пример для "привет - мир":')
    print('  capitalize - "Привет - мир"')
    print('  lower      - "привет - мир"')
    print('  upper      - "ПРИВЕТ - МИР"')

    while True:
        method = input('\nВведите метод (или 6 для выхода): ').strip().lower()
        if method == '6':
            return
        if method in ('upper', 'lower', 'capitalize'):
            word = input('Введите слово: ')
            print('Результат:', getattr(word, method)())
        else:
            print('Неизвестный метод. Доступны: upper, lower, capitalize')


def level_2():
    print(' Уровень 2: find, replace, count, index ')
    print('find    - индекс первого вхождения подстроки, или -1, если не найдена')
    print('replace - заменяет подстроку на другую')
    print('count   - количество вхождений подстроки')
    print('index   - как find, но бросает ValueError, если подстрока не найдена')
    print('Пример для "Ботать это круто. Очень круто":')
    print('  find("круто")             - индекс первого "круто"')
    print('  replace("круто", "мощно") - "Ботать это мощно. Очень мощно"')
    print('  count("круто")            - 2')
    print('  index("круто")            - индекс первого "круто"')

    while True:
        method = input('\nВведите метод (или 6 для выхода): ').strip().lower()
        if method == '6':
            return

        if method == 'find':
            word = input('Введите слово: ')
            sub = input('Введите подстроку: ')
            print('Результат:', word.find(sub))

        elif method == 'replace':
            word = input('Введите слово: ')
            sub = input('Что заменить: ')
            new = input('На что заменить: ')
            result = word.replace(sub, new)
            print('Результат:', result)
            if sub not in word:
                print('(подстрока не найдена — строка не изменилась)')

        elif method == 'count':
            word = input('Введите слово: ')
            sub = input('Введите подстроку: ')
            print('Результат:', word.count(sub))

        elif method == 'index':
            word = input('Введите слово: ')
            sub = input('Введите подстроку: ')
            try:
                print('Результат:', word.index(sub))
            except ValueError:
                print('Подстрока не найдена (ValueError)')

        else:
            print('Неизвестный метод. Доступны: find, replace, count, index')


def level_3():
    print(' Уровень 3: split, join ')
    print('split - разбивает строку на список подстрок по разделителю')
    print('join  - склеивает список строк в одну строку через разделитель')
    print('Пример для "Ботать это круто. Очень круто":')
    print('  split(" ")            - ["Ботать", "это", "круто.", "Очень", "круто"]')
    print('  ", ".join([...])      - "Ботать, это, круто., Очень, круто"')

    while True:
        method = input('\nВведите метод (или 6 для выхода): ').strip().lower()
        if method == '6':
            return

        if method == 'split':
            word = input('Введите слово: ')
            sep = input('Введите разделитель (Enter = пробел): ') or ' '
            print('Результат:', word.split(sep))

        elif method == 'join':
            print('Как собрать строку:')
            print('  1 - из готового текста (разобьём по разделителю и склеим)')
            print('  2 - из элементов, введённых вручную')
            mode = input('Выберите способ (1/2): ').strip()

            if mode == '2':
                raw = input('Введите элементы через запятую: ')
                items = [x.strip() for x in raw.split(',') if x.strip() != '']
                sep = input('Введите разделитель (Enter = пробел): ') or ' '
                print('Результат:', sep.join(items))
            else:
                word = input('Введите слово: ')
                sep = input('Введите разделитель (Enter = пробел): ') or ' '
                print('Результат:', sep.join(word.split()))

        else:
            print('Неизвестный метод. Доступны: split, join')


def level_4():
    print('Уровень 4: isdigit, isalpha, strip, format, reverse, lower, upper ')
    print('isdigit   - состоит ли строка только из цифр')
    print('isalpha   - состоит ли строка только из букв')
    print('strip     - убирает пробелы в начале и конце')
    print('format    - форматирование строки (2 знака после запятой)')
    print('reverse   - разворот строки через срез [::-1]')
    print('lower     - нижний регистр')
    print('upper     - верхний регистр')
    print('Пример: "1234*&^%"')
    print('  isdigit()  -> False (есть не только цифры)')
    print('  isalpha()  -> False (есть не только буквы)')

    while True:
        method = input('\nВведите метод (или 6 для выхода): ').strip().lower()
        if method == '6':
            return

        if method == 'isdigit':
            word = input('Введите слово: ')
            print('Результат:', word.isdigit())

        elif method == 'isalpha':
            word = input('Введите слово: ')
            print('Результат:', word.isalpha())

        elif method == 'strip':
            word = input('Введите слово с пробелами по краям: ')
            print('Результат:', repr(word.strip()))

        elif method == 'format':
            word = input('Введите число: ')
            try:
                print('Результат:', '{:.2f}'.format(float(word)))
            except ValueError:
                print('Это не число.')

        elif method == 'reverse':
            word = input('Введите слово: ')
            print('Результат:', word[::-1])

        elif method == 'lower':
            word = input('Введите слово: ')
            print('Результат:', word.lower())

        elif method == 'upper':
            word = input('Введите слово: ')
            print('Результат:', word.upper())

        else:
            print('Неизвестный метод. Доступны: isdigit, isalpha, strip, '
                  'format, reverse, lower, upper')


def level_5():
    print(' Уровень 5: секретный ')
    print('Цепочка методов: strip -> replace -> upper -> capitalize')
    source = '   python;is;AWESOME   '
    result = source.strip().replace(';', ' ').upper().capitalize()
    print('Исходная строка :', repr(source))
    print('Результат       :', repr(result))
    print('Разбор:')
    print('  strip()          убирает пробелы по краям - "python;is;AWESOME"')
    print('  replace(";", " ") меняет ; на пробел     - "python is AWESOME"')
    print('  upper()          верхний регистр         - "PYTHON IS AWESOME"')
    print('  capitalize()     первая заглавная, ост. строчные - "Python is awesome"')

    while True:
        choice = input('\nХотите попробовать свою строку? (да/нет): ').strip().lower()
        if choice in ('нет', 'н', 'no', 'n', '6'):
            return
        if choice in ('да', 'д', 'yes', 'y'):
            user_str = input('Введите строку (можно с ";" и пробелами по краям): ')
            user_result = user_str.strip().replace(';', ' ').upper().capitalize()
            print('Ваш результат:', repr(user_result))
        else:
            print('Введите "да" или "нет".')


def main():
    levels = {
        '1': level_1,
        '2': level_2,
        '3': level_3,
        '4': level_4,
        '5': level_5,
    }

    while True:
        print('\n=== Меню ===')
        print('1 - upper / lower / capitalize')
        print('2 - find / replace / count / index')
        print('3 - split / join')
        print('4 - isdigit / isalpha / strip / format / reverse')
        print('5 - секретный уровень (цепочка методов)')
        print('6 - выход')

        choice = input('Введите номер уровня (1-5) или 6 для выхода: ').strip()

        if choice == '6':
            print('До встречи!')
            break

        if choice in levels:
            levels[choice]()
        else:
            print('Такого уровня нет. Попробуйте 1-5.')


if __name__ == '__main__':
    main()