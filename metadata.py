# Modify these constants
GUARDIAN_STONE_COST = 53/10
DESTRUCTION_STONE_COST = 96/10
LEAPSTONE_COST = 169
SHARD_COST = 83/500
SOLAR_GRACE_COST = 59
SOLAR_BLESSING_COST = 240
SOLAR_PROTECTION_COST = 584


# Metadata, should not change
class Metadata():
    chanceToHone = 0
    stones = 0
    leaps = 0
    shards = 0
    graceChance = 0
    blessingChance = 0
    protectionChance = 0

    @property
    def totalCost(self):
        return -1

    def getString(self):
        return "undefined"

class MetadataA(Metadata):
    @property
    def totalCost(self):
        return self.leaps*LEAPSTONE_COST + self.shards*SHARD_COST + self.stones*GUARDIAN_STONE_COST 

    def getString(self):
        return "Armor"

class MetadataW(Metadata):
    @property
    def totalCost(self):
        return self.leaps*LEAPSTONE_COST + self.shards*SHARD_COST + self.stones*DESTRUCTION_STONE_COST

    def getString(self):
        return "Weapon"


class Metadata7A(MetadataA):
    chanceToHone = .6
    stones = 156
    leapStones = 4
    shards = 42
    graceChance = 0.0167
    blessingChance = 0.0333
    protectionChance = 0.1

    def getString(self):
        return super().getString() + " 6 -> 7"

class Metadata8A(MetadataA):
    chanceToHone = .45
    stones = 156
    leapStones = 4
    shards = 42
    graceChance = 0.0125
    blessingChance = 0.025
    protectionChance = 0.075

    def getString(self):
        return super().getString() + " 7 -> 8"

class Metadata9A(MetadataA):
    chanceToHone = .3
    stones = 156
    leapStones = 4
    shards = 42
    graceChance = 0.0084
    blessingChance = 0.0167
    protectionChance = 0.05

    def getString(self):
        return super().getString() + " 8 -> 9"

class Metadata10A(MetadataA):
    chanceToHone = .3
    stones = 192
    leapStones = 6
    shards = 50
    graceChance = 0.0084
    blessingChance = 0.00167
    protectionChance = 0.05

    def getString(self):
        return super().getString() + " 9 -> 10"