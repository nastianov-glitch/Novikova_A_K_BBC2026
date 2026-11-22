import random
import copy

EMPTY = 'empty'
CHEST = 'chest'
MONSTER = 'monster'
TRAP = 'trap'
KEY = 'key'
PORTAL = 'portal'
WALL = 'wall'

ITEM_TEMPLATES = [
    {'name': 'меч', 'weight': 5, 'value': 20, 'type': 'оружие', 'damage': 3},
    {'name': 'щит', 'weight': 7, 'value': 15, 'type': 'броня', 'armor': 2},
    {'name': 'зелье', 'weight': 1, 'value': 10, 'type': 'расходник', 'heal': 30},
    {'name': 'ключ', 'weight': 1, 'value': 50, 'type': 'ключ', 'opens': 'portal'},
    {'name': 'карта', 'weight': 1, 'value': 25, 'type': 'ключ', 'opens': 'chest'},
    {'name': 'золото', 'weight': 2, 'value': 30, 'type': 'сокровище', 'gold': 30},
    {'name': 'амулет', 'weight': 1, 'value': 40, 'type': 'сокровище', 'mana': 10},
    {'name': 'факел', 'weight': 2, 'value': 5, 'type': 'расходник', 'light': 1},
]

def build_labyrinth(rows, cols):
    lab = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    lab[0] = [WALL for _ in range(cols)]
    lab[-1] = [WALL for _ in range(cols)]
    for r in range(rows):
        lab[r][0] = WALL
        lab[r][-1] = WALL
    return lab

def place_rooms(lab):
    rows = len(lab)
    cols = len(lab[0])
    rooms = {}
    free_cells = [(r, c) for r in range(1, rows - 1) for c in range(1, cols - 1)]
    plan = [CHEST] * 3 + [MONSTER] * 2 + [TRAP] * 3 + [KEY] * 1 + [PORTAL] * 1
    random.shuffle(free_cells)
    for room_type, (r, c) in zip(plan, free_cells):
        lab[r][c] = room_type
        data = {}
        if room_type == CHEST:
            if random.random() < 0.7:
                data['item'] = copy.deepcopy(random.choice(ITEM_TEMPLATES))
                data['opened'] = False
            else:
                data['item'] = None
                data['opened'] = False
        elif room_type == MONSTER:
            data['hp'] = 3
            data['name'] = 'Пакман'
            data['alive'] = True
        elif room_type == TRAP:
            data['damage'] = random.choice([5, 10, 15])
            data['triggered'] = False
        elif room_type == KEY:
            data['item'] = {'name': 'ключ', 'weight': 1, 'value': 50, 'type': 'ключ', 'opens': 'portal'}
        rooms[(r, c)] = {'type': room_type, 'data': data}
    return rooms

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        print(f'  [+] Добавлен предмет: {item["name"]}')

    def remove_item(self, name):
        for it in self.items:
            if it['name'] == name:
                self.items.remove(it)
                print(f'  [-] Выброшен предмет: {name}')
                return True
        print(f'  [!] Предмет "{name}" не найден.')
        return False

    def pop_item(self, index=-1):
        if not self.items:
            print('  [!] Инвентарь пуст.')
            return None
        if index >= len(self.items) or index < -len(self.items):
            print('  [!] Неверный индекс.')
            return None
        it = self.items.pop(index)
        print(f'  [-] Выброшен предмет (pop #{index}): {it["name"]}')
        return it

    def sort_by(self, criterion='value', reverse=True):
        self.items.sort(key=lambda it: it.get(criterion, 0), reverse=reverse)
        print(f'  [~] Инвентарь отсортирован по "{criterion}".')

    def reverse_order(self):
        self.items.reverse()
        print('  [~] Порядок инвентаря развёрнут.')

    def has_key(self):
        return any(it['type'] == 'ключ' for it in self.items)

    def find_index(self, name):
        names = [it['name'] for it in self.items]
        return names.index(name) if name in names else -1

    def bad_copy(self):
        shallow = self.items.copy()
        print('  [!] Сделана поверхностная копия.')
        return shallow

    def good_copy(self):
        deep = copy.deepcopy(self.items)
        print('  [OK] Сделана глубокая копия.')
        return deep

    def slice_items(self, start=0, end=None):
        return self.items[start:end]

    def upgrade_item(self, name, prop, bonus):
        idx = self.find_index(name)
        if idx == -1:
            print(f'  [!] Предмет "{name}" не найден.')
            return
        item = self.items[idx]
        item[prop] = item.get(prop, 0) + bonus
        print(f'  [*] Предмет "{name}": {prop} увеличен на {bonus} (теперь {item[prop]}).')

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
            print(f'  [{i}] {it["name"]:8} (вес={it["weight"]}, ценность={it["value"]}, тип={it["type"]}{extra})')
        print('  └─────────────────────────┘')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.inventory = Inventory()
        self.visited = []

    def move(self, dx, dy, lab):
        nx, ny = self.x + dx, self.y + dy
        if lab[ny][nx] == WALL:
            print('  [x] Там стена, дальше нельзя.')
            return False
        self.x, self.y = nx, ny
        return True

    def damage(self, amount):
        self.hp -= amount
        print(f'  [-] Получен урон {amount}. Текущее HP: {self.hp}')
        if self.hp <= 0:
            print('  [X] Вы погибли! Игра окончена.')
            return True
        return False

