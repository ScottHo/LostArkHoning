import random
import pprint
from collections import OrderedDict

class Metadata():
    chanceToHone = 0
    addedChanceToSucceed = 0 
    addCost = 0
    totalCost = 0

    def getData(self):
        return [self.chanceToHone, self.totalCost, self.addCost, self.addedChanceToSucceed]

    def getString(self):
        return "undefined"

# Change addCost and totalCost based on prices
class Metadata8W(Metadata):
    chanceToHone = .45
    addedChanceToSucceed = 0.025
    addCost = 131
    totalCost = 1510

    def getString(self):
        return "Weapon 7 -> 8"


class Hone():
    def __init__(self, chanceToHone, totalCost, addCost, addedChanceToSucceed):
        self.chanceToHone = chanceToHone
        self.totalCost = totalCost
        self.addCost = addCost
        self.addedChanceToSucceed = addedChanceToSucceed

    def run(self):
        artisanEnergy = 0
        cost = 0 
        baseChanceToSucceed = self.chanceToHone
        increasePerFail = .1*baseChanceToSucceed
        numAdded = 0
        count = 0
        addsUsed = []
        while (True):
            chanceToSucceed = baseChanceToSucceed
            artisanEnergyToAdd = chanceToSucceed*.465
            cost += self.totalCost

            if (artisanEnergy >= 1):
                addsUsed.append(0)
                break
            maxAdds = int(.45/self.addedChanceToSucceed)
            if (1 - chanceToSucceed < .45):
                maxAdds = int((1 - chanceToSucceed) / self.addedChanceToSucceed)
            if (maxAdds > 1):
                addsToUse = random.randrange(0, maxAdds)
            else:
                addsToUse = 0

            cost += addsToUse * self.addCost
            chanceToSucceed += addsToUse*self.addedChanceToSucceed
            addsUsed.append(addsToUse)

            if random.random() < chanceToSucceed:
                break
            else:
                artisanEnergy += artisanEnergyToAdd
                artisanEnergy += .007*numAdded
                baseChanceToSucceed += increasePerFail
            count += 1

        return cost, addsUsed

def simulate(metadata, runs, extraLogging, firstMoon=-1):
    def fill(valueKey, countKey, primeKey, currentDict, value):
        if valueKey not in currentDict:
            currentDict[valueKey] = 0
        if countKey not in currentDict:
            currentDict[countKey] = 0
        if primeKey not in currentDict:
            currentDict[primeKey] = {}
        currentDict[valueKey] += value
        currentDict[countKey] += 1
    h = {}
    for r in range(runs):
        hone = Hone(*metadata.getData())
        cost, addsUsed = hone.run()
        currentDict = h
        key = str(addsUsed[0])
        primeKey = key + "p"
        countKey = key + "c"
        fill(key, countKey, primeKey, currentDict, cost)

        for i in range(1, len(addsUsed)):
            currentDict = currentDict[primeKey]
            key = str(addsUsed[i])
            primeKey = key + "p"
            countKey = key + "c"
            fill(key, countKey, primeKey, currentDict, cost)


    currentH = h
    firstRound = {}
    for k, v in currentH.items():
        if "c" not in k and "p" not in k:
            firstRound[int(k)] = v/currentH[k+"c"]
    firstRoundMin = min(firstRound, key=firstRound.get)
    if (extraLogging):
        for k, v in sorted(firstRound.items()):
            print("R1 {} : {}, runs: {}".format(k, round(v, 2), currentH[str(k)+"c"]))

    secondRound = {}
    secondRoundKey = str(firstRoundMin) + "p"
    currentH = h[secondRoundKey]
    for k, v in currentH.items():
        if "c" not in k and "p" not in k:
            secondRound[int(k)] = v/currentH[k+"c"]
    if len(secondRound) == 0:
        print(metadata.getString() + " Adds: {}".format(firstRoundMin))
        return
    secondRoundMin = min(secondRound, key=secondRound.get)
    if (extraLogging):
        print("Using {} adds from round 1".format(firstRoundMin))
        for k, v in sorted(secondRound.items()):
            print("--R2 {} : {}, runs: {}".format(k, round(v, 2), currentH[str(k)+"c"]))

    thirdRound = {}
    thirdRoundKey = str(secondRoundMin) + "p"
    currentH = h[secondRoundKey][thirdRoundKey]
    for k, v in currentH.items():
        if "c" not in k and "p" not in k:
            thirdRound[int(k)] = v/currentH[k+"c"]
    if len(thirdRound) == 0:
        print(metadata.getString() + " Adds: {}, {}".format(firstRoundMin, secondRoundMin))
        return
    thirdRoundMin = min(thirdRound, key=thirdRound.get)
    if (extraLogging):
        print("Using {} adds from round 2".format(secondRoundMin))
        for k, v in sorted(thirdRound.items()):
            print("----R3 {} : {}, runs: {}".format(k, round(v, 2), currentH[str(k)+"c"]))

    print(metadata.getString() + " Adds: {}, {}, {}".format(firstRoundMin, secondRoundMin, thirdRoundMin))
    return

if __name__ == '__main__':
    extraLogging = True
    runs = 9999999
    simulate(Metadata8W(), runs, extraLogging)
    
