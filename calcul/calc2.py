def get_price(dish):
    menu = {"pizza": 700, "sushi": 500, "burger": 350, "fries": 250}
    return menu.get(dish, 0)

def calct(price, count, tips=0.1):
    return price * count * (1 + tips)

def split(total, people):
    return total / people

dish_input = input("Dish (pizza/sushi/burger/fries): ").lower()
if dish_input:
    dish = dish_input.split()[0]  
else:
    dish=" "

count = int(input("Portions: "))
people = int(input("People: "))

total = round(calct(get_price(dish), count),2)
per_person = round(split(total, people), 2)

print("Total:", total, "rub.")
print("Per person:", per_person, "rub.")