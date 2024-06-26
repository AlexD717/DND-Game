import time
import random
import pickle
import os.path
import math

highestRoomBeat = 0

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
  def __init__(self, name, damage, retreatDamage, cost, roomRequirement=0):
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
    self.type = "Weapon"
    self.roomRequirement = roomRequirement


class Potion:
  def __init__(self, name, healthMod, acMod, attackMod, shieldMod, cost, roomRequirement=0):
    self.name = name
    self.healthMod = healthMod
    self.acMod = acMod
    self.attackMod = attackMod
    self.shieldMod = shieldMod
    self.cost = cost
    self.type = "Potion"
    self.roomRequirement = roomRequirement

class Armor:
  def __init__(self, name, acMod, shieldMod, cost, roomRequirement=0):
    self.name = name
    self.type = "Armor"
    self.acMod = acMod
    self.shieldMod = shieldMod
    self.cost = cost
    self.roomRequirement = roomRequirement

class Player:
  def __init__(self, name, playerClass, maxHealth, ac, attackModifier, weaponList, coins):
    self.name = name
    self.playerClass = playerClass
    self.playerClass.setPlayer(self)
    self.maxHealth = maxHealth
    self.health = maxHealth
    self.ac = ac
    self.acTemp = ac
    self.attackModifier = attackModifier
    self.attackModifierTemp = attackModifier
    self.weaponList = weaponList
    self.coins = coins
    self.status = "Not in combat"
    self.potionList = []
    self.armorList = []
    self.armorEquipped = None
    self.shield = 0
    self.shieldTemp = 0
  def __reduce__(self):
    return (self.__class__, (self.name, self.playerClass, self.maxHealth, self.ac, self.attackModifier, self.weaponList, self.coins))

class PlayerClass:
  def __init__(self, className, xp=0):
    self.name = className
    self.xp = xp
    self.level = self.setPlayerLevel()
    self.player = None
  def setPlayer(self, player: Player):
    self.player = player
  def setPlayerLevel(self):
    return math.floor(math.sqrt(self.xp))
  def xpIncrease(self, increase):
    self.xp += increase
    previousLevel = self.level
    self.level = self.setPlayerLevel()
    if (previousLevel < self.level):
      self.playerLeveledUp()
  def bonusAttackModifier(self, weapon: Weapon):
    return 0
  def playerLeveledUp(self):
    print(f"Congradulations {self.player.name}, you have leveled up! You are now level {self.level}.")
    time.sleep(1)


class Fighter(PlayerClass):
  def __init__(self, className, xp=0):
    super().__init__(className, xp)
  def bonusAttackModifier(self, weapon: Weapon):
    return math.ceil(self.level / 2)
  def xpIncrease(self, increase):
    super().xpIncrease(increase)
  def playerLeveledUp(self):
    super().playerLeveledUp()
    if (self.level % 2 == 0):
      self.player.maxHealth += 1


class Paladin(PlayerClass):
  def __init__(self, className, xp=0):
    super().__init__(className, xp)
  def bonusAttackModifier(self, weapon: Weapon):
    return math.floor(self.level / 5)
  def xpIncrease(self, increase):
    super().xpIncrease(increase)
  def playerLeveledUp(self):
    super().playerLeveledUp()
    self.player.maxHealth += 1
    if (self.level % 3 == 0):  # TODO check if this is working
      self.player.ac += 1

class Ranger(PlayerClass):
  def __init__(self, className, xp=0):
    super().__init__(className, xp)
  def bonusAttackModifier(self, weapon: Weapon):
    if (weapon.retreatNumber > 0):
      print(f"Adding bonus of {self.level}")
      return self.level
    else:
      return 0


