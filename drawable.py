from abc import ABC, abstractmethod

class Drawable(ABC):

  def __init__(self, x, y, radius):
    self.x = x
    self.y = y
    self.radius = radius
    self.colour = 0
    super().__init__()

  @abstractmethod
  def draw(self):
    pass

  @abstractmethod
  def update(self):
    pass