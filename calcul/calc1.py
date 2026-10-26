print("=== Restaurant Bill Calculator ===") # Английский, чтобы не глючило
dish_input = input("What did you order? (pizza/sushi/burger/fries): ").lower()

# Берем только первое слово, если ввели несколько блюд через пробел
if dish_input:
    dish = dish_input.split()[0]  
else:
    dish=" " # Берем только первое слово, при вводе нескольких блюд через пробел

count = int(input("How many portions? "))
people = int(input("For how many people? "))

if dish == "pizza":
    price = 700
elif dish == "sushi":
    price = 500
elif dish == "burger":
    price = 350
elif dish == "fries":
    price = 250
else:
    price = 0
    print("Sorry, this dish is not on the menu.")

total = price * count
tips = total * 0.1
final = total + tips

print("Total:",final, "rub." )
print("Per person:", round(final / people,2),"rub.")
