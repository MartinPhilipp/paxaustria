# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to move pygames Sprites 
around
"""


import pygame 
import math
import random
import os


class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
 
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
 
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        return bool(self.x or self.y)
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
 
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
 
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return Vec2d(-self.x, -self.y)
 
    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
 
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)
 
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))
 
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return Vec2d(-self.y, self.x)
 
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])
 
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
 
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2
 
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)
 
    def cross(self, other):
        return self.x*other[1] - self.y*other[0]
 
    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
 
    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y]
 
    def __setstate__(self, dict):
        self.x, self.y = dict   

class FlyingObject(pygame.sprite.Sprite):
    
    number = 0
    book = {}
    images = []
    
    def __init__(self, x=320, y=240, angle=0, dx=0, dy=0, i=0):
        """create Ship"""
        pygame.sprite.Sprite.__init__(self, self.groups) 
        self.image = Ship.images[i]
        self.image0 = Ship.images[i]
        self.i=i
        Ship.number += 1
        self.number = Ship.number
        self.shortlife=False
        self.lifetime = 0
        self.age = 0
        self.maxage = 0
        self.cooldown = 0
        self.maxlifetime = 5
        self.animatetime = 0
        self.imageage =0
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = x, y
        self._layer = 4
        self.dx = dx
        self.dy = dy
        self.rotate(self.angle)
        self.init2()
        
        def init2():
            pass
        
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
    
    def animate(self):
        pass
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.age += seconds
        self.imageage += seconds
        if self.animatetime > 0 and self.imageage > self.animatetime:
            self.imageage = 0
            self.animate()
        if self.maxage > 0:
            if self.age > self.maxage:
                self.kill()
        if self.cooldown > 0:
            self.cooldown -= seconds
        else:
            self.cooldown = 0
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.rect.centerx < 0 or self.rect.centerx > PygView.width:
            self.kill()
        if self.rect.centery < 0 or self.rect.centery > PygView.height:
            self.kill()

class Explosion(FlyingObject):
    
    pics = []
    
    def init2(self):
        self.shortlife = True
        self.maxlifetime = 1
        self.animtime = 0
        self.animcycle = 1/16
        self.pic = 0
        for f in range(random.randint(50, 100)):
            Shard(x=self.x -20, y=self.y -20)
        
    def create_image(self):
        self.image = Explosion.pics[0]
        self.image0 = self.image
        self.rect = self.image0.get_rect()
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.lifetime += seconds
        self.animtime += seconds
        if self.animtime > self.animcycle:
            self.animtime = 0
            self.pic += 1
            if self.pic >= len(Explosion.pics):
                self.pic = 0 
            self.image = Explosion.pics[self.pic]
            
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x-self.rect.width, 0)
        self.rect.centery = round(self.y-self.rect.height, 0)
        if self.shortlife and self.lifetime > self.maxlifetime:
            self.kill()

class ExplosionA(FlyingObject):
    
    pics = []
    
    def init2(self):
        self.shortlife = True
        self.maxlifetime = 1
        self.animtime = 0
        self.animcycle = 1/16
        self.pic = 0
        self.create_image()
        for f in range(random.randint(50, 100)):
            ShardA(x=self.x +20, y=self.y +20)
    
    def create_image(self):
        self.image = ExplosionA.pics[0]
        self.image0 = self.image
        #print(345678)# todo / bischen weniger FAKE???
    
    def update(self, seconds):
        self.lifetime += seconds
        self.animtime += seconds
        if self.animtime > self.animcycle:
            self.animtime = 0
            self.pic += 1
            if self.pic >= len(ExplosionA.pics):
                self.pic = 0 
            self.image = ExplosionA.pics[self.pic]
            self.rect = self.image0.get_rect()
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.shortlife and self.lifetime > self.maxlifetime:
            self.kill()
 
class Shard(FlyingObject):
    
    def init2(self):
        self.maxage = random.random()*2
        self.dx = random.randint(-50, 50)
        self.dy = random.randint(-50, 50)
        self.create_image()
        self.imageage = 0
    
    def create_image(self):
        self.image = pygame.Surface((2,2))
        pygame.draw.circle(self.image, (random.randint(50,155), random.randint(50,155), random.randint(100,255)), (1, 1), 1)
        self.image0 = self.image
        
        
class ShardA(Shard):
    
    def init2(self):
        self.maxage = random.random()*2
        self.dx = random.randint(-100, 100)
        self.dy = random.randint(-100, 100)
        self.create_image()
    
    def create_image(self):
        self.image = pygame.Surface((2,2))
        pygame.draw.circle(self.image, (random.randint(100,255), random.randint(50,155), random.randint(50,155),), (1, 1), 1)
        self.image0 = self.image






class Light(FlyingObject):
    
    def init2(self):
        self.viertel = random.randint(1,4)
        self.maxage = 0.4
        self.create_image()
    
    def create_image(self):
        self.image = pygame.Surface((60, 60))
        if self.viertel == 1:
            # x = 0 - 30, y = 0 - 30
            x1 = random.randint(0, 30)
            y1 = random.randint(0, 30)
            x2 = random.randint(0, 30)
            y2 = random.randint(0, 30)
            x3 = random.randint(0, 30)
            y3 = random.randint(0, 30)
            x4 = random.randint(0, 30)
            y4 = random.randint(0, 30)
        if self.viertel == 2:
            # x = 30 - 60, y = 0 - 30
            x1 = random.randint(30, 60)
            y1 = random.randint(0, 30)
            x2 = random.randint(30, 60)
            y2 = random.randint(0, 30)
            x3 = random.randint(30, 60)
            y3 = random.randint(0, 30)
            x4 = random.randint(30, 60)
            y4 = random.randint(0, 30)
        if self.viertel == 3:
            # x = 0 - 30, y = 30 - 60
            x1 = random.randint(0, 30)
            y1 = random.randint(30, 60)
            x2 = random.randint(0, 30)
            y2 = random.randint(30, 60)
            x3 = random.randint(0, 30)
            y3 = random.randint(30, 60)
            x4 = random.randint(0, 30)
            y4 = random.randint(30, 60)
        if self.viertel == 4:
            # x = 30 - 60, y = 30 - 60
            x1 = random.randint(30, 60)
            y1 = random.randint(30, 60)
            x2 = random.randint(30, 60)
            y2 = random.randint(30, 60)
            x3 = random.randint(30, 60)
            y3 = random.randint(30, 60)
            x4 = random.randint(30, 60)
            y4 = random.randint(30, 60)
            
        pygame.draw.line(self.image, (random.randint(100,200), random.randint(155,160), random.randint(255,255)), 
                        (30,30), (x1, y1), random.randint(1,3))
        pygame.draw.line(self.image, (random.randint(100,200), random.randint(155,160), random.randint(255,255)), 
                        (x1,y1), (x2, y2), random.randint(1,3))
        pygame.draw.line(self.image, (random.randint(100,200), random.randint(155,160), random.randint(255,255)), 
                        (x2,y2), (x3, y3), random.randint(1,3))
        pygame.draw.line(self.image, (random.randint(100,200), random.randint(155,160), random.randint(255,255)), 
                        (x3,y3), (x4, y4), random.randint(1,3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.age += seconds
        self.imageage += seconds
        if random.random() < 0.5:
            self.create_image()
        if self.animatetime > 0 and self.imageage > self.animatetime:
            self.imageage = 0
            self.animate()
        if self.maxage > 0:
            if self.age > self.maxage:
                self.kill()
        if self.cooldown > 0:
            self.cooldown -= seconds
        else:
            self.cooldown = 0
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.rect.centerx < 0 or self.rect.centerx > PygView.width:
            self.kill()
        if self.rect.centery < 0 or self.rect.centery > PygView.height:
            self.kill()

        
class Ship(FlyingObject):
    pass
   

class Hunter(Ship):
    
    pics=[]
    
    def init2(self):
        """create Ship"""
        self.side = 1
        self.image = Hunter.pics[0]
        self.image0 = Hunter.pics[0]
        self.i = 0
        self.di = 1
        self.imageage = 0
        self.angle = 270
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self._layer = 4
        self.dx = 4+random.random()*0.4-0.2
        self.dy = random.random()*3-1.5
        #self.rotate(self.angle)
        self.laserrange = 150
        self.hitpoints = 30
        self.laserdamage_per_second = 11
        
        self.laserdamagechance = 0.6
        self.animatetime = 1 / len(Hunter.pics)
    
    def animate(self):
        self.i += self.di
        if self.i == len(Hunter.pics)-1:
            self.di = -1
        elif self.i == 0:
            self.di=1
        self.image = Hunter.pics[self.i]
    
        
class Bomber(Ship):
    
    pics=[]
    
    def init2(self):
        """create Ship"""
        self.side = 2
        self.image = Ship.images[1]
        self.image0 = Ship.images[1]
        self.i = 1
        self.di = 1
        self.imageage = 0
        self.angle = 90
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self._layer = 4
        self.dx = -4+random.random()*0.4-0.2
        self.dy = random.random()*3-1.5
        self.rotate(self.angle)
        self.torpedorange = 150
        self.hitpoints = 25
        self.animatetime = 1 / len(Bomber.pics)
    
    def animate(self):
        self.i += self.di
        if self.i == len(Bomber.pics)-1:
            self.di = -1
        elif self.i == 0:
            self.di=1
        self.image = Bomber.pics[self.i]


def write(background, text, x=50, y=20, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
            font = pygame.font.SysFont('mono', fontsize, bold=True)
            fw, fh = font.size(text)
            surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

class Shoot(FlyingObject):
    pass
    
        
class KinetikShoot(Shoot):
    
    def init2(self):
        self.damage = 10
        self.maxage = 15
        i=2
        self.shortlife = True 
        #self.dx = random.random()*-30+1.5
        #self.dy = random.random()*3-1.5
        self.create_image()
        
    def create_image(self):
        self.image = KinetikShoot.kinetikshootpic
        self.image0 = KinetikShoot.kinetikshootpic
        self.rect = self.image0.get_rect()


class PygView(object):
    width = 0
    height = 0
  
    def __init__(self, width=1300, height=700, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        tmp = pygame.image.load(os.path.join("data","background03.jpg"))
        self.background = pygame.transform.scale(tmp, (self.width, self.height)).convert()
        #for x in range(0, 1301, 50):
        #    pygame.draw.line(self.background, (128, 0, 128), (x, 0), (x, 701), 3 if x%100 == 0 else 1)
        #for y in range(0, 701, 50):
        #    pygame.draw.line(self.background, (128, 0, 128), (0, y), (1301, y), 3 if y%100 == 0 else 1)
        Ship.images.append(pygame.image.load(os.path.join("data","links.png")).convert_alpha())
        Ship.images.append(pygame.image.load(os.path.join("data","rechts.png")).convert_alpha())
        tmp = pygame.image.load(os.path.join("data","Torpedo.png")).convert_alpha()
        KinetikShoot.kinetikshootpic = pygame.transform.scale(tmp, (10, 10))
        
        for filename in ["1b", "1bb", "1bbb", "1bbbb", "2b", "2bb", "2bbb", "2bbbb", "3b", "3bb", "3bbb", "3bbbb", "4b", "4bb", "4bbb", "4bbbb",]:
            Explosion.pics.append(pygame.image.load(os.path.join("data", "explosion_"+filename+".png")))
        random.shuffle(Explosion.pics)
        
        for filename in ["1a", "1aa", "1aaa", "1aaaa", "2a", "2aa", "2aaa", "2aaaa", "3a", "3aa", "3aaa", "3aaaa", "4a", "4aa", "4aaa", "4aaaa"]:
            ExplosionA.pics.append(pygame.image.load(os.path.join("data", "explosion_"+filename+".png")))
        random.shuffle(ExplosionA.pics)
        
        for filename in ["1","2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]:
            Hunter.pics.append(pygame.image.load(os.path.join("data", "links"+filename+".png")))
            
        for filename in ["1","2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]:
            Bomber.pics.append(pygame.image.load(os.path.join("data", "rechts"+filename+".png")))
        
        #for dimension in ((10, 10), (20, 20), (30, 30), (40, 40)):
        #    for name in ("explosion_1.png", "explosion_2.png", "explosion_3.png", "explosion_4.png"):
        #        tmp = pygame.image.load(os.path.join("data", name)).convert_alpha()
        #        tmp = pygame.transform.scale(tmp, dimension)
        #        Explosion.pics.append(tmp)
        #for dimension in ((10, 10), (20, 20), (30, 30), (40, 40)):
        #    for name in ("explosion_1a.png", "explosion_2a.png", "explosion_3a.png", "explosion_4a.png"):
        #        tmp = pygame.image.load(os.path.join("data", name)).convert_alpha()
        #        tmp = pygame.transform.scale(tmp, dimension)
        #        ExplosionA.pics.append(tmp)        
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.paint() 
        
    def paint(self):
        """painting on the surface and create sprites"""
        # make an interesting background 
        #draw_examples(self.background)
        # create (pygame) Sprites.
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        #self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.shipgroup = pygame.sprite.Group()
        self.huntergroup = pygame.sprite.Group()
        self.bombergroup = pygame.sprite.Group()
        self.shootgroup = pygame.sprite.Group()
        self.kinetikshootgroup = pygame.sprite.Group()
        self.explogroup =pygame.sprite.Group()
        
        #Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Ship.groups = self.allgroup, self.shipgroup
        Hunter.groups = self.allgroup, self.huntergroup, self.shipgroup
        Bomber.groups = self.allgroup, self.bombergroup, self.shipgroup
        KinetikShoot.groups = self.allgroup, self.kinetikshootgroup, self.shootgroup
        Explosion.groups = self.allgroup, self.explogroup
        ExplosionA.groups = self.allgroup, self.explogroup
        Shard.groups = self.allgroup, self.explogroup
        Light.groups = self.allgroup, self.explogroup
        
        #self.ball1 = Ball(x=100, y=100) # creating a Ball Sprite
        #self.ball2 = Ball(x=200, y=100) # create another Ball Sprite
        self.hunter = Hunter(x=400, y=350)
        self.bomber = Bomber(x=900, y=350) 
    
        

    def run(self):
        """The mainloop"""
        running = True
        y= 0
        x = 100
        dy = 25
        char = "x"
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                    if event.key == pygame.K_h:
                        Hunter(x=random.randint(50, 600), y=random.randint(50, 650)) 
                        
                    if event.key == pygame.K_g:
                        for z in range(10):
                            Hunter(x=random.randint(50, 600), y=random.randint(50, 650))
                        
                    if event.key == pygame.K_y:
                        KinetikShoot(x=100, y=100)
                    
                    if event.key == pygame.K_b:
                        Bomber(x=random.randint(700, 1250), y=random.randint(50, 650))
                        
                    if event.key == pygame.K_v:
                        for z in range(10):
                            Bomber(x=random.randint(700, 1250), y=random.randint(50, 650))
                    
                    if event.key == pygame.K_n:
                        for ship in self.allgroup:
                            ship.kill()
                                
                        
            # random wave of ships
            if random.random() < 0.005:
                for z in range(random.randint(5, 15)):
                    Bomber(x=random.randint(700, 1250), y=random.randint(50, 650))
                    Hunter(x=random.randint(50, 600), y=random.randint(50, 650))
                        
            # end of event handler
           
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            
            
            #---------Shard collision---------
            
            
            #----------Hunter fire laser at Bomber------------------
            for h in self.huntergroup:
                targets = []
                for b in self.bombergroup:
                    if ((h.x-b.x)**2 + (h.y-b.y)**2)**0.5 < h.laserrange:
                        targets.append(b)
                if len (targets) > 0:
                    number = 0
                    for t in targets:
                        if t.number > number:
                            number = t.number
                            target = t
                    #target = random.choice(targets)
                    pygame.draw.line(self.screen, (random.randint(100, 255), random.randint(0, 100), random.randint(50, 150)), (h.x, h.y), (target.x, target.y), 2)
                    if random.random() < 0.05:
                        Light(x=t.x, y=t.y)
                    if random.random() < h.laserdamagechance:
                        t.hitpoints -= h.laserdamage_per_second * seconds
                        #print(t, t.hitpoints)
                        if t.hitpoints < 1:
                            Explosion(x=t.x +40, y=t.y +40)
                            for a in range(90):
                                 s = Shard(x = t.x +20, y = t.y +20)
                                 s.dx = math.cos(a) * 50
                                 s.dy = math.sin(a) * 50
                            t.kill()
             
            for b in self.bombergroup:
                targets = []
                for h in self.huntergroup:
                    if ((b.x-h.x)**2 + (b.y-h.y)**2)**0.5 < b.torpedorange:
                        targets.append(h)
                if len (targets) > 0:
                    number = 0
                    for t in targets:
                        if t.number > number:
                            number = t.number
                            target = t 
                    if b.cooldown == 0:
                        KinetikShoot(b.x, b.y, dx = t.x-b.x, dy = t.y-b.y)
                        b.cooldown = 2
                    
            for k in self.kinetikshootgroup:
               crashgroup = pygame.sprite.spritecollide(k, self.huntergroup, False, pygame.sprite.collide_circle)
               for h in crashgroup:
                   #elastic_collision(ball, bullet) # change dx and dy of both sprites
                   #ball.hitpoints -= bullet.damage 
                   h.hitpoints -= k.damage
                   Light(x=t.x, y=t.y)
                   k.kill()
                   if h.hitpoints < 1:
                       ExplosionA(x=h.x, y=h.y)
                       for a in range(90):
                           s = ShardA(x = h.x +20, y = h.y +20)
                           s.dx = math.cos(a) * 100
                           s.dy = math.sin(a) * 100
                       h.kill()
            
            
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)           
        
            # write text over everything 
            #write(self.screen, "Press b to add another ballöÖäÄüÜß",x=self.width//2, y=250, center=True)
            # write moving text (not a Sprite)
                
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
