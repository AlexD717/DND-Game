import time
import random
import pickle
import os.path

class Enemy:
  def __init__(self, name, health, ac, damage, attackModifier, coinsToGiveOnDeath):
    self.name = name
    self.health = health
    self.damage = damage
    self.attackModifier = attackModifier
    self.ac = ac
    self.coinsToGiveOnDeath = coinsToGiveOnDeath

class Weapon:
  def __init__(self, name, damage, cost):
    self.name = name
    self.damage = damage
    self.cost = cost

class Player:
  def __init__(self, name, ac, attackModifier, weaponList, coins):
    self.name = name
    self.health = 10
    self.ac = ac
    self.attackModifier = attackModifier
    self.weaponList = weaponList
    self.coins = coins
  def __reduce__(self):
    return (self.__class__, (self.name, self.ac, self.attackModifier, self.weaponList, self.coins))

aviableWeapons = [Weapon("Dagger", 1, 1), Weapon("Short Sword", 3, 5)]

def SaveData(allPlayers, aviableWeapons):
  with open('playerData.pkl', 'wb') as file:
    pickle.dump([allPlayers, aviableWeapons], file)

def LoadData():
  global aviableWeapons
  global allPlayers
  with open('playerData.pkl', 'rb') as file:
    saveFile = pickle.load(file)
    allPlayers = saveFile[0]
    aviableWeapons = saveFile[1]
    print("You are playing a " + str(len(allPlayers)) + " player game.")
    print("The players are ")
    for player in allPlayers:
      print(player.name + " with " + str(player.coins) + " coins")
      print("The weapons " + player.name + " has are")
      for weapon in player.weaponList:
        print(weapon.name + " that does " + str(weapon.damage) + " damage")

def AskQuestion(questionText, validResults):
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
      "Whould you like to go visit the shop or enter the dungeon (shop/dungeon)? ",
      ["shop", "dungeon"])
  if (userResponse == "shop"):
    print("You are visiting the shop")
    Shop()
  else:
    Dungeon()

def BuyItem(aviableItems, player):
  itemNames = [item.name for item in aviableItems]
  userChoice = AskQuestion("What would you like to buy? ", itemNames)
  itemBuying = aviableItems[itemNames.index(userChoice)]
  if (player.coins >= itemBuying.cost):
    player.coins -= itemBuying.cost
    player.weaponList.append(itemBuying)
    print("You bought a " + itemBuying.name + " for " + str(itemBuying.cost) + " coins")
    print("You now have " + str(player.coins) + " coins")
    print(len(player.weaponList))
  else:
    print("You don't have enough coins to buy that")
  userChoice = AskQuestion("Whould you like to buy anything else? ", ["yes", "no"])
  if (userChoice == "yes"):
    BuyItem(aviableItems, player)

shopWeapons = []

def RandomiseShopItems():
  global shopWeapons
  shopWeapons = [random.choices(aviableWeapons, k=5)][0]
RandomiseShopItems()

def Shop():
  time.sleep(1)
  print("\nYou are at the shop")
  time.sleep(0.2)
  print("Here are your weapon choices")
  for weapon in shopWeapons:
    print("This weapon is a " + weapon.name + " that does " + str(weapon.damage) + " damage and costs " + str(weapon.cost) + " coins.")
  for player in allPlayers:
    userChoice = AskQuestion("Whould " + player.name + " like to buy anything? ", ["yes", "no"])
    if (userChoice == "yes"):
      BuyItem(shopWeapons, player)
  print("Come back later when the items will be refreshed")
  StartArea()

roomEnemies = [
  [Enemy("Green Slime", 1, 5, 1, 0, 1)],
  [Enemy("Green Slime", 1, 5, 1, 0, 1), Enemy("Green Slime", 1, 5, 1, 0, 1)],
  [Enemy("Green Slime", 1, 5, 1, 0, 1), Enemy("Green Slime", 1, 5, 1, 0, 1), Enemy("Blue Slime", 2, 7, 2, 0, 1)],
]
def Dungeon():
  global highestRoomBeat
  RandomiseShopItems()
  time.sleep(1)
  print("\nYou have entered the dungeon")
  room = 0
  while (room < len(roomEnemies)):
    print("\nYou are entering room " + str(room + 1))
    if (TurnCombat(allPlayers, roomEnemies[room])):
      print("You have defeated room " + str(room + 1))
      room += 1
      SaveData(allPlayers, aviableWeapons)
    else:
      print("You have failed to defeat room " + str(room + 1))
      SaveData(allPlayers, aviableWeapons)
      StartArea()

def TurnCombat(allPlayers, roomEnemies):
  for player in allPlayers:
    print("\nThe enemies in this room are ")
    enemyNames = [enemy.name for enemy in roomEnemies]
    for enemyName in enemyNames:
      print(enemyName)
    userChoice = AskQuestion("Which enemy would " + player.name + " like to attack? ", enemyNames)
    enemyAttacking = roomEnemies[enemyNames.index(userChoice)]
    weaponNames = [weapon.name for weapon in player.weaponList]
    print("Your weapon choices are")
    for weapon in player.weaponList:
      print(weapon.name + " that does " + str(weapon.damage) + " damage")
    userChoice = AskQuestion("Which weapon would you like to use? ", weaponNames)
    weaponUsing = player.weaponList[weaponNames.index(userChoice)]
    time.sleep(1)
    print("Rolling the dice")
    time.sleep(1)
    if(AttackHit(player.attackModifier, enemyAttacking.ac)):
      print("\nYour attack has hit the " + enemyAttacking.name + " and dealt " + str(weaponUsing.damage) + " damage")
      time.sleep(0.5)
      enemyAttacking.health -= weaponUsing.damage
      if (enemyAttacking.health <= 0):
        print("Congradulations, you have managed to defeat the " + enemyAttacking.name + " and got " + str(enemyAttacking.coinsToGiveOnDeath) + " coins")
        time.sleep(0.5)
        player.coins += enemyAttacking.coinsToGiveOnDeath
        roomEnemies.remove(enemyAttacking)
        if (len(roomEnemies) <= 0):
          return True
    else:
      print("\nThe " + enemyAttacking.name + " managed to dodge your attack")
  print("")
  for enemy in roomEnemies:
    playerAttacking = random.choice(allPlayers)
    print("The " + enemy.name + " is attacking " + playerAttacking.name)
    time.sleep(1)
    if (AttackHit(enemy.attackModifier, playerAttacking.ac)):
      print("The attach hit and dealt " + str(enemy.damage) + " damage")
      time.sleep(0.5)
      playerAttacking.health -= enemy.damage
      if (playerAttacking.health <= 0):
        print("The attack has killed the weakling who calls himself " + playerAttacking.name)
        time.sleep(0.5)
        allPlayers.remove(playerAttacking)
        if (len(allPlayers) <= 0):
          return False
      else:
        print(playerAttacking.name + " now has " + str(playerAttacking.health) + " health")
        time.sleep(0.5)
  return TurnCombat(allPlayers, roomEnemies)

def AttackHit(attackMod, ac):
  roll = random.randint(1, 20)
  if (roll == 1):
    return False
  elif (roll == 20):
    return True
  elif (roll + attackMod >= ac):
    return True
  else:
    return False

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
    playerName = input("What is the name of player " + str(i + 1) + "? ")
    allPlayers.append(Player(playerName, 10, 0, [Weapon("Dagger", 1, 1)], 0))
  SaveData(allPlayers, aviableWeapons)
  StartArea()

if (os.path.isfile("./playerData.pkl")):
  AskToLoadData()
else:
  CreatePlayers()