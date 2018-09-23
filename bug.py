from network import Network
import pyxel
from pyxel import constants
import math
import numpy as np
from drawable import Drawable
import sys
import random

class Bug(Drawable):

  COLOURS = [
    7, 8, 9, 10, 11, 12, 13, 14, 15
  ]

  NUM_EYES = 3
  EYE_DIST = 0
  EYE_SEEN = 1

  #outputs
  ROT_CTRL = 0
  FORWARD = 1

  def __init__(self, x, y):
    super().__init__(x, y, 1)
    self.vx = 0
    self.vy = 0
    self.v = 0
    self.rot = 0
    self.hunger = 0
    self.input_size = 2 + self.NUM_EYES * 2
    sizes = [self.input_size, 10, 10, 6]
    self.network = Network(sizes)
    self.a = 0
    self.colour = 0
    self.dead = False
    self.eyesight = 75
    self.reset_eyes()
    self.eye_angle = 0.2
    self.repr_timer = 0
    self.repr_anim = 0
    self.repr_str = 0
    self.colour_str = 0
    self.food_count = 0
    self.species = random.randint(1, 999)
    self.heart_anim = False
    self.gen = 0
    self.age = 0
    self.propagate()

  def draw(self, show_labels, eye_debug):
    pyxel.circ(self.x, self.y, self.radius, self.colour)

    # Debug visualiser for eyesight
    if eye_debug:
      for eye in range(self.NUM_EYES*2):
        eye_rel = self.NUM_EYES // 2 - eye // 2
        if self.NUM_EYES % 2 == 0:
          eye_rel -= 0.5
        eye_offset = eye_rel * self.eye_angle * 2
        if eye % 2 == 0:
          continue

        dist = self.eyesight - self.eyes[eye][self.EYE_DIST]
        pyxel.line(self.x, self.y, self.x+math.cos(eye_offset+self.rot+self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(eye_offset+self.rot+self.eye_angle)*min(self.eyesight, dist), 5)
        pyxel.line(self.x, self.y, self.x+math.cos(eye_offset+self.rot-self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(eye_offset+self.rot-self.eye_angle)*min(self.eyesight, dist), 5)



    pyxel.line(self.x+math.cos(self.rot)*2, self.y+math.sin(self.rot)*2, self.x+math.cos(self.rot+math.pi*3/4)*3, self.y+math.sin(self.rot+math.pi*3/4)*3, self.colour)
    pyxel.line(self.x+math.cos(self.rot)*2, self.y+math.sin(self.rot)*2, self.x+math.cos(self.rot-math.pi*3/4)*3, self.y+math.sin(self.rot-math.pi*3/4)*3, self.colour)

    if self.repr_anim > 0:
      pyxel.text(self.x, self.y - 10, "+", 15)

    if show_labels:
      pyxel.text(self.x - 10, self.y + 10, str(self.species)+'-'+str(self.gen), 15)

      if self.heart_anim:
        pyxel.text(self.x + 10, self.y - 10, "<3", 15)
      else:
        pyxel.text(self.x + 10, self.y - 10, str(math.floor(self.hunger)), 15)


  def reset_eyes(self):
    self.eyes = [(0,) for _ in range(self.NUM_EYES*2)]

  def update(self, food, bugs):

    self.reset_eyes()

    for eye in range(self.NUM_EYES*2):
      eye_rel = self.NUM_EYES // 2 - eye // 2
      if self.NUM_EYES % 2 == 0:
        eye_rel -= 0.5
      eye_offset = eye_rel * self.eye_angle * 2
      min_dist = self.eyesight
      for drawable in food:
        if eye % 2 == int(drawable.deadly):
          continue
        cx = drawable.x - self.x
        cy = drawable.y - self.y
        dist = math.sqrt(cx**2+cy**2)
        if dist < min_dist:
          ca = math.atan2(cy, cx)

          if ca - self.rot > math.pi/2:
            continue

          lx = math.cos(eye_offset+self.rot+self.eye_angle)*self.eyesight
          ly = math.sin(eye_offset+self.rot+self.eye_angle)*self.eyesight
          rx = math.cos(eye_offset+self.rot-self.eye_angle)*self.eyesight
          ry = math.sin(eye_offset+self.rot-self.eye_angle)*self.eyesight
          la = math.atan2(ly, lx)
          ra = math.atan2(ry, rx)
          dr = abs(ra - ca)
          dl = abs(la - ca)
          if (dr < self.eye_angle * 2 and dl < self.eye_angle * 2):
            min_dist = dist
            self.eyes[eye] = (self.eyesight - min_dist, )

    self.colour_str = 0
    for bug in bugs:
      if bug != self and bug.colour == self.colour:
        dist = math.sqrt((bug.x-self.x) ** 2 + (bug.y-self.y) ** 2)
        if dist < self.eyesight:
          self.colour_str += 2 * (1 - dist / self.eyesight)

    if self.age > 30:
      self.dead = True

    for bit in food:
      if not bit.eaten and math.sqrt((bit.x - self.x) ** 2 + (bit.y - self.y) ** 2) < 6:

        if bit.deadly:
          self.dead = True
          return

        bit.eaten = True
        self.food_count += 1
        self.hunger = 0

    self.propagate()
    rotv = max(min(self.activations[self.ROT_CTRL][0], 1), 0) - 0.5
    self.rot += rotv
    self.a = (max(min(self.activations[self.FORWARD][0], 1), 0) - 0.5) * 0.25
    self.v += self.a
    self.v *= 0.97
    self.hunger += abs(self.a) / 2 + abs(rotv) * 2

    self.vx = math.cos(self.rot) * self.v
    self.vy = math.sin(self.rot) * self.v

    self.x = (self.x + self.vx) % 256
    self.y = (self.y + self.vy) % 256

    self.repr_timer += 1

    if self.repr_anim > 0:
      self.repr_anim -= 1

    self.heart_anim = False
    if self.food_count > 3:
      self.heart_anim = True

    if self.food_count > 3 and len(bugs) < 40:
      new_bug = Bug(self.x, self.y)

      new_bug.network.weights = np.copy(self.network.weights)
      new_bug.network.biases = np.copy(self.network.biases)
      new_bug.mutate()

      new_bug.species = self.species
      new_bug.gen = self.gen + 1
      new_bug.repr_anim = 100
      new_bug.rot = self.rot

      bugs.append(new_bug)

      self.food_count -= 4
      self.age += 1

    c_act = [self.activations[i] for i in range(2, 6)]
    c_index = c_act.index(max(c_act))
    self.colour = self.COLOURS[c_index]
    self.hunger += 0.1
    if self.hunger >= 300:
      self.dead = True

  def merge_network(self, other_weights, other_biases):
    b1 = random.uniform(0.01, 0.04)
    for i in range(len(other_weights)):
      for j in range(len(other_weights[i])):
        if random.uniform(0, 1) < 0.5:
          b1 = 2 - b1
        b2 = 2 - b1
        self.network.weights[i][j] = (other_weights[i][j]*b1 + self.network.weights[i][j]*b2) / 2
        self.network.biases[i][j] = (other_biases[i][j]*b1 + self.network.biases[i][j]*b2) / 2

  def mutate(self):
    for i in range(len(self.network.weights)):
      for j in range(len(self.network.weights[i])):
        self.network.weights[i][j] *= random.uniform(0.98, 1.02)
        self.network.biases[i][j] *= random.uniform(0.98, 1.02)

  def line_intersect(self, ax, ay, bx, by, cx, cy, r):
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    a = ax**2 + ay**2 - r**2
    b = 2*(ax*(bx - ax) + ay*(by - ay))
    c = (bx - ax)**2 + (by - ay)**2
    disc = b**2 - 4*a*c

    if disc <= 0:
      return False

    sqrtdisc = math.sqrt(disc)
    t1 = (-b + sqrtdisc)/(2*a)
    t2 = (-b - sqrtdisc)/(2*a)
    return ((0 < t1 and t1 < 1) or (0 < t2 and t2 < 1))

  def propagate(self):
    inputs = np.zeros((self.input_size, 1))
    input_list = [math.sin(pyxel.frame_count * 2), self.hunger]

    for eye in range(self.NUM_EYES*2):
      input_list += [*self.eyes[eye]]

    for i in range(self.input_size):
      inputs[i] = input_list[i]

    self.activations = self.network.activations(inputs)[3]