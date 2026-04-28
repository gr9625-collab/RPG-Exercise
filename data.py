from entities import Player, Weapon, Inventory, Item, StatusEffect, Poison

# Dictionary of items
item_dict = {
    "Minor health potion": Item(
        "Minor Health Potion",
        "heal",
        None,
        1,
        None,
    ),
    "Major health potion": Item(
        "Major Health Potion",
        "heal",
        None,
        2,
        None,
    ),
    "Vial of squonk tears": Item(
        "Vial of squonk tears",
        "resistance",
        "fire",
        1,
        5,
    ),
    "Potion of fire resistance": Item(
        "Potion of fire resistance",
        "resistance",
        "fire",
        2,
        5,
    ),
}

# Dictionary of weapons
weapon_dict = {
    "Poison dagger": Weapon(
        "Poison dagger",
        5,
        "piece",
        [
            {
                "status_class": Poison,
                "duration": 5,
                "chance": 1,
            },
        ],
    ),
    "Sword of Destiny": Weapon(
        "Sword of Destiny",
        20,
        "slash",
        [],
    ),
    "Wooden club": Weapon(
        "Wooden club",
        5,
        "blunt",
        [],
    ),
    "Rusty sword": Weapon(
        "Rusty sword",
        15,
        "slash",
        [],
    ),
    "Fire breath": Weapon(
        "Fire breath",
        50,
        "fire",
        [],
    ),
    "Small bow": Weapon(
        "Small bow",
        10,
        "pierce",
        [],
    ),
    "Cute snuffle": Weapon(
        "Cute snuffle",
        0,
        "magic",
        [],
    ),
    "Interdimensional tentacle": Weapon(
        "Interdimensional tentacle",
        15,
        "magic",
        [],
    ),
    "Cry of shame": Weapon(
        "Cry of shame",
        0,
        "magic",
        [],
    ),
}

# Dictionary of playable heroes
hero_dict = {
    "Warrior": Player(
        "Warrior",
        100,
        75,
        Inventory(
            [weapon_dict["Poison dagger"]],
            [
                item_dict["Minor health potion"],
                item_dict["Vial of squonk tears"],
            ],
        ),
        [],
        [],
    )
}

# Make a mimic enemy (of course)
# Dictionary of enemies
enemy_dict = {
    "Goblin": Player(
        "Goblin", 30, 75, Inventory([weapon_dict["Wooden club"]], []), [], []
    ),
    "Orc": Player("Orc", 40, 60, Inventory([weapon_dict["Rusty sword"]], []), [], []),
    "Skeleton": Player(
        "Skeleton", 35, 25, Inventory([weapon_dict["Rusty sword"]], []), [], []
    ),
    "Dragon": Player(
        "Dragon", 200, 25, Inventory([weapon_dict["Fire breath"]], []), [], []
    ),
    "Gnome archer": Player(
        "Gnome archer", 20, 80, Inventory([weapon_dict["Small bow"]], []), [], []
    ),
    "Flying piglett": Player(
        "Flying piglett", 1, 100, Inventory([weapon_dict["Cute snuffle"]], []), [], []
    ),
    "Four-dimensional octopus": Player(
        "Four-dimensional octopus",
        10,
        100,
        Inventory([weapon_dict["Interdimensional tentacle"]], []),
        [],
        [],
    ),
    "Squonk": Player(
        "Squonk", 25, 30, Inventory([weapon_dict["Cry of shame"]], []), [], []
    ),
}
