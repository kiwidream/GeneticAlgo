from network import Network
import pyxel
from pyxel import constants
import math
import numpy as np
from drawable import Drawable
import sys

class Food(Drawable):

  def __init__(self, x, y, deadly=False):
    super().__init__(x, y, 1)
    self.deadly = deadly
    self.colour = 8 if deadly else 3
    self.eaten = False
    self.timer = 200

  def draw(self):
    pyxel.circ(self.x, self.y, self.radius, self.colour)

  def update(self):
    self.timer -= 1
    if self.timer <= 0:
      self.eaten = True