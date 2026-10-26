import random
import copy

# ============================================================
#  ИГРА "МФЦ" (Многофункциональный Центр)
#  Игрок — посетитель МФЦ, который ищет свой ключ от портала домой
#  в запутанном лабиринте коридоров.
# ============================================================

# ---------- ТИПЫ КОМНАТ ----------
EMPTY    = 'empty'      # пустая комната
CHEST    = 'chest'      # комната с сундуком
MONSTER  = 'monster'    # комната с монстром (пакман)
TRAP     = 'trap'       # комната с ловушкой
KEY      = 'key'        # комната с ключом
PORTAL   = 'portal'     # комната с порталом домой
WALL     = 'wall'       # стена

# ---------- ПРЕДМЕТЫ ----------
# Каждый предмет — словарь: имя, вес, ценность, тип
ITEM_TEMPLATES = [
    {'name': 'меч',     'weight': 5, 'value': 20, 'type': 'оружие',    'damage': 3},
    {'name': 'щит',     'weight': 7, 'value': 15, 'type': 'броня',     'armor': 2},
    {'name': 'зелье',   'weight': 1, 'value': 10, 'type': 'расходник', 'heal': 30},
    {'name': 'ключ',    'weight': 1, 'value': 50, 'type': 'ключ',      'opens': 'portal'},
    {'name': 'карта',   'weight': 1, 'value': 25, 'type': 'ключ',      'opens': 'chest'},
    {'name': 'золото',  'weight': 2, 'value': 30, 'type': 'сокровище', 'gold': 30},
    {'name': 'амулет',  'weight': 1, 'value': 40, 'type': 'сокровище', 'mana': 10},
    {'name': 'факел',   'weight': 2, 'value': 5,  'type': 'расходник', 'light': 1},
]


# ============================================================
#  ГЕНЕРАЦИЯ ЛАБИРИНТА (list comprehension)
# ============================================================
def build_labyrinth(rows, cols):
    """
    Создаёт двумерный список rows x cols, заполненный пустыми комнатами,
    с рамкой из стен по периметру.
    Использует list comprehension для генерации матрицы.
    """
    # Внутренние комнаты — пустые
    lab = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    # Рамка из стен — модифицируем через срезы и генераторы
    lab[0] = [WALL for _ in range(cols)]             # верхняя стена
    lab[-1] = [WALL for _ in range(cols)]            # нижняя стена
    for r in range(rows):                            # боковые стены
        lab[r][0] = WALL
        lab[r][-1] = WALL

    return lab


def place_rooms(lab):
    """
    Расставляет комнаты по карте с помощью генератора случайных координат.
    Возвращает словарь: {(row, col): {'type': ..., 'data': ...}}
    """
    rows = len(lab)
    cols = len(lab[0])
    rooms = {}

    # Внутренние координаты, где можно ставить комнаты
    free_cells = [(r, c) for r in range(1, rows - 1)
                          for c in range(1, cols - 1)]

    # Список типов, которые надо расставить (генератор коллекций)
    plan = (
        [CHEST] * 3 +
        [MONSTER] * 2 +
        [TRAP] * 3 +
        [KEY] * 1 +
        [PORTAL] * 1
    )

    random.shuffle(free_cells)

    for room_type, (r, c) in zip(plan, free_cells):
        lab[r][c] = room_type
        data = {}

        if room_type == CHEST:
            # Сундук пустой или с предметом
            if random.random() < 0.7:
                data['item'] = copy.deepcopy(random.choice(ITEM_TEMPLATES))
                data['opened'] = False
            else:
                data['item'] = None
                data['opened'] = False

        elif room_type == MONSTER:
            data['hp'] = 3          # здоровье монстра
            data['name'] = 'Пакман'
            data['alive'] = True

        elif room_type == TRAP:
            data['damage'] = random.choice([5, 10, 15])
            data['triggered'] = False

        elif room_type == KEY:
            data['item'] = {'name': 'ключ', 'weight': 1, 'value': 50,
                            'type': 'ключ', 'opens': 'portal'}

        elif room_type == PORTAL:
            data['active'] = False

        rooms[(r, c)] = {'type': room_type, 'data': data}

    return rooms


