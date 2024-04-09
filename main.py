import time
import random
import pickle
import os.path
import math
 
class Enemy:
  def __init__(self, name, health, ac, damage, attackModifier, coinsToGiveOnDeath, xpToGiveOnDeath):
    self.name = name
    self.health = health
    self.damage = damage
    self.attackModifier = attackModifier
    self.ac = ac
    self.coinsToGiveOnDeath = coinsToGiveOnDeath
    self.xpToGiveOnDeath = xpToGiveOnDeath

#Adding dice rolls to weapon damage
class Weapon:
  def __init__(self, name, damage, retreatDamage, cost):
    self.name = name
    self.baseDamage = int(damage.split(" + ")[1])
    damage = damage.split(" + ")[0]
    self.number = int(damage.split("d")[0])
    self.dice = int(damage.split("d")[1])
    self.damage = damage
    self.retreatDamage = retreatDamage
    self.retreatBaseDamage = int(retreatDamage.split(" + ")[1])
    self.retreatNumber = int((retreatDamage.split(" + ")[0]).split("d")[0])
    self.retreatDice = int((retreatDamage.split(" + ")[0]).split("d")[1])
    self.cost = int(cost)

class Player:
  def __init__(self, name, ac, attackModifier, weaponList, coins, xp=0):
    self.name = name
    self.health = 10
    self.ac = ac
    self.attackModifier = attackModifier
    self.weaponList = weaponList
    self.coins = coins
    self.xp = xp
    self.level = self.setPlayerLevel()
    self.status = "Not in combat"
  def __reduce__(self):
    return (self.__class__, (self.name, self.ac, self.attackModifier, self.weaponList, self.coins, self.xp))
  def setPlayerLevel(self):
    self.level = math.floor(math.sqrt(self.xp))
  def xpIncrease(self, increase):
    self.xp += increase
    previousLevel = self.level
    self.setPlayerLevel()
    if (previousLevel < self.level):
      print(f"Congradulations {self.name}, you have leveled up! You are now level {self.level}.")
      time.sleep(1)

availableWeapons = [Weapon("Dagger", "1d4 + 0", "0d4 + 0", 1), Weapon("Short Sword", "3d4 + 1", "0d4 + 0", 5), Weapon("Training Bow", "0d4 + 0", "1d4 + 0", 3)]

def SaveData(allPlayers, availableWeapons):
  with open('playerData.pkl', 'wb') as file:
    pickle.dump([allPlayers, availableWeapons], file)

def LoadData():
  global availableWeapons
  global allPlayers
  with open('playerData.pkl', 'rb') as file:
    saveFile = pickle.load(file)
    allPlayers = saveFile[0]
    availableWeapons = saveFile[1]
    print(f"You are playing a {len(allPlayers)} player game.")
    print("The players are ")
    for player in allPlayers:
      player.setPlayerLevel()
      print(f"{player.name} who is on level {player.level} with {player.coins} coins")
      print(f"The weapons {player.name} has are")
      for weapon in player.weaponList:
        print(f"{weapon.name} that does {weapon.damage} damage")

def AskQuestion(questionText, validResults: list):
  userAnswer = input(questionText)
  if (userAnswer in validResults):
    return userAnswer
  else:
    time.sleep(0.5)
    print("That wasn't a valid answer")
    time.sleep(0.5)
    print("Try again")
    time.sleep(0.5)
    return AskQuestion(questionText, validResults)

def StartArea():
  time.sleep(1)
  print("\nYou are at the front of the dungeon")
  time.sleep(0.5)
  userResponse = AskQuestion(
      "Whould you like to go visit the shope, enter the dungeon, or leave the game (shop/dungeon/leave)? ",
      ["shop", "dungeon", "leave"])
  if (userResponse == "shop"):
    print("You are visiting the shop")
    Shop()
  elif userResponse == "dungeon":
    Dungeon()
  else:
    SaveData(allPlayers, availableWeapons)
    exit()

def BuyItem(availableItems, player):
  itemNames = [item.name for item in availableItems]
  userChoice = AskQuestion("What would you like to buy? ", itemNames)
  itemBuying = availableItems[itemNames.index(userChoice)]
  if (player.coins >= itemBuying.cost):
    player.coins -= itemBuying.cost
    player.weaponList.append(itemBuying)
    print(f"You bought a {itemBuying.name} for {itemBuying.cost} coins")
    print(f"You now have {player.coins} coins")
    print(len(player.weaponList))
  else:
    print("You don't have enough coins to buy that")
  userChoice = AskQuestion("Whould you like to buy anything else? ", ["yes", "no"])
  if (userChoice == "yes"):
    BuyItem(availableItems, player)

shopWeapons = []

def RandomiseShopItems():
  global shopWeapons
  shopWeapons = [random.choices(availableWeapons, k=5)][0]
RandomiseShopItems()

