import pyxel
from bug import Bug
from food import Food
import random
import math

pyxel.init(256, 256)
food = [Food(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(15)]
bugs = [Bug(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(40)]

def update():
  if pyxel.btnp(pyxel.KEY_Q):
    pyxel.quit()

  for bug in bugs:
    bug.update(food, bugs)

  for bit in list(food):
    if bit.eaten:
      food.remove(bit)
      food.append(Food(random.uniform(10, 246), random.uniform(10, 246)))

  for bug in list(bugs):
    if bug.dead:
      bugs.remove(bug)
      if len(bugs) < 5:
        bugs.append(Bug(random.uniform(10, 246), random.uniform(10, 246)))

def draw():
  pyxel.cls(0)

  for drawable in food + bugs:
    drawable.draw()


pyxel.run(update, draw)