from enum import Enum

# HX: Breakup program into "Get keywords of cards", "Produce matrix", "Show on site"
# HX: Rarity breakdown
# HX: With Prowess, add toggle for number of spells on stack
# HX: Compile python

# Combat-related keywords
# HX: Protection
KEYWORDS = ["Deathtouch",
            "Defender",
            "Double strike",
            "First strike",
            "Flying",
            "Indestructible",
            "Prowess",
            "Reach",
            "Skulk"]

class Result(Enum):
    depends = 0 # Assigned manually
    NA = 1
    no_win = 2
    left_win = 3
    right_win = 4
    both_win = 5
    unblocked = 6

class Creature():
    def __init__(self, card_dict):
        self.name = card_dict["name"]
        self.damage = 0
        # Keep track of problematic creatures
        self.problematic = False
        try:
            self.power = int(card_dict["power"])
            self.toughness = int(card_dict["toughness"])
        except ValueError:
            self.power = 0
            self.toughness = 0
            self.problematic = True
        try:
            self.keywords = card_dict["keywords"]
        except KeyError:
            self.keywords = []
    
    def hasKW(self, keyword):
        return keyword in self.keywords
    
    def reset_dmg(self):
        self.damage = 0
        
    def __str__(self):
        return self.name
    
def kills( attacker, blocker, useDamage=False ):
    limit = blocker.toughness - blocker.damage if useDamage \
            else blocker.toughness
    return (not blocker.hasKW("Indestructible") and
            ((attacker.power >= limit) or
            (attacker.power > 0 and attacker.hasKW("Deathtouch"))))

"""
Returns result of combat when index_l attacks and index_r blocks
"""
def combat(index_l, index_r):
    print("( %s ) vs ( %s )" % (creature_list[index_l].name,
                                creature_list[index_r].name))
    attack = creature_list[index_l]
    block = creature_list[index_r]
    
    if (attack.problematic or block.problematic):
        return Result.depends
    rv = 2
    # Can attacker attack?
    if (attack.hasKW("Defender")):
        return Result.NA
    # Can blocker block?
    if ((attack.hasKW("Flying") and (not block.hasKW("Flying") or
         not block.hasKW("Reach"))) or 
        (attack.hasKW("Skulk") and block.power > attack.power)):
        return Result.unblocked
    # First strike
    if (attack.hasKW("First strike") or attack.hasKW("Double strike")):
        if (kills(attack, block)):
            rv += 1
        else:
            block.damage += attack.power
    if (block.hasKW("First strike") or block.hasKW("Double strike")):
        if (kills(block, attack)):
            rv += 2
        else:
            attack.damage += block.power
    # Normal combat
    if (not attack.hasKW("First strike") and kills(attack, block, True)):
        rv += 1
    if (not block.hasKW("First strike") and kills(block, attack, True)):
        rv += 2
    attack.reset_dmg()
    block.reset_dmg()
    return Result(rv)
