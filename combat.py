import random
import time
import math
import copy

from entities import Player
from data import enemy_dict


class Battle:
    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy

    def take_damage(self, player, damage):
        player.current_hp -= damage
        if player.current_hp < 0:
            player.current_hp = 0

    def calculate_damage(self, attacker, defender):
        raw_damage = attacker.equipped_weapon.damage

        # Type modifiers (e.g. weaknesses and resistances)
        if attacker.equipped_weapon.damage_type in defender.weaknesses:
            type_modifier = 2
        elif attacker.equipped_weapon.damage_type in defender.resistances:
            type_modifier = 0.5
        else:
            type_modifier = 1

        # Temporary resistance modifiers
        temp_modifier = 1
        if (
            attacker.equipped_weapon.damage_type
            in defender.temporary_resistances.keys()
        ):
            temp_modifier = (
                1
                - defender.temporary_resistances[attacker.equipped_weapon.damage_type][
                    "strength"
                ]
                * 0.33
            )

        # Crit checker (10% chance of crit)
        if random.random() > 0.9:
            crit_modifier = 1.5
            is_crit = True
        else:
            crit_modifier = 1
            is_crit = False

        damage = math.ceil(raw_damage * type_modifier * temp_modifier * crit_modifier)

        return damage, is_crit

    # This should apply status effects for both weapons and item
    def apply_status_effect(
        self,
        player,
        status_effect,
        duration,
        strength=None,
    ):
        player.status_effects[status_effect.name] = {
            "strength": strength,
            "duration": duration,
        }

        return None

    def use_item(self, player, item):
        if item.effect == "heal":
            old_hp = player.current_hp
            player.current_hp = min(
                player.max_hp, player.current_hp + (50 * item.strength)
            )
            time.sleep(1)
            print(f"{player.name} used {item.name}.")
            time.sleep(1)
            print(f"{player.name} gained {player.current_hp - old_hp} health!")

        if item.effect == "resistance":
            time.sleep(1)
            print(f"{player.name} used {item.name}.")
            time.sleep(1)
            print(f"{player.name} gained resistance to {item.effect_type}!")
            player.temporary_resistances[item.effect_type] = {
                "strength": item.strength,
                "duration": item.duration,
            }

        player.inventory.items.remove(item)

    # Updates the statuses as the end of each turn

    def update_status(self, player):
        # Updates temporary resistances
        for damage_type in list(player.temporary_resistances.keys()):
            player.temporary_resistances[damage_type]["duration"] -= 1
            if player.temporary_resistances[damage_type]["duration"] == 0:
                player.temporary_resistances.pop(damage_type)
                time.sleep(1)
                print(f"{player.name}'s resistance to {damage_type} wore off!")
        return None

    def perform_attack(self, attacker, defender):
        damage, is_crit = self.calculate_damage(attacker, defender)
        time.sleep(1)
        print(f"{attacker.name} attacks with {attacker.equipped_weapon.name}!")
        if is_crit:
            time.sleep(1)
            print("It's a critical hit!")
        time.sleep(1)
        print(f"{defender.name} takes {damage} damage!")
        self.take_damage(defender, damage)

    def half_turn(self, attacker, defender, action, item=None):
        if action == "run":
            time.sleep(1)
            print("You run away!")
            return "run"
        elif action == "attack":
            self.perform_attack(attacker, defender)
            if not defender.is_alive():
                time.sleep(1)
                print(f"{defender.name} was slain!")
                return "defender_dead"

        elif action == "item":
            if attacker == self.enemy:
                item = random.choice(attacker.inventory.items)
            self.use_item(attacker, item)
        return "continue"

    def choose_enemy_action(self, enemy):
        if random.random() < 0.2 and enemy.inventory.items:
            return "item"
        return "attack"

    def get_player_action(self):
        hero = self.hero
        item_input = None
        selected_item = None
        while True:
            time.sleep(1)
            user_input = input("Choose your action (attack/run/item): ")
            if user_input == "item":
                if hero.inventory.items == []:
                    time.sleep(1)
                    print("You have no items!")
                    continue
                for i, item in enumerate(hero.inventory.items):
                    time.sleep(1)
                    print(f"{i + 1}: {item.name}")
                time.sleep(1)
                while True:
                    try:
                        item_input = int(input("Use which item: "))
                        if 1 <= item_input <= len(hero.inventory.items):
                            selected_item = hero.inventory.items[item_input - 1]
                            break
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Enter a number.")
            break
        return user_input, selected_item

    def get_turn_order(self):
        hero = self.hero
        enemy = self.enemy
        if hero.speed > enemy.speed:
            first_player = hero
            second_player = enemy
        elif hero.speed < enemy.speed:
            first_player = enemy
            second_player = hero
        else:
            if random.random() < 0.5:
                first_player = hero
                second_player = enemy
            else:
                first_player = enemy
                second_player = hero
        return first_player, second_player

    def turn(self):
        hero = self.hero
        enemy = self.enemy
        time.sleep(1)
        print("-----------")
        print(f"New Turn: Current health {hero.current_hp}/{hero.max_hp}")
        print("-----------")

        user_input, selected_item = self.get_player_action()

        first_player, second_player = self.get_turn_order()

        if first_player == hero:
            first_player_action = user_input
            second_player_action = self.choose_enemy_action(enemy)
        else:
            first_player_action = self.choose_enemy_action(enemy)
            second_player_action = user_input

        if first_player == hero:
            result = self.half_turn(
                first_player, second_player, first_player_action, selected_item
            )
        else:
            result = self.half_turn(first_player, second_player, first_player_action)
        if result in ["run", "defender_dead"]:
            if result == "run":
                return "run"
            else:
                if second_player == hero:
                    return "hero_dead"
                else:
                    self.update_status(hero)
                    return "enemy_dead"

        if second_player == hero:
            result = self.half_turn(
                second_player, first_player, second_player_action, selected_item
            )
        else:
            result = self.half_turn(second_player, first_player, second_player_action)
        if result in ["run", "defender_dead"]:
            if result == "run":
                return "run"
            else:
                if first_player == hero:
                    return "hero_dead"
                else:
                    self.update_status(hero)
                    return "enemy_dead"

        self.update_status(first_player)
        self.update_status(second_player)

        return "continue"

    def run(self):
        enemy = self.enemy
        print("")
        print(f"**{enemy.name} appears!**")
        print("")

        while True:
            result = self.turn()

            if result in ["run", "enemy_dead", "hero_dead"]:
                return result


class Dungeon:
    def __init__(self, hero, enemies):
        self.hero = hero
        self.enemies = enemies

    def run(self):
        dungeon_level = 0
        while True:
            time.sleep(1)
            print(f"\nYou descend to dungeon level {dungeon_level + 1}\n")
            time.sleep(1)
            enemy_name = random.choice(list(self.enemies.keys()))
            battle = Battle(self.hero, copy.deepcopy(enemy_dict[enemy_name]))
            results = battle.run()
            if results == "hero_dead" or results == "run":
                break
            dungeon_level += 1
        time.sleep(1)
        print(f"\nYou completed {dungeon_level} dungeon levels in total!")
