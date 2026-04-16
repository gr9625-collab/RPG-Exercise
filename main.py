from combat import Dungeon
from data import hero_dict, enemy_dict

dungeon = Dungeon(hero_dict["Warrior"], enemy_dict)
dungeon.run()