# ============================================================
#  ИНВЕНТАРЬ ИГРОКА
# ============================================================
class Inventory:
    """Инвентарь на основе списка предметов (словарей)."""

    def __init__(self):
        self.items = []         # основной список предметов

    # ---- 1. ДОБАВЛЕНИЕ ----
    def add(self, item):
        """append — добавляет ОДИН предмет в конец списка."""
        self.items.append(item)
        print(f'  [+] Добавлен предмет: {item["name"]}')

    def add_many(self, items):
        """extend — добавляет НЕСКОЛЬКО предметов сразу."""
        self.items.extend(items)
        names = [it['name'] for it in items]
        print(f'  [+] Добавлены предметы: {", ".join(names)}')

    # ---- 2. УДАЛЕНИЕ ----
    def remove_item(self, name):
        """remove — удаляет ПЕРВЫЙ найденный предмет по имени."""
        for it in self.items:
            if it['name'] == name:
                self.items.remove(it)
                print(f'  [-] Выброшен предмет: {name}')
                return True
        print(f'  [!] Предмет "{name}" не найден.')
        return False

    def pop_item(self, index=-1):
        """pop — удаляет предмет по индексу и возвращает его."""
        if not self.items:
            print('  [!] Инвентарь пуст.')
            return None
        if index >= len(self.items) or index < -len(self.items):
            print('  [!] Неверный индекс.')
            return None
        it = self.items.pop(index)
        print(f'  [-] Выброшен предмет (pop #{index}): {it["name"]}')
        return it

    # ---- 3. СОРТИРОВКА (sort / reverse) ----
    def sort_by(self, criterion='value', reverse=True):
        """
        Сортировка инвентаря по критерию (без ручной сортировки!):
          - 'value'  : по ценности
          - 'weight' : по весу
          - 'name'   : по имени
        """
        self.items.sort(key=lambda it: it.get(criterion, 0), reverse=reverse)
        print(f'  [~] Инвентарь отсортирован по "{criterion}" '
              f'({"убыв." if reverse else "возр."}).')

    def reverse_order(self):
        """reverse — разворот текущего порядка."""
        self.items.reverse()
        print('  [~] Порядок инвентаря развёрнут.')

    # ---- 4. ПОИСК КЛЮЧЕВЫХ ПРЕДМЕТОВ ----
    def has_key(self):
        """in — проверка наличия ключа."""
        return any(it['type'] == 'ключ' for it in self.items)

    def find_index(self, name):
        """index — поиск индекса предмета по имени."""
        names = [it['name'] for it in self.items]
        if name in names:
            return names.index(name)
        return -1

    # ---- 5. КОПИРОВАНИЕ ----
    def bad_copy(self):
        """
        copy() — ПОВЕРХНОСТНАЯ копия.
        ПРОБЛЕМА: копируется список, но словари внутри — те же объекты!
        Изменение предмета в копии изменит оригинал.
        """
        shallow = self.items.copy()
        print('  [!] Сделана ПОВЕРХНОСТНАЯ копия (copy).')
        print('      Изменения предметов в копии затронут оригинал!')
        return shallow

    def good_copy(self):
        """
        deepcopy — ГЛУБОКАЯ копия.
        Изменение предметов в копии НЕ затронет оригинал.
        """
        deep = copy.deepcopy(self.items)
        print('  [OK] Сделана ГЛУБОКАЯ копия (deepcopy).')
        return deep

    def slice_items(self, start=0, end=None):
        """Срез списка — копия части инвентаря."""
        return self.items[start:end]

    # ---- 6. ИЗМЕНЕНИЕ СВОЙСТВА ПРЕДМЕТА ----
    def upgrade_item(self, name, prop, bonus):
        """Изменяет свойство предмета в инвентаре (например, +урон)."""
        idx = self.find_index(name)
        if idx == -1:
            print(f'  [!] Предмет "{name}" не найден.')
            return
        item = self.items[idx]
        item[prop] = item.get(prop, 0) + bonus
        print(f'  [*] Предмет "{name}": {prop} увеличен на {bonus} '
              f'(теперь {item[prop]}).')

    # ---- ПРОСМОТР ----
    def show(self):
        if not self.items:
            print('  Инвентарь пуст.')
            return
        print('  ┌─────── ИНВЕНТАРЬ ───────┐')
        for i, it in enumerate(self.items):
            extra = ''
            for k, v in it.items():
                if k not in ('name', 'weight', 'value', 'type'):
                    extra += f', {k}={v}'
            print(f'  [{i}] {it["name"]:8} '
                  f'(вес={it["weight"]}, ценность={it["value"]}, '
                  f'тип={it["type"]}{extra})')
        print('  └─────────────────────────┘')


