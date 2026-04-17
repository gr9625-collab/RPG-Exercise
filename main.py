from combat import Dungeon
from data import hero_dict, enemy_dict

dungeon = Dungeon(hero_dict["Warrior"], enemy_dict)
dungeon.run()

# Next you want to add item drops from each enemy, as well as resistance items and damage boost items
# Also rewards for beating dungeon levels etc
# And the dragon should only appear towards the later levels