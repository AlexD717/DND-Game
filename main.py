class Enemy:
  def __init__(self, health, ac, damage, attackModifier):
    self.health = health
    self.damage = damage
    self.attackModifier = attackModifier
    self.ac = ac

class Weapon:
  def __init__(self, name, damage):
    self.name = name
    self.damage = damage