availableGoods = [
    Weapon("Dagger", "1d4 + 0", "0d4 + 0", 1),
    Weapon("Short Sword", "3d4 + 1", "0d4 + 0", 5),
    Weapon("Two Short Swords", "4d6 + 2", "0d4 + 0", 10),
    Weapon("Long Sword", "4d8 + 4", "0d4 + 0", 18),
    Weapon("Battle Axe", "2d20 + 0", "0d4 + 0", 18),
    Weapon("Spear", "4d10 + 2", "2d6 + 0", 25),
    Weapon("Pike", "4d12 + 4", "2d8 + 2", 35),
    Weapon("Mace", "5d10 + 8", "0d4 + 0", 40),
    Weapon("Morning Star", "8d6 + 10", "0d4 + 0", 45),
    Weapon("Great Sword", "8d8 + 10", "0d4 + 0", 50),
    Weapon("Light Javelin", "3d4 + 0", "1d8 + 1", 15),
    Weapon("Heavy Javelin", "3d8 + 0", "1d12 + 4", 25),
    Weapon("Training Bow", "0d4 + 0", "1d4 + 0", 3),
    Weapon("Light Bow", "0d4 + 0", "1d8 + 0", 10),
    Weapon("Hunting Bow", "0d4 + 1", "2d6 + 2", 15),
    Weapon("Long Bow", "0d4 + 2", "2d8 + 2", 20),
    Weapon("Heavy Bow", "0d4 + 4", "2d12 + 4", 30),
    Weapon("War Bow", "1d4 + 1", "4d8 + 6", 40),
    Weapon("Crossbow", "1d6 + 0", "5d4 + 8", 40),
    Weapon("Heavy War Bow", "2d4 + 0", "8d6 + 6", 50),
    Weapon("Heavy Crossbow", "3d4 + 2", "8d4 + 8", 50),
    Potion("Minor Health Potion", 1, 0, 0, 0, 1),
    Potion("Small Health Potion", 3, 0, 0, 0, 2),
    Potion("Medium Health Potion", 5, 0, 0, 0, 5),
    Potion("Large Health Potion", 10, 1, 0, 1, 10),
    Potion("Huge Health Potion", 15, 5, 0, 3, 15),
    Potion("Shield Potion", 0, 0, 0, 1, 5),
    Potion("Large Shield Potion", 0, 1, 0, 3, 15),
    Armor("Old Leather Armor", 1, 0, 2),
    Armor("Boiled Leather Armor", 4, 1, 5),
    Armor("Chainmail Armor", 8, 4, 15),
    Armor("Heavy Mail", 10, 8, 25),
    Armor("Light Plate Armor", 12, 10, 32),
    Armor("Plate Armor", 15, 12, 40),
    Armor("Heavy Plate Armor", 18, 10, 50, 3)
]


def SaveData(allPlayers, highestRoomBeat):
  with open('playerData.pkl', 'wb') as file:
    pickle.dump([allPlayers, highestRoomBeat], file)


def LoadData():
  global allPlayers
  global highestRoomBeat
  with open('playerData.pkl', 'rb') as file:
    saveFile = pickle.load(file)
    allPlayers = saveFile[0]
    highestRoomBeat = int(saveFile[1])
    print(f"You are playing a {len(allPlayers)} player game.")
    print("The players are ")
    for player in allPlayers:
      player.playerClass.setPlayerLevel()
      print(f"{player.name} who is a {player.playerClass.name} on level {player.playerClass.level} with {player.coins} coins")
      print(f"They have {player.health} health and {player.ac} ac")
      print(f"The weapons {player.name} has are")
      for weapon in player.weaponList:
        if (weapon.number > 0):
          print(f"{weapon.name} that does {weapon.number}d{weapon.dice} + {weapon.baseDamage} damage")
        if (weapon.retreatNumber > 0):
          print(f"{weapon.name} that does {weapon.retreatNumber}d{weapon.retreatDice} + {weapon.retreatBaseDamage} damage")
    print(f"Your highest room beat is {highestRoomBeat}")
  RandomiseShopItems()


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
  for player in allPlayers:
    player.health = player.maxHealth
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
    SaveData(allPlayers, highestRoomBeat)
    exit()


