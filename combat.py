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

        # Crit checker (10% chance of crit)
        if random.random() > 0.9:
            crit_modifier = 1.5
            is_crit = True
        else:
            crit_modifier = 1
            is_crit = False

        damage = math.ceil(raw_damage * type_modifier * crit_modifier)

        return damage, is_crit
    
    def use_item(self, player, item):
        if item.effect == "heal":
            old_hp = player.current_hp
            player.current_hp = min(player.max_hp, player.current_hp + (50 * item.strength))
            time.sleep(1)
            print(f"{player.name} used {item.name}.")
            time.sleep(1)
            print(f"{player.name} gained {player.current_hp - old_hp} health!")
    
        player.inventory.items.remove(item)
    
    def half_turn(self, attacker, defender, action, item_input):
        if action == "run":
            time.sleep(1)
            print("You run away!")
            return "run"
        elif action == "attack":
            damage, is_crit = self.calculate_damage(attacker, defender)
            time.sleep(1)
            print(f"{attacker.name} attacks with {attacker.equipped_weapon.name}!")
            if is_crit:
                time.sleep(1)
                print("It's a critical hit!")
            time.sleep(1)
            print(f"{defender.name} takes {damage} damage!")
            self.take_damage(defender, damage)

            if not defender.is_alive():
                time.sleep(1)
                print(f"{defender.name} was slain!")
                return "defender_dead"

        elif action == "item":
            self.use_item(attacker, attacker.inventory.items[item_input - 1])
        return "continue"

    def turn(self):
        hero = self.hero
        enemy =  self.enemy
        time.sleep(1)
        print("-----------")
        print(f"New Turn: Current health {hero.current_hp}/{hero.max_hp}")
        print("-----------")
        item_input = None
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
                item_input = int(input("Use which item: "))
            break

        # Choose who goes first based on speed
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

        if first_player == hero:
            first_player_action = user_input
            second_player_action = "attack"
        else:
            first_player_action = "attack"
            second_player_action = user_input

        result = self.half_turn(first_player, second_player, first_player_action, item_input)
        if result in ["run", "defender_dead"]:
            if result == "run":
                return "run"
            else:
                if second_player == hero:
                    return "hero_dead"
                else:
                    return "enemy_dead"

        result = self.half_turn(second_player, first_player, second_player_action, item_input)
        if result in ["run", "defender_dead"]:
            if result == "run":
                return "run"
            else:
                if first_player == hero:
                    return "hero_dead"
                else:
                    return "enemy_dead"

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
