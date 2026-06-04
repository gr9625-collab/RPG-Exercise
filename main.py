from combat import Dungeon
from data import hero_dict, enemy_dict

dungeon = Dungeon(hero_dict["Warrior"], enemy_dict)
dungeon.run()

# Add rewards for beating dungeon levels
# And the dragon should only appear towards the later levels

# There is currently the problem if two players die on the same turn (what should happen here?)

# Add resistances as a class, and also damage buffs/nerfs
