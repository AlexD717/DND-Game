import time
import random

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
  def __init__(self, name, attackModifier):
    self.name = name
    self.attackModifier = attackModifier
    self.weaponList = [Weapon("Damaged Short Sword", 1, 1)]

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
    AskQuestion(questionText, validResults)

def StartArea():
  time.sleep(1)
  print("\nYou are at the front of the dungeon")
  time.sleep(0.5)
  userResponse = AskQuestion("Whould you like to go visit the shop or enter the dungeon (shop/dungeon)? ", ["shop", "dungeon"])
  if (userResponse == "shop"):
    print("You are visiting the shop")
    Shop()
  else:
    Dungeon()

aviableWeapons = [Weapon("Short Sword", 3, 5), Weapon("Shinning Short Sword", 5, 7)]

def BuyItem(aviableItems, player):
  userChoice = AskQuestion("What would you like to buy? ")

def Shop():
  time.sleep(1)
  print("You are at the shop")
  time.sleep(0.2)
  print("Here are your weapon choices")
  shopWeapons = [random.choices(aviableWeapons, k=5)][0]
  print(shopWeapons)
  for weapon in shopWeapons:
    print("This weapon is a " + weapon.name + " that does " + str(weapon.damage) + " damage and costs " + str(weapon.cost) + " coins.")
  for player in allPlayers:
    userChoice = AskQuestion("Whould " + player.name + "like to buy anything? ", "yes", "no")
    if (userChoice == "yes"):
      BuyItem(shopWeapons, player)
  print("Come back later when the items will be refreshed")
  StartArea()

def Dungeon():
  time.sleep(1)
  print("You have entered the dungeon")

numPlayers = int(AskQuestion("How many people are playing? ", ["1", "2", "3", "4"]))
allPlayers = []
for i in range(numPlayers):
  playerName = input("What is the name of player " + str(i + 1) + "? ")
  allPlayers.append(Player(playerName, 0))
StartArea()