def enter_room(lab, rooms, player, prev_x, prev_y):
    key = (player.y, player.x)
    if [player.x, player.y] not in player.visited:
        player.visited.append([player.x, player.y])
    if key not in rooms:
        print('  Пустая комната.')
        return

    room = rooms[key]
    rtype = room['type']
    data = room['data']

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
                    player.inventory.add({'name': 'золото', 'weight': 2, 'value': 30, 'type': 'сокровище', 'gold': 30})
                    break
                if player.damage(random.randint(1, 2)):
                    return 'DEAD'
            elif action in ('у', 'u', 'run'):
                print('  Вы убежали в предыдущую комнату.')
                player.x, player.y = prev_x, prev_y
                return
            else:
                print('  Неизвестное действие.')

    elif rtype == TRAP:
        if data.get('triggered'):
            print('  Ловушка уже сработала.')
            return
        print(f'  [!] Ловушка! Урон: {data["damage"]}')
        data['triggered'] = True
        if player.damage(data['damage']):
            return 'DEAD'

    elif rtype == KEY:
        if data.get('item'):
            item = data['item']
            print('  Найден ключ от портала!')
            player.inventory.add(item)
            data['item'] = None
        else:
            print('  Ключ уже забран.')

    elif rtype == PORTAL:
        if player.inventory.has_key():
            print('  [OK] У вас есть ключ! Портал активирован. Вы дома!')
            return 'WIN'
        else:
            print('  Портал закрыт. Нужен ключ.')

def show_map(lab, player, visited):
    print('\n  Карта:')
    for r in range(len(lab)):
        line = '  '
        for c in range(len(lab[0])):
            if [c, r] == [player.x, player.y]:
                line += ' P '
            elif [c, r] in visited:
                t = lab[r][c]
                icons = {EMPTY: '.', CHEST: 'C', MONSTER: 'M', TRAP: 'T', KEY: 'K', PORTAL: 'O', WALL: '#'}
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
    player = Player(x=1, y=1)
    lab[1][1] = EMPTY

    while True:
        show_map(lab, player, player.visited)
        print(f'  HP: {player.hp}/{player.max_hp} | Позиция: ({player.x}, {player.y}) | Предметов: {len(player.inventory.items)}')
        print('  Команды: w/a/s/d — движение, i — инвентарь, q — выход')
        cmd = input('  > ').strip().lower()

        old_x, old_y = player.x, player.y

        if cmd == 'w':
            if player.move(0, -1, lab):
                r = enter_room(lab, rooms, player, old_x, old_y)
                if r in ('WIN', 'DEAD'): break
        elif cmd == 's':
            if player.move(0, 1, lab):
                r = enter_room(lab, rooms, player, old_x, old_y)
                if r in ('WIN', 'DEAD'): break
        elif cmd == 'a':
            if player.move(-1, 0, lab):
                r = enter_room(lab, rooms, player, old_x, old_y)
                if r in ('WIN', 'DEAD'): break
        elif cmd == 'd':
            if player.move(1, 0, lab):
                r = enter_room(lab, rooms, player, old_x, old_y)
                if r in ('WIN', 'DEAD'): break
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
    inv = player.inventory
    while True:
        print('\n  ─── ИНВЕНТАРЬ ───')
        print('  1 — показать')
        print('  2 — сортировать (по ценности)')
        print('  3 — сортировать (по весу)')
        print('  4 — сортировать (по имени)')
        print('  5 — развернуть порядок')
        print('  6 — выбросить по имени')
        print('  7 — выбросить по индексу')
        print('  8 — улучшить предмет')
        print('  9 — проверить наличие ключа')
        print(' 10 — найти индекс предмета')
        print(' 11 — срез списка')
        print(' 12 — плохая копия (copy)')
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
            prop = input('  Свойство: ').strip()
            try:
                bonus = int(input('  На сколько увеличить: ').strip())
            except ValueError:
                print('  [!] Нужно число.')
                continue
            inv.upgrade_item(name, prop, bonus)
        elif c == '9':
            print('  [OK] Ключ есть!' if inv.has_key() else '  [X] Ключа нет.')
        elif c == '10':
            name = input('  Имя предмета: ').strip()
            i = inv.find_index(name)
            print(f'  [OK] Индекс: {i}' if i != -1 else '  [!] Не найдено.')
        elif c == '11':
            s = input('  Начало среза (Enter=0): ').strip() or '0'
            e = input('  Конец среза (Enter=конец): ').strip()
            part = inv.slice_items(int(s), int(e) if e else None)
            print('  Срез инвентаря:')
            for it in part:
                print(f'    - {it["name"]}')
        elif c == '12':
            if not inv.items:
                print('  [!] Инвентарь пуст.')
                continue
            bad = inv.bad_copy()
            if bad:
                original_name = bad[0]['name']
                bad[0]['name'] = 'ИЗМЕНЕНО_В_КОПИИ'
                print('  Оригинал после изменения копии:')
                inv.show()
                bad[0]['name'] = original_name
        elif c == '13':
            deep = inv.good_copy()
            if deep and deep[0:1]:
                deep[0]['name'] = 'ИЗМЕНЕНО_В_КОПИИ'
                print('  Оригинал (НЕ изменился):')
                inv.show()
        elif c == '0':
            return
        else:
            print('  Неизвестная команда.')

if __name__ == '__main__':
    game()