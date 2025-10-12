#gamefunctions.py
#Logan OBrion
#9/28/25

import random


# Attempts to buy quantityToPurchase items given an item price and starting money.
# Returns how many items were purchased and how much money remains.
def purchase_item(itemPrice,startingMoney,quantityToPurchase=1):
    """
    Attempts to buy quantityToPurchase items given an item price and starting money
    Returns how many items were purchased and how much money remains.
    """
    max_affordable_items = startingMoney//itemPrice
    num_purchased = min(quantityToPurchase,max_affordable_items)
    leftover_money = startingMoney - (num_purchased * itemPrice)
    return num_purchased, leftover_money


# Defines possible types, with ranges for health, power, and money   
def new_random_monster():
    """Creates and returns a randomly generated monster with randomized stats.

    Returns:
        dict: A dictionary containing the monster's name, description, health, power, and money.
    """
    monsters = [{"name": "Dragon", "description": "A huge dragon that can breathe fire.", "health_range": (500,1000), "power_range": (50,80), "money_range": (200,500)},
                {"name": "Gnome", "description": "A small but mischievious gnome.", "health_range": (50,100), "power_range": (10,20), "money_range": (100,150)},
                {"name": "Cyclops", "description": "An ugly one-eyed beast with a big club.", "health_range": (200,300), "power_range": (30,40), "money_range": (50,100)}]

    # Randomly select one of the monster templates
    chosen = random.choice(monsters)
    monster = {
        "name": chosen["name"],
        "description": chosen["description"],
        "health": random.randint(*chosen["health_range"]),
        "power": random.randint(*chosen["power_range"]),
        "money": random.randint(*chosen["money_range"])
    }

    return monster


def print_welcome(name: str, width: int):
    """Prints a centered welcome message for the name"""
    message = f"Hello, {name}!"
    print(message.center(width))


def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float):
    """Prints a formatted shop menu with two items and their prices."""
    print("/" + "-" * 22 + "\\")
    print(f"| {item1Name:<12} {f'${item1Price:.2f}':>8} |")
    print(f"| {item2Name:<12} {f'${item2Price:.2f}':>8} |")
    print("\\" + "-" * 22 + "/")

    
                  
#item purchase function tests

#Default value
num_purchased, leftover_money = purchase_item(341, 2112)
print(num_purchased)
print(leftover_money)

#Can afford all items
num_purchased, leftover_money = purchase_item(123, 1000, 3)
print(num_purchased)
print(leftover_money)

#Can't afford all items
num_purchased, leftover_money = purchase_item(123, 201, 3)
print(num_purchased)
print(leftover_money)


#monster fuction tests
my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])


my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])


my_monster = new_random_monster()
print(my_monster['name'])
print(my_monster['description'])
print(my_monster['health'])
print(my_monster['power'])
print(my_monster['money'])


#print_welcome tests
print_welcome("Jeff", 20)
print_welcome("Audrey", 30)
print_welcome("Logan", 25)


#print_shop_menu tests
print_shop_menu("Apple", 31, "Pear", 1.234)
print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
print_shop_menu("Donut", 2.5, "Orange Juice", 2.0)