def BuyItem(availableItems, player):
  itemNames = [item.name for item in availableItems]
  userChoice = AskQuestion("What would you like to buy? ", itemNames)
  itemBuying = availableItems[itemNames.index(userChoice)]
  if (player.coins >= itemBuying.cost):
    player.coins -= itemBuying.cost
    print(f"You bought a {itemBuying.name} for {itemBuying.cost} coins")
    print(f"You now have {player.coins} coins")
    if itemBuying.type == "Weapon":
      player.weaponList.append(itemBuying)
    if itemBuying.type == "Potion":
      player.potionList.append(itemBuying)
    if itemBuying.type == "Armor":
      player.armorList.append(itemBuying)
      userChoice = AskQuestion("Would you like to equip this armor? ", ["yes", "no"])
      if userChoice == "yes":
        player.armorEquipped = itemBuying
        player.ac = itemBuying.acMod
        player.shield = itemBuying.shieldMod
        print(f"You have equipped {itemBuying.name}")
        print(f"Your AC is now {player.ac}")
  else:
    print("You don't have enough coins to buy that")
  userChoice = AskQuestion("Whould you like to buy anything else? ", ["yes", "no"])
  if (userChoice == "yes"):
    BuyItem(availableItems, player)


shopItems = []
def RandomiseShopItems():
  global shopItems
  goodsPlayerCanGet = []
  for good in availableGoods:
    if (good.roomRequirement <= highestRoomBeat):
      goodsPlayerCanGet.append(good)
  shopItems = [random.choices(goodsPlayerCanGet, k=5)][0]
RandomiseShopItems()


def Shop():
  time.sleep(1)
  print("\nYou are at the shop")
  time.sleep(0.2)
  print("Here are your item choices")
  for item in shopItems:
    if item.type == "Weapon":
      print(f"This weapon is a {item.name} that does {item.damage} damage on the frontline, {item.retreatDamage} on the backline, and costs {item.cost} coins.")
    elif item.type == "Potion":
      print(f"This {item.name} is a potion that restores {item.healthMod} health, increases your ac by {item.acMod}, increases your attack by {item.attackMod}, increases your shield by {item.shieldMod} and costs {item.cost}")
    elif item.type == "Armor":
      print(f"This {item.name} is a piece of armor that increases your ac by {item.acMod}, and increases your shield by {item.shieldMod}, costing {item.cost} coins")
  for player in allPlayers:
    #remove this
    player.coins = 10000
    print(f"You have {player.coins} coins")
    userChoice = AskQuestion(f"Whould {player.name} like to buy anything? ", ["yes", "no"])
    if (userChoice == "yes"):
      BuyItem(shopItems, player)
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
      print(f"{weapon.name} is a weapon that does {weapon.damage} damage and can be sold for {math.floor(weapon.cost)}")
      userChoices.append(weapon.name)
    userChoices.append("cancel")
    userChoice = AskQuestion(
        "What would you like to sell or would you like to cancel the transaction? ",
        userChoices)
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
        SaveData(allPlayers, highestRoomBeat)
  else:
    print("You cannot sell your last weapon")
    SaveData(allPlayers, highestRoomBeat)


def Dungeon():
  global highestRoomBeat
  roomEnemies = [[Enemy("Green Slime", 1, 5, 1, 0, 1, 1)],
                 [
                     Enemy("Green Slime", 1, 5, 1, 0, 1, 1),
                     Enemy("Green Slime", 1, 5, 1, 0, 1, 1)
                 ],
                 [
                     Enemy("Green Slime", 1, 5, 1, 0, 1, 1),
                     Enemy("Green Slime", 1, 5, 1, 0, 1, 1),
                     Enemy("Blue Slime", 2, 7, 2, 0, 2, 3)
                 ], [Enemy("Skeleton", 5, 5, 5, 2, 5, 3)]]
  RandomiseShopItems()
  time.sleep(1)
  print("\nYou have entered the dungeon")
  room = 0
  random.shuffle(allPlayers)
  for player in allPlayers:
    player.status = "engaged"
    player.healthTemp = player.health
    player.acTemp = player.ac
    player.shieldTemp = player.shield
    player.attackModifierTemp = player.attackModifier
  while (room < len(roomEnemies)):
    userChoice = AskQuestion(
        f"Whould you like to proceed to room {room + 1}? ", ["yes", "no"])
    if (userChoice == "yes"):
      print(f"\nYou are entering room {room+1}")
      print()
      if Combat(allPlayers, roomEnemies[room]):
        print(f"You have defeated room {room+1}")
        room += 1
        if (room > highestRoomBeat):
          highestRoomBeat = room
        SaveData(allPlayers, highestRoomBeat)
      else:
        print(f"You have failed to defeat room {room+1}")
        SaveData(allPlayers, highestRoomBeat)
        StartArea()
    else:
      StartArea()
  print(f"Congragulations, you have completed all {len(roomEnemies)} levels of the dungeon")
  StartArea()