def Shop():
  time.sleep(1)
  print("\nYou are at the shop")
  time.sleep(0.2)
  print("Here are your weapon choices")
  for weapon in shopWeapons:
    print(f"This weapon is a {weapon.name} that does {weapon.damage} damage and costs {weapon.cost} coins.")
  for player in allPlayers:
    userChoice = AskQuestion(f"Whould {player.name} like to buy anything? ", ["yes", "no"])
    if (userChoice == "yes"):
      BuyItem(shopWeapons, player)
    userChoice = AskQuestion(f"Whould {player.name} like to sell anything? ", ["yes", "no"])
    if (userChoice == "yes"):
      SellItems(player)
  print("Come back later when the items will be refreshed")
  StartArea()

def SellItems(player: Player):
  if (len(player.weaponList) > 1):
    print("These are your items")
    userChoices = []
    for weapon in player.weaponList:
      print(f"{weapon.name} is a weapon that does {weapon.damage} damage and can be sold for {math.floor(weapon.cost / 2)}")
      userChoices.append(weapon.name)
    userChoices.append("cancel")
    userChoice = AskQuestion("What would you like to sell or would you like to cancel the transaction? ", userChoices)
    if (userChoice != "cancel"):
      weaponSelling = player.weaponList[userChoices.index(userChoice)]
      coinsGotBack = math.floor(weaponSelling.cost / 2)
      player.coins += coinsGotBack
      player.weaponList.remove(weaponSelling)
      print(f"{player.name} sold their {weaponSelling.name} for {coinsGotBack} coins.")
      userChoice = AskQuestion("Whould you like to sell another weapon? ", ["yes", "no"])
      if (userChoice == "yes"):
        SellItems(player)
      else:
        SaveData(allPlayers, availableWeapons)
  else:
    print("You cannot sell your last weapon")
    SaveData(allPlayers, availableWeapons)

roomEnemies = [
  [Enemy("Green Slime", 1, 5, 1, 0, 1, 1)],
  [Enemy("Green Slime", 1, 5, 1, 0, 1, 1), Enemy("Green Slime", 1, 5, 1, 0, 1, 1)],
  [Enemy("Green Slime", 1, 5, 1, 0, 1, 1), Enemy("Green Slime", 1, 5, 1, 0, 1, 1), Enemy("Blue Slime", 2, 7, 2, 0, 2, 3)],
]
def Dungeon():
  global highestRoomBeat
  RandomiseShopItems()
  time.sleep(1)
  print("\nYou have entered the dungeon")
  room = 0
  random.shuffle(allPlayers)
  while (room < len(roomEnemies)):
    userChoice = AskQuestion(f"Whould you like to proceed to room {room + 1}? ", ["yes", "no"])
    if (userChoice == "yes"):
      print(f"\nYou are entering room {room + 1}")
      for player in allPlayers:
        player.status = "engaged"
      if Combat(allPlayers, roomEnemies[room]):
        print(f"You have defeated room {room + 1}")
        room += 1
        SaveData(allPlayers, availableWeapons)
      else:
        print(f"You have failed to defeat room {room + 1}")
        SaveData(allPlayers, availableWeapons)
        StartArea()
    else:
      StartArea()
  print(f"Congragulations, you have completed all {len(roomEnemies)} levels of the dungeon")
  StartArea()

def playerAttack(player, weaponUsing, enemyAttacking, currentRoomEnemies):
  print("Rolling the dice")
  time.sleep(1)
  if(AttackHit(player.attackModifier, enemyAttacking.ac)):
    if player.status == "engaged":
      damageDealt = sum([random.randint(1, weaponUsing.dice) for i in range(weaponUsing.number)]) + weaponUsing.baseDamage
    elif player.status == "disengaged":
      damageDealt = sum([random.randint(1, weaponUsing.retreatDice) for i in range(weaponUsing.retreatNumber)]) + weaponUsing.retreatBaseDamage
    else:
      raise Exception("Invalid player status")
    print(f"\nYour attack has hit the {enemyAttacking.name} and dealt {damageDealt} damage")
    time.sleep(0.5)
    enemyAttacking.health -= damageDealt
    if (enemyAttacking.health <= 0):
      print(f"Congradulations, you have managed to defeat the {enemyAttacking.name} and got {enemyAttacking.coinsToGiveOnDeath} coins")
      time.sleep(0.5)
      player.coins += enemyAttacking.coinsToGiveOnDeath
      player.xpIncrease(enemyAttacking.xpToGiveOnDeath)
      currentRoomEnemies.remove(enemyAttacking)
  else:
    print(f"\nThe {enemyAttacking.name} managed to dodge your attack")
  print("")
  return [currentRoomEnemies, player.coins]

def enemyAttack(enemy, playersInCombat):
  playerAttacking = random.choice(playersInCombat)
  print(f"The {enemy.name} is attacking {playerAttacking.name}")
  time.sleep(1)
  if (AttackHit(enemy.attackModifier, playerAttacking.ac)):
    print(f"The attack hit and dealt {enemy.damage} damage")
    time.sleep(0.5)
    playerAttacking.health -= enemy.damage
    if (playerAttacking.health <= 0):
      print(f"The attack has killed the weakling who calls themself {playerAttacking.name}")
      time.sleep(0.5)
      allPlayers.remove(playerAttacking)
      if len(allPlayers) == 0:
        return allPlayers
    else:
      print(f"{playerAttacking.name} now has {playerAttacking.health} health")
      time.sleep(0.5)
  else:
    print(f"The {enemy.name}'s attack missed due to a skill issue")
  return allPlayers

