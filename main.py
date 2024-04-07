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
#Adding dice rolls to weapon damage
class Weapon:
  def __init__(self, name, baseDamage, numberDice, dice, cost):
    self.name = name
    self.baseDamage = baseDamage
    self.number = numberDice
    self.dice = dice
    self.cost = cost
    self.damage = str(numberDice) + "d" + str(dice) + " + " + str(baseDamage)

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

availableWeapons = [Weapon("Dagger", 0, 1, 4, 1), Weapon("Short Sword", 1, 3, 4, 5)]

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
      print(f"{player.name} with {player.coins} coins")
      print("The weapons {player.name} has are")
      for weapon in player.weaponList:
        print(f"{weapon.name} that does {weapon.damage} damage")

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
  elif userResponse == "dungeon":
    Dungeon()

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
  #randomising order
  random.shuffle(allPlayers)
  while (room < len(roomEnemies)):
    print(f"\nYou are entering room {room+1}")
    if (TurnCombat(allPlayers, roomEnemies[room])):
      print(f"You have defeated room {room+1}")
      room += 1
      SaveData(allPlayers, availableWeapons)
    else:
      print(f"You have failed to defeat room {room+1}")
      SaveData(allPlayers, availableWeapons)
      StartArea()
  print(f"Congragulations, you have completed all {len(roomEnemies)} levels of the dungeon")
  StartArea()

def TurnCombat(allPlayers, roomEnemies):
  currentRoomEnemies = roomEnemies
  for player in allPlayers:
    print("\nThe enemies in this room are ")
    enemyNames = [enemy.name for enemy in currentRoomEnemies]
    for enemyName in enemyNames:
      print(enemyName)
    userChoice = AskQuestion(f"Which enemy would {player.name} like to attack? ", enemyNames)
    enemyAttacking = currentRoomEnemies[enemyNames.index(userChoice)]
    weaponNames = [weapon.name for weapon in player.weaponList]
    print("Your weapon choices are")
    for weapon in player.weaponList:
      print(f"{weapon.name} that does {weapon.damage} damage")
    userChoice = AskQuestion("Which weapon would you like to use? ", weaponNames)
    weaponUsing = player.weaponList[weaponNames.index(userChoice)]
    time.sleep(1)
    print("Rolling the dice")
    time.sleep(1)
    if(AttackHit(player.attackModifier, enemyAttacking.ac)):
      damageDealt = sum([random.randint(1, weaponUsing.dice) for i in range(weaponUsing.number)]) + weaponUsing.baseDamage
      print(f"\nYour attack has hit the {enemyAttacking.name} and dealt {damageDealt} damage")
      time.sleep(0.5)
      enemyAttacking.health -= damageDealt
      if (enemyAttacking.health <= 0):
        print(f"Congradulations, you have managed to defeat the {enemyAttacking.name} and got {enemyAttacking.coinsToGiveOnDeath} coins")
        time.sleep(0.5)
        player.coins += enemyAttacking.coinsToGiveOnDeath
        currentRoomEnemies.remove(enemyAttacking)
        if (len(currentRoomEnemies) <= 0):
          return True
    else:
      print(f"\nThe {enemyAttacking.name} managed to dodge your attack")
  print("")
  
  for enemy in currentRoomEnemies:
    playerAttacking = random.choice(allPlayers)
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
        if (len(allPlayers) <= 0):
          return False
      else:
        print(f"{playerAttacking.name} now has {playerAttacking.health} health")
        time.sleep(0.5)
    else:
      print(f"The {enemy.name}'s attack missed due to a skill issue")
  return TurnCombat(allPlayers, currentRoomEnemies)

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
    allPlayers.append(Player(playerName, 10, 0, [Weapon("Dagger",0, 1, 4, 1)], 0))
  SaveData(allPlayers, availableWeapons)
  StartArea()

if (os.path.isfile("./playerData.pkl")):
  AskToLoadData()
else:
  CreatePlayers()