class Item:
    def __init__(self, name, effect, effect_type, strength, duration=1):
        self.name = name
        # Effects are type resistance (e.g. fire, slash, blunt, pierce etc), damage boost, health gain
        self.effect = effect
        # Which type of resistance etc
        self.effect_type = effect_type
        # Strength can be 1 or 2 (different levels)
        self.strength = strength
        # How long the effect lasts for
        self.duration = duration

class Inventory:
    def __init__(self, weapons, items):
        self.weapons = weapons
        self.items = items

class Weapon:
    def __init__(self, name, damage, damage_type):
        self.name = name
        self.damage = damage
        self.damage_type = damage_type

class Player:
    def __init__(self, name, hp, speed, inventory, weaknesses, resistances):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.equipped_weapon = inventory.weapons[0]
        self.speed = speed
        self.inventory = inventory
        self.weaknesses = weaknesses
        self.resistances = resistances
        self.temporary_resistances = {}

    def is_alive(self):
        return self.current_hp > 0