#implementing engage/disengage
def Combat(allPlayers, roomEnemies):
  currentRoomEnemies = roomEnemies
  for player in allPlayers:
    print("\nThe enemies in this room are ")
    enemyNames = [enemy.name for enemy in currentRoomEnemies]
    for enemyName in enemyNames:
      print(enemyName)
    enemyNames.append("disengage")
    enemyNames.append("re-engage")
    if player.status == "disengaging":
      playerStatusChoice = AskQuestion(f"Would {player.name} like to complete their retreat or re-engage? (retreat/re-engage) ", ["retreat", "re-engage"])
      if playerStatusChoice == "retreat":
        print(f"{player.name} has completed their cowardly retreat")
        player.status = "disengaged"
      elif playerStatusChoice == "re-engage":
        print(f"{player.name} has decided to not be a baby and re-engage")
        player.status = "engaged"

    if player.status == "engaged" or player.status == "disengaged":
      if player.status == "engaged":
        acceptableWeaponList = [weapon for weapon in player.weaponList if weapon.number != 0 or weapon.baseDamage != 0]
        enemyNames.remove("re-engage")
      elif player.status == "disengaged":
        acceptableWeaponList = [weapon for weapon in player.weaponList if weapon.retreatNumber != 0 or weapon.retreatBaseDamage != 0]
        enemyNames.remove("disengage")
      else:
        raise Exception("Invalid Player status")
      if len(acceptableWeaponList) != 0:
        userChoice = AskQuestion(f"Which enemy would {player.name} like to attack? You are currently {player.status}. Alternatively, choose to disengage/re-engage. ", enemyNames)
        if userChoice == "disengage":
          print(f"{player.name} has decided to try and run away.")
          player.status = "disengaging"
          continue
        if userChoice == "re-engage":
          print(f"{player.name} has decided to re-engage")
          player.status = "engaged"
          continue
        enemyAttacking = currentRoomEnemies[enemyNames.index(userChoice)]
        weaponNames = [weapon.name for weapon in player.weaponList]
        print("Your weapon choices are")
        if player.status == "engaged":
          for weapon in acceptableWeaponList:
            print(f"{weapon.name} that does {weapon.damage} damage")
        elif player.status == "disengaged":
          for weapon in acceptableWeaponList:
            print(f"{weapon.name} that does {weapon.retreatDamage} damage")
        else:
          raise Exception("Invalid Player Status")
        userChoice = AskQuestion("Which weapon would you like to use? ", [weapon.name for weapon in acceptableWeaponList])
        weaponUsing = player.weaponList[weaponNames.index(userChoice)]
        time.sleep(1)
        currentRoomEnemies, player.coins = playerAttack(player, weaponUsing, enemyAttacking, currentRoomEnemies)
        if len(currentRoomEnemies) == 0:
          return True

  playersInCombat = [player for player in allPlayers if player.status != "disengaged"]
  if len(playersInCombat) == 0:
    unluckyPlayer = random.choice(allPlayers)
    print(f"Since there are no players in combat, {unluckyPlayer.name} has decided to volunteer to be a punching bag.")
    unluckyPlayer.status = "disengaging"
    playersInCombat = [unluckyPlayer]
  for enemy in currentRoomEnemies:
    allPlayers = enemyAttack(enemy, playersInCombat)
    if len(allPlayers) == 0:
      return False
  return Combat(allPlayers, currentRoomEnemies)

def AttackHit(attackMod, ac):
  roll = random.randint(1, 20)
  if (roll == 1) or roll + attackMod < ac:
    return False
  elif (roll == 20) or roll + attackMod >= ac:
    return True
  else:
    raise Exception("Something went wrong calculating if the attack hit or not")

def AskToLoadData():
  loadData = AskQuestion("Whould you like to load your previous data? ",
                         ["yes", "no"])
  if (loadData == "yes"):
    LoadData()
    StartArea()
  else:
    loadData = AskQuestion("Are you sure? ", ["yes", "no"])
    if (loadData == "no"):
      AskToLoadData()
    else:
      CreatePlayers()

def CreatePlayers():
  global allPlayers
  numPlayers = int(
      AskQuestion("How many people are playing? ", ["1", "2", "3", "4"]))
  allPlayers = []
  for i in range(numPlayers):
    playerName = input(f"What is the name of player {i+1}? ")
    allPlayers.append(Player(playerName, 10, 0, [Weapon("Dagger", "1d4 + 0", "0d4 + 0", 1), Weapon("Training Bow", "0d4 + 0", "1d4 + 0", 3)], 0))
  SaveData(allPlayers, availableWeapons)
  StartArea()

if (os.path.isfile("./playerData.pkl")):
  AskToLoadData()
else:
  CreatePlayers()