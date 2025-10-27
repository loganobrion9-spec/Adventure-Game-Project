"""Game Functions Module.

This module has  several functions used in an adventure game.
It can print a welcome message, shop menu, purchase items, and generate random monsters.

Typical use examples:
    print_welcome("Logan", 25)
    print_shop_menu("Apple", 31, "Pear", 1.234)
    monster = new_random_monster()
    print(monster)
"""

import random


# Attempts to buy quantityToPurchase items given an item price and starting money.
# Returns how many items were purchased and how much money remains.
def purchase_item(itemPrice,startingMoney,quantityToPurchase=1):
    """
    Attempts to buy quantityToPurchase items given an item price and starting money
    Returns how many items were purchased and how much money remains.

    Parameters:
        itemPrice (int): The price of one item.
        startingMoney(int): The player's current money.
        quantityToPurchase(int, optional): The number of items that the player wants to buy (Defaults to one).

    Returns:
        tuple[int, int]: A tuple containing the number of items purchased
        and the amount of money remaining.        

    """

    max_affordable_items = startingMoney//itemPrice
    num_purchased = min(quantityToPurchase,max_affordable_items)
    leftover_money = startingMoney - (num_purchased * itemPrice)
    return num_purchased, leftover_money


# Defines possible types, with ranges for health, power, and money   
def new_random_monster():
    """
    Creates and returns a randomly generated monster with randomized stats.

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


def fight_monster(player_hp, player_gold, monster):
    """Fight loop"""
    character_health = player_hp
    monster_health = monster["health"]
    character_damage = random.randint(25, 75)
    monster_damage = monster["power"]

    print(f"\nA {monster['name']} appears! {monster['description']}")

    while character_health > 0 and monster_health > 0:
        action = input("\n1) Attack  2) Flee: ")

        if action == "1":
            monster_health = monster_health - character_damage
            character_health = character_health - monster_damage
            print(f"You hit the {monster['name']} for {character_damage} damage.")
            print(f"The {monster['name']} hit you for {monster_damage} damage.")

        elif action == "2":
            print("You run away")
            break
        else:
            print("That's not a command, silly.")

        if character_health <= 0:
            print('You got too scared and ran away')
            character_health = 1
        if monster_health <= 0:
            print(f"You defeated the {monster['name']}!")
            player_gold += monster["money"]
            print(f"You found {monster['money']} gold!")

    return character_health, player_gold



    

def print_welcome(name: str, width: int):
    """
    Prints a centered welcome message for the player.

    Parameters:
        name (str): The player's name.
        width (int): The width to center the message within.

    Returns:
        None
    """
    message = f"Hello, {name}!"
    print(message.center(width))


def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float):
    """Prints a formatted shop menu with two items and their prices.
    
    Parameters:
        item1Name(str): Name of shop's first item.
        item1Price(float): Price of shop's first item.
        item2Name(str): Name of shop's second item.
        item2Price(float): Price of shop's second item.

    Returns:
        None
    """
    print("/" + "-" * 22 + "\\")
    print(f"| {item1Name:<12} {f'${item1Price:.2f}':>8} |")
    print(f"| {item2Name:<12} {f'${item2Price:.2f}':>8} |")
    print("\\" + "-" * 22 + "/")

    
def test_functions():
    """Runs tests for all functions in this module."""

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
    print_shop_menu("Apple", 3, "Pear", 1.234)
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
    print_shop_menu("Donut", 2.5, "Orange Juice", 2.0)

if __name__ == "__main__":
    test_functions()
