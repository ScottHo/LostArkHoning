import pprint
from metadata import *

DEBUG = False

class Hone():
    def __init__(self, metadata):
        self.database = {}
        self._memoChance = {}
        self.metadata = metadata
        self.minCost = 99999999
        self.minKey = ""
        return

    def getChance(self, numGrace, numBlessing, numProtection, previousFails):
        """
        Get the chance to hone given helper materials and pity rate
        """
        chanceToHone = self.metadata.chanceToHone
        graceRate = numGrace*self.metadata.graceChance
        blessingRate = numBlessing*self.metadata.blessingChance
        protectionRate = numProtection * self.metadata.protectionChance
        pityRate = previousFails*chanceToHone*.10
        return chanceToHone+graceRate+blessingRate+protectionRate+pityRate

    def getCost(self, numGrace, numBlessing, numProtection):
        """
        Get the cost per hone including helper materials
        """
        graceCost = numGrace*SOLAR_GRACE_COST
        blessingCost = numBlessing*SOLAR_BLESSING_COST
        protectionCost = numProtection*SOLAR_PROTECTION_COST
        return self.metadata.totalCost+graceCost+blessingCost+protectionCost


    def getArtisanEnergy(self, numGrace, numBlessing, numProtection):
        """
        Get the artisan energy acquired if the current hone fails
        """
        graceBonus = numGrace*self.metadata.graceChance*.465
        blessingBonus = numBlessing*self.metadata.blessingChance*.465
        protectionBonus = numProtection * self.metadata.protectionChance*.465
        failBonus = self.metadata.chanceToHone*.465
        return graceBonus + blessingBonus + protectionBonus + failBonus


    def storeNextCost(self, previousFails, artisanEnergy, fullKey, accumulatedChance, totalPreviousCost):
        """
        Recursively calculate the average cost of the following combination of mats
        """
        for protection in range(3):
            for blessing in range(7):
                for grace in range(13):
                    key = fullKey+"{}-{}-{}... ".format(grace, blessing, protection)
                    cost = self.getCost(grace, blessing, protection)
                    chance = self.getChance(grace, blessing, protection, previousFails+1)
                    if artisanEnergy >= 1 or chance >= 1:
                        cost = totalPreviousCost + cost*(1.0-accumulatedChance)
                        if (cost < self.minCost):
                            self.minCost = cost
                            self.minKey = key
                        return
                    else:
                        thisCost = (1.0-accumulatedChance)*cost
                        if totalPreviousCost+thisCost > self.minCost:
                            return
                        thisChance = (1.0-accumulatedChance)*chance
                        artisanEnergyToGain = self.getArtisanEnergy(grace, blessing, protection)
                        self.storeNextCost(previousFails+1, artisanEnergy+artisanEnergyToGain, key, accumulatedChance + thisChance, totalPreviousCost + thisCost)


    def getBestRate(self):
        """
        For each combination of helper mats, find the best average cost 
        """
        for protection in range(3):
            for blessing in range(7):
                for grace in range(13):
                    key = "{}-{}-{}... ".format(grace, blessing, protection)
                    cost = self.getCost(grace, blessing, protection)
                    chance = self.getChance(grace, blessing, protection, 0)
                    artisanEnergy = self.getArtisanEnergy(grace, blessing, protection)
                    self.storeNextCost(0, artisanEnergy, key, chance, cost)

        print(self.metadata.getString(), self.minKey, "Average Cost: {}".format(round(self.minCost, 2)))

if __name__ == '__main__':
    Hone(Metadata7A()).getBestRate()
    Hone(Metadata8A()).getBestRate()
    Hone(Metadata9A()).getBestRate()
    Hone(Metadata10A()).getBestRate()