# ============================================================
#  ИГРОК
# ============================================================
class Player:
    def __init__(self, x, y):
        self.x = x                  # координаты (x, y) — как [col, row]
        self.y = y
        self.hp = 100               # здоровье
        self.max_hp = 100
        self.inventory = Inventory()
        self.visited = []           # список посещённых координат

    def position(self):
        return [self.x, self.y]     # (x, y) — список

    def move(self, dx, dy, lab):
        nx, ny = self.x + dx, self.y + dy
        if lab[ny][nx] == WALL:
            print('  [x] Там стена, дальше нельзя.')
            return False
        self.x, self.y = nx, ny
        return True

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f'  [+] HP восстановлено на {amount}. Текущее HP: {self.hp}')

    def damage(self, amount):
        self.hp -= amount
        print(f'  [-] Получен урон {amount}. Текущее HP: {self.hp}')
        if self.hp <= 0:
            print('  [X] Вы погибли! Игра окончена.')
            return True
        return False


# ============================================================
#  ОБРАБОТКА КОМНАТ
# ============================================================
def enter_room(lab, rooms, player):
    """Обрабатывает текущую комнату игрока."""
    key = (player.y, player.x)

    # Запоминаем посещение (второй список — посещённые комнаты)
    if [player.x, player.y] not in player.visited:
        player.visited.append([player.x, player.y])

    if key not in rooms:
        print('  Пустая комната.')
        return

    room = rooms[key]
    rtype = room['type']
    data = room['data']

    # --- СУНДУК ---
    if rtype == CHEST:
        if data.get('opened'):
            print('  Сундук уже открыт.')
            return
        if data.get('item'):
            item = data['item']
            print(f'  Найден сундук с предметом: {item["name"]}!')
            ans = input('  Взять предмет? (д/н): ').strip().lower()
            if ans in ('д', 'y', 'да'):
                player.inventory.add(item)
                data['item'] = None
        else:
            print('  Сундук пуст.')
        data['opened'] = True

    # --- МОНСТР ---
    elif rtype == MONSTER:
        if not data.get('alive'):
            print('  Здесь уже никого нет.')
            return
        print(f'  Вас встретил монстр "{data["name"]}"! HP монстра: {data["hp"]}')
        while data['hp'] > 0 and player.hp > 0:
            action = input('  Атаковать (а) / Убежать (у): ').strip().lower()
            if action in ('а', 'a', 'attack'):
                dmg = random.randint(1, 3)
                data['hp'] -= dmg
                print(f'  Вы ударили монстра на {dmg}. HP монстра: {data["hp"]}')
                if data['hp'] <= 0:
                    print('  [+] Монстр побеждён!')
                    data['alive'] = False
                    # Награда
                    player.inventory.add({'name': 'золото', 'weight': 2,
                                          'value': 30, 'type': 'сокровище',
                                          'gold': 30})
                    break
                # Монстр отвечает
                if player.damage(random.randint(1, 2)):
                    return
            elif action in ('у', 'u', 'run'):
                print('  Вы убежали в предыдущую комнату.')
                # откатываем шаг
                return
            else:
                print('  Неизвестное действие.')

    # --- ЛОВУШКА ---
    elif rtype == TRAP:
        if data.get('triggered'):
            print('  Ловушка уже сработала.')
            return
        print(f'  [!] Ловушка! Урон: {data["damage"]}')
        data['triggered'] = True
        if player.damage(data['damage']):
            return

    # --- КЛЮЧ ---
    elif rtype == KEY:
        if data.get('item'):
            item = data['item']
            print(f'  Найден КЛЮЧ от портала!')
            player.inventory.add(item)
            data['item'] = None
        else:
            print('  Ключ уже забран.')

    # --- ПОРТАЛ ---
    elif rtype == PORTAL:
        if player.inventory.has_key():
            print('  [OK] У вас есть ключ! Портал активирован. ВЫ ДОМА! 🏠')
            return 'WIN'
        else:
            print('  Портал закрыт. Нужен ключ (ищите комнату с ключом).')


