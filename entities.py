class Item:
    def __init__(self, name, effect, effect_type, strength, duration):
        self.name = name
        # Effects are type resistance (e.g. fire, slash, blunt, pierce etc), damage boost, health gain
        self.effect = effect
        # Which type of resistance etc
        self.effect_type = effect_type
        # Strength can be 1 or 2 (different levels)
        self.strength = strength
        # How long the effect lasts for
        self.duration = duration


class StatusEffect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def on_turn_end(self, target):
        pass


class Poison(StatusEffect):
    def __init__(self, duration):
        super().__init__("Poison", duration)

    def on_turn_end(self, target):
        target.current_hp -= 5
        self.duration -= 1


# Try to make a poision dagger weapon that gives the poison status effect
# Test this out before making more status effects


class Resistance(StatusEffect):
    def __init__(self, duration, resistance_type, strength):
        super().__init__("Resistance", duration)
        self.strength = strength
        self.resistance_type = resistance_type


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
        self.status_effects = []

    def is_alive(self):
        return self.current_hp > 0
