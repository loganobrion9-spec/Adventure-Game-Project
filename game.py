# game.py
# Logan OBrion
# 10/19/25

"""
Main game script that imports and uses the functions
from the gamefunctions module.
"""

import gamefunctions

def main():
    """Main function that demonstrates use of the gamefunctions module."""

    # Ask for player name
    name = input("Enter your name: ")

    # Welcome message
    gamefunctions.print_welcome(name, 40)

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

if __name__ == "__main__":
    main()