# ============================================================
#  ГЛАВНЫЙ ЦИКЛ ИГРЫ
# ============================================================
def show_map(lab, player, rooms, visited):
    """Показывает карту: посещённые комнаты видны, остальные — скрыты."""
    print('\n  Карта (?) — неисследованные комнаты:')
    for r in range(len(lab)):
        line = '  '
        for c in range(len(lab[0])):
            if [c, r] == [player.x, player.y]:
                line += ' P '
            elif [c, r] in visited:
                t = lab[r][c]
                icons = {EMPTY: '.', CHEST: 'C', MONSTER: 'M',
                         TRAP: 'T', KEY: 'K', PORTAL: 'O', WALL: '#'}
                line += f' {icons.get(t, "?")} '
            elif lab[r][c] == WALL:
                line += ' # '
            else:
                line += ' ? '
        print(line)
    print('  P — вы, # — стена, . — пусто, C — сундук, M — монстр,')
    print('  T — ловушка, K — ключ, O — портал, ? — неизвестно\n')


def game():
    print('=' * 60)
    print('  ДОБРО ПОЖАЛОВАТЬ В МФЦ-ЛАБИРИНТ!')
    print('  Цель: найти ключ и добраться до портала домой.')
    print('=' * 60)

    rows, cols = 8, 10
    lab = build_labyrinth(rows, cols)
    rooms = place_rooms(lab)

    # Начальная позиция
    player = Player(x=1, y=1)
    lab[1][1] = EMPTY

    while True:
        show_map(lab, player, rooms, player.visited)
        print(f'  HP: {player.hp}/{player.max_hp} | '
              f'Позиция: ({player.x}, {player.y}) | '
              f'Предметов: {len(player.inventory.items)}')

        print('  Команды: w/a/s/d — движение, i — инвентарь, '
              'q — выход')
        cmd = input('  > ').strip().lower()

        # ---- ДВИЖЕНИЕ ----
        if cmd == 'w':
            if player.move(0, -1, lab):
                r = enter_room(lab, rooms, player)
                if r == 'WIN':
                    break
        elif cmd == 's':
            if player.move(0, 1, lab):
                r = enter_room(lab, rooms, player)
                if r == 'WIN':
                    break
        elif cmd == 'a':
            if player.move(-1, 0, lab):
                r = enter_room(lab, rooms, player)
                if r == 'WIN':
                    break
        elif cmd == 'd':
            if player.move(1, 0, lab):
                r = enter_room(lab, rooms, player)
                if r == 'WIN':
                    break

        # ---- ИНВЕНТАРЬ ----
        elif cmd == 'i':
            inventory_menu(player)

        elif cmd == 'q':
            print('  Вы вышли из игры.')
            break
        else:
            print('  Неизвестная команда.')

        if player.hp <= 0:
            print('  Игра окончена: вы погибли.')
            break