def playerAttack(player, weaponUsing, enemyAttacking, currentRoomEnemies):
  print("Rolling the dice")
  time.sleep(1)
  if (AttackHit(
      player.attackModifierTemp +
      player.playerClass.bonusAttackModifier(weaponUsing), enemyAttacking.ac)):
    if player.status == "engaged":
      damageDealt = sum([
          random.randint(1, weaponUsing.dice)
          for i in range(weaponUsing.number)
      ]) + weaponUsing.baseDamage
    elif player.status == "disengaged":
      damageDealt = sum([
          random.randint(1, weaponUsing.retreatDice)
          for i in range(weaponUsing.retreatNumber)
      ]) + weaponUsing.retreatBaseDamage
    else:
      raise Exception("Invalid player status")
    print(
        f"\nYour attack has hit the {enemyAttacking.name} and dealt {damageDealt} damage"
    )
    time.sleep(0.5)
    enemyAttacking.health -= damageDealt
    if (enemyAttacking.health <= 0):
      print(
          f"Congradulations, you have managed to defeat the {enemyAttacking.name} and got {enemyAttacking.coinsToGiveOnDeath} coins"
      )
      time.sleep(0.5)
      player.coins += enemyAttacking.coinsToGiveOnDeath
      player.playerClass.xpIncrease(enemyAttacking.xpToGiveOnDeath)
      currentRoomEnemies.remove(enemyAttacking)
  else:
    print(f"\nThe {enemyAttacking.name} managed to dodge your attack")
  print("")
  return [currentRoomEnemies, player.coins]


def enemyAttack(enemy, playersInCombat):
  playerAttacking = random.choice(playersInCombat)
  print(f"The {enemy.name} is attacking {playerAttacking.name}")
  time.sleep(1)
  if (AttackHit(enemy.attackModifier, playerAttacking.acTemp)):
    print(f"The attack hit and dealt {enemy.damage} damage")
    time.sleep(0.5)
    playerAttacking.healthTemp -= enemy.damage - playerAttacking.shieldTemp
    if (playerAttacking.healthTemp <= 0):
      print(
          f"The attack has killed the weakling who calls themself {playerAttacking.name}"
      )
      time.sleep(0.5)
      allPlayers.remove(playerAttacking)
      if len(allPlayers) == 0:
        return allPlayers
    else:
      print(f"{playerAttacking.name} now has {playerAttacking.healthTemp} health")
      time.sleep(0.5)
  else:
    print(f"The {enemy.name}'s attack missed due to a skill issue")
  return allPlayers


