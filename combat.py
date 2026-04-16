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
        return None
    
    # Make the half turn stuff happen here (different things depending on the action)
    def half_turn(self, attacker, defender, action):
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
            time.sleep(1)
            for i, item in enumerate(attacker.inventory.items):
                time.sleep(1)
                print(f"{i + 1}: {item.name}")
            time.sleep(1)
            item_input = int(input("Use which item: "))
            self.use_item(attacker, attacker.inventory.items[item_input - 1])

        return None

    # This code is fucked, it needs to always assign the faster/slower players first. Then do the actions run/attack/item.
    def turn(self):
        hero = self.hero
        enemy =  self.enemy
        time.sleep(1)
        print("-----------")
        print(f"New Turn: Current health {hero.current_hp}/{hero.max_hp}")
        print("-----------")
        time.sleep(1)
        user_input = input("Choose your action (attack/run/item): ")

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

        # Update this to make you take a hit if you go second (even if you run)
        if user_input == "run":
            # Make user run, not first player
            self.half_turn(first_player, second_player, "run")

        elif user_input == "attack":
                # First player attacks
                damage, is_crit = self.calculate_damage(first_player, second_player)
                time.sleep(1)
                print(f"{first_player.name} attacks with {first_player.equipped_weapon.name}!")
                if is_crit:
                    time.sleep(1)
                    print("It's a critical hit!")
                time.sleep(1)
                print(f"{second_player.name} takes {damage} damage!")
                self.take_damage(second_player, damage)

                if not second_player.is_alive():
                    time.sleep(1)
                    print(f"{second_player.name} was slain!")
                    if second_player == enemy:
                        return "enemy_dead"
                    else:
                        return "hero_dead"
                
                # Now the second player attacks
                damage, is_crit = self.calculate_damage(second_player, first_player)
                time.sleep(1)
                print(f"{second_player.name} attacks with {second_player.equipped_weapon.name}!")
                if is_crit:
                    time.sleep(1)
                    print("It's a critical hit!")
                time.sleep(1)
                print(f"{first_player.name} takes {damage} damage!")
                self.take_damage(first_player, damage)

                if not first_player.is_alive():
                    time.sleep(1)
                    print(f"{first_player.name} was slain!")
                    if first_player == enemy:
                        return "enemy_dead"
                    else:
                        return "hero_dead"
        elif user_input == "item":
            time.sleep(1)
            for i, item in enumerate(hero.inventory.items):
                time.sleep(1)
                print(f"{i + 1}: {item.name}")
            time.sleep(1)
            item_input = int(input("Use which item: "))
            self.use_item(hero, hero.inventory.items[item_input - 1])
    
        else:
            print("Invalid action")
            return "continue"

        print("")

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