def inventory_menu(player):
    """Меню инвентаря."""
    inv = player.inventory
    while True:
        print('\n  ─── ИНВЕНТАРЬ ───')
        print('  1 — показать')
        print('  2 — сортировать (по ценности)')
        print('  3 — сортировать (по весу)')
        print('  4 — сортировать (по имени)')
        print('  5 — развернуть порядок (reverse)')
        print('  6 — выбросить по имени (remove)')
        print('  7 — выбросить по индексу (pop)')
        print('  8 — улучшить предмет (+урон/+броня)')
        print('  9 — проверить наличие ключа (in)')
        print(' 10 — найти индекс предмета (index)')
        print(' 11 — срез списка (slice)')
        print(' 12 — ПЛОХАЯ копия (copy — изменяет оригинал!)')
        print(' 13 — хорошая копия (deepcopy)')
        print('  0 — назад')
        c = input('  > ').strip()

        if c == '1':
            inv.show()
        elif c == '2':
            inv.sort_by('value')
        elif c == '3':
            inv.sort_by('weight')
        elif c == '4':
            inv.sort_by('name', reverse=False)
        elif c == '5':
            inv.reverse_order()
        elif c == '6':
            name = input('  Имя предмета: ').strip()
            inv.remove_item(name)
        elif c == '7':
            idx = input('  Индекс предмета: ').strip()
            try:
                inv.pop_item(int(idx))
            except ValueError:
                print('  [!] Введите целое число.')
        elif c == '8':
            name = input('  Имя предмета: ').strip()
            prop = input('  Свойство (damage/armor/heal): ').strip()
            try:
                bonus = int(input('  На сколько увеличить: ').strip())
            except ValueError:
                print('  [!] Нужно число.')
                continue
            inv.upgrade_item(name, prop, bonus)
        elif c == '9':
            if inv.has_key():
                print('  [OK] Ключ есть в инвентаре!')
            else:
                print('  [X] Ключа нет.')
        elif c == '10':
            name = input('  Имя предмета: ').strip()
            i = inv.find_index(name)
            if i == -1:
                print('  [!] Не найдено.')
            else:
                print(f'  [OK] Индекс: {i}')
        elif c == '11':
            s = input('  Начало среза (Enter=0): ').strip() or '0'
            e = input('  Конец среза (Enter=конец): ').strip()
            s = int(s)
            part = inv.slice_items(s, int(e) if e else None)
            print('  Срез инвентаря:')
            for it in part:
                print(f'    - {it["name"]}')
        elif c == '12':
            # Демонстрация проблемы copy()
            if not inv.items:
                print('  [!] Инвентарь пуст.')
                continue
            print('  Демонстрация проблемы поверхностного копирования:')
            bad = inv.bad_copy()
            print('  Изменяем название первого предмета в КОПИИ...')
            if bad:
                bad[0]['name'] = 'ИЗМЕНЕНО_В_КОПИИ'
                print('  Оригинал после изменения копии:')
                inv.show()
                # восстанавливаем
                bad[0]['name'] = 'меч' if bad[0]['name'] == 'ИЗМЕНЕНО_В_КОПИИ' else bad[0]['name']
        elif c == '13':
            deep = inv.good_copy()
            if deep and deep[0:1]:
                print('  Изменяем название первого предмета в ГЛУБОКОЙ копии...')
                deep[0]['name'] = 'ИЗМЕНЕНО_В_КОПИИ'
                print('  Оригинал (НЕ изменился):')
                inv.show()
        elif c == '0':
            return
        else:
            print('  Неизвестная команда.')


# ============================================================
#  ЗАПУСК
# ============================================================
if __name__ == '__main__':
    game()