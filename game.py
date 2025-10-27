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

#Player's starting stats
    player_hp = 150
    player_gold = 10

#Main game loop

    while True:
        print("\nYou are in town.")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice = input("Choose an option:")

        if choice == "1":
            monster = gamefunctions.new_random_monster()
            player_hp, player_gold = gamefunctions.fight_monster(player_hp, player_gold, monster)
            
        elif choice == "2":
            if player_gold >= 5:
                 player_gold = player_gold - 5
                 player_hp = 150
                 print("You slept and feel sooooooo much better!")
            else:
                print("You don't have enough gold. Get a job!")

        elif choice == "3":
            print("See you again soon!")
            break

        else:
            print("You have to enter a 1, 2, or 3, man.")
            
        
    
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
