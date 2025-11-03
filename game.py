# game.py
# Logan OBrion
# 10/19/25

"""
Main game script that imports and uses the functions
from the gamefunctions module.
"""

import gamefunctions
import random

def main():
    """Main game loop"""

    # Ask for player name
    name = input("Enter your name: ")

    # Welcome message
    gamefunctions.print_welcome(name, 40)


    player = {
        "name": name,
        "hp": 150,
        "gold": 1000,
        "inventory": [],
        "equippedWeapon": None
    }

#Main game loop

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player['hp']}, Gold: {player['gold']}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Equip Weapon")
        print("5) Show Inventory")
        print("6) Quit")

        choice = input("Choose an option:")

        if choice == "1":
            monster = gamefunctions.new_random_monster()
            player["hp"], player["gold"] = gamefunctions.fight_monster(player, player["hp"], player["gold"], monster)
            
        elif choice == "2":
            if player["gold"] >= 5:
                 player["gold"] = player["gold"] - 5
                 player["hp"] = 150
                 print(f"You slept and feel sooooooo much better! HP: {player['hp']}")
            else:
                print("You don't have enough gold. Get a job!")

        elif choice == "3":
            player = gamefunctions.visit_shop(player)

        elif choice == "4":
            gamefunctions.equip_weapon(player)

        elif choice == "5":
            print("\nYour Inventory:")
            if not player["inventory"]:
                print("  (empty)")
            for item in player["inventory"]:
                item_info = f"{item['name']} (Type: {item['type']})"
                if item["type"] == "weapon":
                    item_info += f", Durability: {item['currentDurability']}/{item['maxDurability']}"
                if item["type"] == "special":
                    item_info += f", Note: {item.get('note','')}"
                print(" -", item_info)

            if player["equippedWeapon"]:
                print(f"Equipped Weapon: {player['equippedWeapon']['name']}")
            else:
                print("Equipped Weapon: None")

        elif choice == "6":
            print("See you again soon!")
            break

        else:
            print("You have to enter from 1-6, man.")
            
        
    
"""
    # Show shop menu
    print("\nWelcome to the shop!")
    gamefunctions.print_shop_menu("Donut", 2.5, "Apple", 3)

    # Try purchasing something
    money = 100
    print(f"\nYou have ${money}.")
    num_purchased, money_left = gamefunctions.purchase_item(2.5, money, 3)
    print(f"You bought {num_purchased} items and have ${money_left} left.")

    # Generate a random monster
    monster = gamefunctions.new_random_monster()
    print("\nA monster appears!")
    print(monster)
"""
if __name__ == "__main__":
    main()
