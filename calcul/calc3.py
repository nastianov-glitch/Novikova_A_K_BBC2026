def restaurant():
    menu = {"pizza": 700, "sushi": 500, "burger": 350, "fries": 250}
    
    dish_input = input("Dish (pizza/sushi/burger/fries): ").lower()

    if dish_input:
        dish = dish_input.split()[0]  
    else:
        dish=" "
    
    if dish not in menu:
        print("Not on the menu")
        return
        
    count = int(input("Portions: "))
    people = int(input("People: "))
    
    total = round(menu[dish] * count * 1.1,2) # +10% чаевые
    per_person = round(total / people, 2)
    
    print("Total:", total, "rub.")
    print("Per person:", per_person, "rub.")

restaurant()