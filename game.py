import pyxel
from bug import Bug
from food import Food
import random
import math

pyxel.init(255, 255)
food = [Food(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(20)]
bugs = [Bug(random.uniform(10, 246), random.uniform(10, 246)) for _ in range(40)]
show_labels = False

def update():
  global show_labels
  if pyxel.btnp(pyxel.KEY_Q):
    pyxel.quit()

  if pyxel.btnp(pyxel.KEY_T):
    show_labels = not show_labels

  for bug in bugs:
    bug.update(food, bugs)

  for bit in food:
    bit.update()

  for bit in list(food):
    if bit.eaten:
      food.remove(bit)

  if pyxel.frame_count % 4 == 0:
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

    food.append(Food(x, y, random.randint(0, 100) < 10))

  for bug in list(bugs):
    if bug.dead:
      bugs.remove(bug)
      if len(bugs) < 25:
        bugs.append(Bug(random.uniform(10, 246), random.uniform(10, 246)))

def draw():
  global show_labels
  pyxel.cls(0)

  for drawable in food + bugs:
    drawable.draw(show_labels)

  pyxel.text(10, 10, "TOTAL BUGS: "+str(len(bugs)), 10)


pyxel.run(update, draw)