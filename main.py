import time
import random
import pickle
import os.path


class Enemy:

  def __init__(self, health, ac, damage, attackModifier):
    self.health = health
    self.damage = damage
    self.attackModifier = attackModifier
    self.ac = ac


class Weapon:

  def __init__(self, name, damage, cost):
    self.name = name
    self.damage = damage
    self.cost = cost


class Player:

  def __init__(self, name, attackModifier, weaponList, money):
    self.name = name
    self.attackModifier = attackModifier
    self.weaponList = weaponList
    self.money = money

  def __reduce__(self):
    return (self.__class__, (self.name, self.attackModifier, self.weaponList,
                             self.money))


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
      print(player.name + " with " + str(player.money) + " coins")
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
  if (player.money >= itemBuying.cost):
    player.money -= itemBuying.cost
    player.weaponList.append(itemBuying)
    print("You bought a " + itemBuying.name + " for " + str(itemBuying.cost) +
          " coins")
    print("You now have " + str(player.money) + " coins")
    print(len(player.weaponList))
  else:
    print("You don't have enough money to buy that")
  userChoice = AskQuestion("Whould you like to buy anything else? ",
                           ["yes", "no"])
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
    print("This weapon is a " + weapon.name + " that does " +
          str(weapon.damage) + " damage and costs " + str(weapon.cost) +
          " coins.")
  for player in allPlayers:
    userChoice = AskQuestion(
        "Whould " + player.name + " like to buy anything? ", ["yes", "no"])
    if (userChoice == "yes"):
      BuyItem(shopWeapons, player)
  print("Come back later when the items will be refreshed")
  StartArea()


'''
roomEnemies = [[], []]
highestRoomBeat = 0
def Dungeon():
  global highestRoomBeat
  time.sleep(1)
  print("\nYou have entered the dungeon")
  room = 0
  while (room < len(roomEnemies)):
    TurnCombat(allPlayers, roomEnemies[room])
    room += 1
    if (room > highestRoomBeat):
      highestRoomBeat

def TurnCombat(allPlayers, roomEnemies):
  print("The enmies in this room are " + " ,".joing(roomEnemies))
  targetEnemy = AskQuestion("Which Enemy would you like to attack? ", )
'''


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
    allPlayers.append(Player(playerName, 0, [Weapon("Dagger", 1, 1)], 0))
  SaveData(allPlayers, aviableWeapons)
  StartArea()


if (os.path.isfile("./playerData.pkl")):
  AskToLoadData()
else:
  CreatePlayers()
