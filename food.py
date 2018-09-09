from network import Network
import pyxel
from pyxel import constants
import math
import numpy as np
from drawable import Drawable
import sys

class Food(Drawable):

  def __init__(self, x, y):
    super().__init__(x, y, 1)
    self.colour = 3
    self.eaten = False

  def draw(self):
    pyxel.circ(self.x, self.y, self.radius, self.colour)

  def update(self):
    pass