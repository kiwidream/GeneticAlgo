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

  #inputs
  OBJ_PRESENT = 0
  DISTANCE = 1
  COLOUT_0_IN = 2
  COLOUR_1_IN = 3
  COLOUR_2_IN = 4
  COLOUR_3_IN = 5
  COLOUR_4_IN = 6
  CLOCK = 7
  HUNGER = 8
  REPR_STR = 9

  #outputs
  ROT_LEFT = 0
  ROT_RIGHT = 1
  FORWARD = 2
  COLOUR_1_OUT = 3
  COLOUR_2_OUT = 4
  COLOUR_3_OUT = 5
  COLOUR_4_OUT = 6
  COLOUR_5_OUT = 7
  COLOUR_6_OUT = 8
  COLOUR_7_OUT = 9
  COLOUR_8_OUT = 10
  COLOUR_9_OUT = 11


  def __init__(self, x, y):
    super().__init__(x, y, 2)
    self.vx = 0
    self.vy = 0
    self.v = 0
    self.rot = 0
    self.hunger = 0
    sizes = [7, 24, 24, 12]
    self.network = Network(sizes)
    self.a = 0
    self.colour = 0
    self.dead = False
    self.eyesight = 250
    self.eye_seen = 0
    self.eye_dist = 100
    self.eye_colour = 0
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

  def draw(self):
    dist = self.eyesight - self.eye_dist
    pyxel.circ(self.x, self.y, self.radius, self.colour)
    #pyxel.line(self.x, self.y, self.x+math.cos(self.rot+self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(self.rot+self.eye_angle)*min(self.eyesight, dist), 5 if not bool(self.eye_seen) else 6)
    #pyxel.line(self.x, self.y, self.x+math.cos(self.rot-self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(self.rot-self.eye_angle)*min(self.eyesight, dist), 5 if not bool(self.eye_seen) else 6)
    #pyxel.line(self.x+math.cos(self.rot+self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(self.rot+self.eye_angle)*min(self.eyesight, dist), self.x+math.cos(self.rot-self.eye_angle)*min(self.eyesight, dist), self.y+math.sin(self.rot-self.eye_angle)*min(self.eyesight, dist), 5 if not bool(self.eye_seen) else 6)
    pyxel.text(self.x - 10, self.y + 10, str(self.species)+'-'+str(self.gen), 15)
    if self.repr_anim > 0:
      pyxel.text(self.x + 5, self.y - 10 - self.repr_anim // 10, "++", 15)

    if self.heart_anim:
      pyxel.text(self.x + 10, self.y - 10, "<3", 15)

  def update(self, food, bugs):
    min_obj = None
    min_dist = self.eyesight
    for drawable in food:
      if drawable != self:
        lx = math.cos(self.rot+self.eye_angle)*self.eyesight
        ly = math.sin(self.rot+self.eye_angle)*self.eyesight
        rx = math.cos(self.rot-self.eye_angle)*self.eyesight
        ry = math.sin(self.rot-self.eye_angle)*self.eyesight
        cx = drawable.x - self.x
        cy = drawable.y - self.y
        ca = math.atan2(cy, cx)
        la = math.atan2(ly, lx)
        ra = math.atan2(ry, rx)
        dr = abs(ra - ca)
        dl = abs(la - ca)
        if (dr < self.eye_angle * 2 and dl < self.eye_angle * 2):
          dist = math.sqrt(cx**2+cy**2)
          if dist < min_dist:
            min_obj = drawable
            min_dist = dist

    self.colour_str = 0
    for bug in bugs:
      if bug != self and bug.colour == self.colour:
        dist = math.sqrt((bug.x-self.x) ** 2 + (bug.y-self.y) ** 2)
        if dist < self.eyesight:
          self.colour_str += 2 * (1 - dist / self.eyesight)

    self.eye_seen = 0
    self.eye_dist = 0
    self.eye_colour = 0

    if self.age > 10:
      self.dead = True

    if min_obj is not None:
      self.eye_colour = min_obj.colour
      self.eye_dist = self.eyesight - min_dist
      self.eye_seen = 1

    for bit in food:
      if not bit.eaten and math.sqrt((bit.x - self.x) ** 2 + (bit.y - self.y) ** 2) < 10:
        bit.eaten = True
        self.food_count += 1
        if self.food_count > 16:
          self.dead = True
        self.hunger = 0

    self.propagate()
    self.rot += (self.activations[self.ROT_LEFT] - self.activations[self.ROT_RIGHT])
    self.v = min(max(self.activations[self.FORWARD], -2000), -2000) / 750

    self.vx = -math.cos(self.rot) * self.v
    self.vy = -math.sin(self.rot) * self.v

    if self.x + self.vx > 0 and self.x + self.vx < 256:
      self.x += self.vx

    if self.y + self.vy > 0 and self.y + self.vy < 256:
      self.y += self.vy

    self.repr_timer += 1

    if self.repr_anim > 0:
      self.repr_anim -= 1

    self.heart_anim = False
    if self.food_count > 6 and len(bugs) < 35:
      self.heart_anim = True
      for partner in bugs:
        if partner != self and partner.food_count > 6 and math.sqrt((partner.x - self.x) ** 2 + (partner.y - self.y) ** 2) < 15:
          for i in range(4):
            new_bug = Bug(self.x, self.y)
            new_bug.network.weights = np.copy(self.network.weights)
            new_bug.network.biases = np.copy(self.network.biases)
            new_bug.merge_network(partner.network)
            new_bug.mutate()
            new_bug.species = self.species
            new_bug.gen = self.gen + 1
            new_bug.repr_anim = 100
            bugs.append(new_bug)
          self.repr_timer = 0
          self.repr_anim = 100
          self.food_count -= 7
          partner.food_count -= 7
          partner.repr_anim = 100
          self.age += 1
          partner.age += 1
          break

    c_act = [self.activations[i] for i in range(3, 12)]
    c_index = c_act.index(max(c_act))
    self.colour = self.COLOURS[c_index]

    self.hunger += 1
    if self.hunger >= 300:
      self.dead = True

  def merge_network(self, other_nw):
    b1 = random.uniform(0.01, 0.04)
    for i in range(len(other_nw.weights)):
      for j in range(len(other_nw.weights[i])):
        if random.uniform(0, 1) < 0.5:
          b1 = 2 - b1
        b2 = 2 - b1
        self.network.weights[i][j] = (other_nw.weights[i][j]*b1 + self.network.weights[i][j]*b2) / 2
        self.network.biases[i][j] = (other_nw.biases[i][j]*b1 + self.network.biases[i][j]*b2) / 2

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
    inputs = np.zeros((7, 1))
    input_list = [self.eye_seen, self.eye_dist, int(self.eye_colour == 3), math.sin(pyxel.frame_count * 6), self.hunger, self.colour_str, self.food_count]
    for i in range(7):
      inputs[i] = input_list[i]
    self.activations = self.network.activations(inputs)[3]