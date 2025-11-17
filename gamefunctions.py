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
import pygame
import sys

TILE = 32
GRID_SIZE = 10
SCREEN_SIZE = TILE * GRID_SIZE
PLAYER_COLOR = (0, 120, 200)  # Blue player square
TOWN_COLOR = (0, 200, 0)      # Green circle for town
MONSTER_COLOR = (200, 0, 0)   # Red circle for monster
GRID_LINE_COLOR = (50, 50, 50)
BG_COLOR = (0, 0, 0)

def open_map(player, map_state):
    """
    Launch a pygame map and return (action, map_state)
    action: "town" or "monster"
    """

    # Helper to ensure stored values are lists
    def _as_list(v):
        return list(v) if isinstance(v, (tuple, list)) else [0, 0]

    # Load map state (or defaults)
    player_pos = _as_list(map_state.get("player_pos", [0, 0]))
    town_pos = _as_list(map_state.get("town_pos", [0, 0]))
    monster_pos = _as_list(map_state.get("monster_pos", [GRID_SIZE - 1, GRID_SIZE - 1]))
    monster_alive = bool(map_state.get("monster_alive", True))

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 18)

    left_town = False
    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player_pos[0], player_pos[1]

                if event.key == pygame.K_UP:
                    new_y = max(0, player_pos[1] - 1)
                elif event.key == pygame.K_DOWN:
                    new_y = min(GRID_SIZE - 1, player_pos[1] + 1)
                elif event.key == pygame.K_LEFT:
                    new_x = max(0, player_pos[0] - 1)
                elif event.key == pygame.K_RIGHT:
                    new_x = min(GRID_SIZE - 1, player_pos[0] + 1)
                else:
                    continue

                # Apply movement
                if (new_x, new_y) != (player_pos[0], player_pos[1]):
                    player_pos[0], player_pos[1] = new_x, new_y

                    # Check if returning to town
                    if [player_pos[0], player_pos[1]] == town_pos:
                        if left_town:
                            map_state["player_pos"] = player_pos
                            map_state["town_pos"] = town_pos
                            map_state["monster_pos"] = monster_pos
                            map_state["monster_alive"] = monster_alive
                            pygame.quit()
                            return ("town", map_state)
                    else:
                        left_town = True

                    # Check monster encounter
                    if monster_alive and player_pos == monster_pos:
                        map_state["player_pos"] = player_pos
                        map_state["town_pos"] = town_pos
                        map_state["monster_pos"] = monster_pos
                        map_state["monster_alive"] = monster_alive
                        pygame.quit()
                        return ("monster", map_state)

        # DRAWING
        screen.fill(BG_COLOR)

        # Grid
        for gx in range(GRID_SIZE):
            for gy in range(GRID_SIZE):
                rect = pygame.Rect(gx * TILE, gy * TILE, TILE, TILE)
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

        # Town
        town_center = (
            town_pos[0] * TILE + TILE // 2,
            town_pos[1] * TILE + TILE // 2
        )
        pygame.draw.circle(screen, TOWN_COLOR, town_center, TILE // 3)

        # Monster
        if monster_alive:
            monster_center = (
                monster_pos[0] * TILE + TILE // 2,
                monster_pos[1] * TILE + TILE // 2
            )
            pygame.draw.circle(screen, MONSTER_COLOR, monster_center, TILE // 3)

        # Player
        player_rect = pygame.Rect(player_pos[0] * TILE, player_pos[1] * TILE, TILE, TILE)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        # Debug overlay
        info = f"Pos: {player_pos}  Town: {town_pos}  Monster: {monster_pos}"
        text = font.render(info, True, (255, 255, 255))
        screen.blit(text, (4, SCREEN_SIZE - 18))

        pygame.display.flip()
        clock.tick(60)

    # Fallback
    map_state["player_pos"] = player_pos
    pygame.quit()
    return ("town", map_state)


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
    monsters = [{"name": "Killer Rabbit of Caerbannog", "description": "A deceptively cute but deadly rabbit with razor sharp teeth.", "health_range": (500,1000), "power_range": (50,80), "money_range": (200,500)},
                {"name": "Insulting Frenchman ", "description": "A castle guard who doesn't take kindly to you. Stay upwind of him!", "health_range": (50,100), "power_range": (10,20), "money_range": (100,150)},
                {"name": "Three-Headed Giant", "description": "A giant with three heads that can't seem to agree with each other.", "health_range": (200,300), "power_range": (30,40), "money_range": (50,100)}]

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


def fight_monster(player, player_hp, player_gold, monster):
    """Fight loop"""
    character_health = player_hp
    monster_health = monster["health"]
    monster_damage = monster["power"]

    print(f"\nA {monster['name']} appears! {monster['description']}")

    if player and check_special_item(player):
        print("The monster is instantly defeated by your special item!")
        player_gold += monster["money"]
        print(f"You found {monster['money']} gold!")
        return character_health, player_gold

    while character_health > 0 and monster_health > 0:
        action = input("\n1) Attack  2) Flee: ")

        if action == "1":

            character_damage = random.randint(25, 75)
        
            if player.get("equippedWeapon"):
                weapon = player["equippedWeapon"]
                character_damage += weapon.get("damage_boost", 0)
                weapon["currentDurability"] -= 1
                print(f"You attack with {weapon['name']}! Durability left: {weapon['currentDurability']}")

                # Remove weapon if durability reaches 0
                if weapon["currentDurability"] <= 0:
                        print(f"Your {weapon['name']} broke!")
                        player["inventory"].remove(weapon)
                        player["equippedWeapon"] = None

                
            monster_health = monster_health - character_damage
            character_health = character_health - monster_damage

            if character_health < 0:
                character_health = 0
            if monster_health < 0:
                monster_health = 0
                
            print(f"You hit the {monster['name']} for {character_damage} damage.")
            print(f"The {monster['name']} hit you for {monster_damage} damage.")



        elif action == "2":
            print("You get too scared. An onlooker to the battle, Sir Robin, joins you momentarily as you bravely run back to town.")
            return character_health, player_gold
        else:
            print("That's not a command, silly.")

    if character_health <= 0 and monster_health > 0:
            print('You lost. Never underestimate an opponent!')
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


def get_shop_items():
    """Return a list of purchasable items"""
    return [
        {"name": "Excalibur", "type": "weapon", "price": 100, "damage_boost": 20, "maxDurability": 10, "currentDurability": 10},
        {"name": "Holy Hand Grenade of Antioch", "type": "special", "price": 500, "note": "Blows one of thine enemies to tiny bits, in thy mercy."}
        ]


def visit_shop(player):
    """Lets player buy items from the shop"""
    shop_items = get_shop_items()
    print("\nWelcome to the shop!")
    print(f"You have {player['gold']} gold.")
    print("Available items:")

    for i, item in enumerate(shop_items, 1):
        print(f"{i}) {item['name'].title()} - {item['price']} gold")

    choice = input("Choose an item to buy or press enter to leave:")
    if not choice.isdigit():
        print("You are leaving the shop. Bye-Bye!")
        return player
    choice = int(choice)
    if 1 <= choice <= len(shop_items):
        item = shop_items[choice - 1]
        if player["gold"] >= item["price"]:
            player["gold"] -= item["price"]
            player["inventory"].append(item)
            print(f"You bought {item['name']}! Remaining gold: {player['gold']}")

        else:
            print("You don't have enough gold. Sorry!")
    else:
        print("That's not a choice")
    return player

def equip_weapon(player):
    weapons = [item for item in player["inventory"] if item["type"] == "weapon"]
    if not weapons:
        print("You do not have any weapons.")
        return

    print("\nChoose a weapon to equip:")
    for i, weapon in enumerate(weapons, 1):
        print(f"{i}) {weapon['name']} (Durability: {weapon['currentDurability']}/{weapon['maxDurability']})")
              
    choice = input("Enter number or press Enter to cancel: ")
    if not choice.isdigit():
        print("No weapon equipped.")
        return

    choice = int(choice)
    if 1 <= choice <= len(weapons):
        player["equippedWeapon"] = weapons[choice-1]
        print(f"You equipped {weapons[choice - 1]['name']}!")


def check_special_item(player):
    for item in player["inventory"]:
        if item["type"] == "special":
            use = input(f"You have {item['name']} that can instantly defeat the monster. Use it? (y/n): ").lower()
            if use == "y":
                player["inventory"].remove(item)
                print(f"You used {item['name']}! The monster is defeated instantly.")
                return True
    return False
    
        
        
    
    

    
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
