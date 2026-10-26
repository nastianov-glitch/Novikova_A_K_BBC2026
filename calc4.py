def restaurant():
    menu = {"pizza": 700, "sushi": 500, "burger": 350, "fries": 250} 
    
    while True:
        dish_input = input("\nDish (or 'exit'): ").lower() #lower() все в нижнем регистре.\n перенос строки
        
        if dish_input == "exit":
            print("Goodbye,thanks!")
            break
            
        if dish_input:
            dish = dish_input.split()[0]  
        else:
            dish=" "
            
        if dish not in menu:
            print("Not on the menu")
            continue
            
        count = int(input("Portions: "))
        people = int(input("People: "))
        
        total = round(menu[dish] * count * 1.1,2)#menu[dish] из словаря menu берем цену за 1 порцию  
        per_person = round(total / people, 2)
        
        print("Total:", total, "rub.")
        print("Per person:", per_person, "rub.")

restaurant()