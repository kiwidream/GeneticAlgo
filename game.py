import pyxel
from bug import Bug
from food import Food
import random
import math

pyxel.init(255, 255)
food = [Food(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(15)]
bugs = [Bug(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(30)]

def update():
  if pyxel.btnp(pyxel.KEY_Q):
    pyxel.quit()

  for bug in bugs:
    bug.update(food, bugs)

  for bit in list(food):
    if bit.eaten:
      food.remove(bit)

      empty_spot = False
      while empty_spot == False:

        x = random.uniform(10, 246)
        y = random.uniform(10, 246)
        empty_spot = True

        for bug in bugs:
          dist = math.sqrt((x-bug.x) ** 2 + (y-bug.y) ** 2)

          if dist < 30:
            empty_spot = False
            break

      food.append(Food(x, y))

  for bug in list(bugs):
    if bug.dead:
      bugs.remove(bug)
      if len(bugs) < 15:
        bugs.append(Bug(random.uniform(10, 246), random.uniform(10, 246)))

def draw():
  pyxel.cls(0)

  for drawable in food + bugs:
    drawable.draw()


pyxel.run(update, draw)