def usePotion(player):
  print("The potions you have avaliable are:")
  potionNames = [potion.name for potion in player.potionList]
  for potion in potionNames:
    print(potion)
  userChoice = AskQuestion("Which potions would you like to use? ", potionNames)
  potionUsing = player.potionList[potionNames.index(userChoice)]
  player.healthTemp += potionUsing.healthMod
  player.acTemp += potionUsing.acMod
  player.attackModifierTemp += potionUsing.attackMod
  player.potionList.remove(potionUsing)
  print(f"You have used {potionUsing.name}.")
  print(
      f"You now have {player.healthTemp} health, your ac is now {player.acTemp} ac,, your shield is now {player.shieldTemp} and your attack modifier is now {player.attackModifierTemp}."
  )
  return [
      player.healthTemp, player.acTemp, player.attackModifierTemp,
      player.shieldTemp, player.potionList
  ]


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
      playerStatusChoice = AskQuestion(
          f"Would {player.name} like to complete their retreat or re-engage? (retreat/re-engage) ",
          ["retreat", "re-engage"])
      if playerStatusChoice == "retreat":
        print(f"{player.name} has completed their cowardly retreat")
        player.status = "disengaged"
      elif playerStatusChoice == "re-engage":
        print(f"{player.name} has decided to not be a baby and re-engage")
        player.status = "engaged"

    if player.status == "engaged" or player.status == "disengaged":
      if player.status == "engaged":
        acceptableWeaponList = [
            weapon for weapon in player.weaponList
            if weapon.number != 0 or weapon.baseDamage != 0
        ]
        enemyNames.remove("re-engage")
      elif player.status == "disengaged":
        acceptableWeaponList = [
            weapon for weapon in player.weaponList
            if weapon.retreatNumber != 0 or weapon.retreatBaseDamage != 0
        ]
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
          print(f"{player.name} has regained some courage and has decided to re-engage")
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
        currentRoomEnemies, player.coins = playerAttack(
            player, weaponUsing, enemyAttacking, currentRoomEnemies)
        if len(currentRoomEnemies) == 0:
          return True
      else:
        userChoice = AskQuestion(
            "You have no weapons that can be used currently. Would you like to disengage/re-engage? ", ["disengage", "re-engage", "no"])
        if userChoice == "disengage":
          print(f"{player.name} has decided to try and run away")
          player.status = "disengaging"
        elif userChoice == "re-engage":
          print(f"{player.name} has regained some courage and has decided to re-engage")
          player.status = "engaged"
      if player.status == "disengaged" and len(player.potionList) > 0:
        userChoice = AskQuestion("Would you like to use a potion? ", ["yes", "no"])
        if userChoice == "yes":
          player.healthTemp, player.acTemp, player.attackModifierTemp, player.shieldTemp, player.potionList = usePotion(player)
  playersInCombat = [
      player for player in allPlayers if player.status != "disengaged"
  ]
  if len(playersInCombat) == 0:
    unluckyPlayer = random.choice(allPlayers)
    print(
        f"Since there are no players in combat, {unluckyPlayer.name} has decided to volunteer to be a punching bag."
    )
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
  loadData = AskQuestion("Whould you like to load your previous data? ", ["yes", "no"])
  if (loadData == "yes"):
    LoadData()
    StartArea()
  else:
    loadData = AskQuestion("Are you sure? ", ["yes", "no"])
    if (loadData == "no"):
      AskToLoadData()
    else:
      CreatePlayers()


aviableClassNames = ["Fighter", "Ranger", "Paladin"]

def CreatePlayers():
  global allPlayers
  numPlayers = int(AskQuestion("How many people are playing? ", ["1", "2", "3", "4"]))
  allPlayers = []
  for i in range(numPlayers):
    playerName = input(f"What is the name of player {i+1}? ")
    playerClassName = AskQuestion(
        f"What will be the class of the player? Your options are {aviableClassNames} ",
        aviableClassNames)
    playerClass = None
    if (playerClassName == "Fighter"):
      playerClass = Fighter("Fighter")
    elif (playerClassName == "Ranger"):
      playerClass = Ranger("Ranger")
    elif (playerClassName == "Paladin"):
      playerClass = Paladin("Paladin")
    playerAdded = Player(playerName, playerClass, 10, 10, 0, [
        Weapon("Dagger", "1d4 + 0", "0d4 + 0", 1),
        Weapon("Training Bow", "0d4 + 0", "1d4 + 0", 3)
    ], 0)
    allPlayers.append(playerAdded)
  SaveData(allPlayers, highestRoomBeat)
  StartArea()
  RandomiseShopItems()

if (os.path.isfile("./playerData.pkl")):
  AskToLoadData()
else:
  CreatePlayers()