
"""
author: Wilhelm Poigner
email: 3xtraktor@gmail.com
"""
import pygame 
import math
import random
import os
import operator



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





class Hitpointbar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Boss sprite
        Boss needs a unique number in FlyingObjectw.numbers,
        self.hitpoints and self.hitpointsfull"""
    
        def __init__(self, bossnumber, height=7, color = (0,255,0), ydistance=10):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.bossnumber = bossnumber # lookup in Flyingobject.numbers
            self.boss = FlyingObjectw.numbers[self.bossnumber]
            self.height = height
            self.color = color
            self.ydistance = ydistance
            self.image = pygame.Surface((self.boss.rect.width,self.height))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,self.boss.rect.width,self.height),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            
            
        def update(self, time):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                    int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - self.ydistance
            #check if boss is still alive
            if self.bossnumber not in FlyingObjectw.numbers:
                self.kill() # kill the hitbar



class FlyingObjectw(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }
    
    def __init__(self, startpoint,radius = 50, x=320, y=240,
                 mass=10, damage=10, angle=0, 
                 speed=20,  dx=0, dy=0, i=0, layer=4, 
                 friction=1.0, hitpoints=100, move=Vec2d(0,0), 
                 color=None, bossnumber=None, imagenr=None):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObjectw.number # unique number for each sprite
        FlyingObjectw.number += 1 
        FlyingObjectw.numbers[self.number] = self 
        self.radius = radius
        self.mass = mass
        self.startpoint = startpoint
        self.imagenr = imagenr
        self.bossnumber = bossnumber
        self.drift = True
        self.turnspeed = 5   
        self.speed = speed      
        self.lifetime = 0
        self.damage = damage
        self.rotatespeed = 1 # grad pro sekunde
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.x = x
        self.y = y
        self.gotos={}
        self.maxlifetime = 5
        self.shortlife = False
        self.angle = angle
        self.position = Vec2d(self.x, self.y)
        self.move = Vec2d(move.x, move.y)
        if color is None: # create random color if no color is given
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        if dx is None:
            self.dx = random.random() * 100 - 50 # from -50 to 50
        else:
            self.dx = dx
        if dy is None:
            self.dy = random.random() * 100 - 50
        else:
            self.dy = dy
        self.hitpointsfull = hitpoints
        self.heading = Vec2d(0,1) 
        self.ddx = 0 
        self.ddy = 0
        self.friction = friction 
        self.create_image()
        self.rect= self.image.get_rect()
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        self.init2()
        
    def rotate(self, angle):
        (self.oldx, self.oldy) = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.oldx, self.oldy)
        self.angle = angle
        #print ("Helo")
        
    def kill(self):
        del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
    
    def animate(self):
        pass
        
    def init2(self):
        pass # for subclasses
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        self.image0 = self.image.copy()
        
    def turnleft(self):
        self.angle += self.turnspeed
        
    def turnright(self):
        self.angle -= self.turnspeed
        
    def forward(self):
        self.ddx = -math.sin(self.angle*GRAD) 
        self.ddy = -math.cos(self.angle*GRAD) 
        
    def backward(self):
        self.ddx = +math.sin(self.angle*GRAD) 
        self.ddy = +math.cos(self.angle*GRAD)  
        
    def straferight(self):
        self.ddx = +math.cos(self.angle*GRAD)
        self.ddy = -math.sin(self.angle*GRAD)
    
    def strafeleft(self):
        self.ddx = -math.cos(self.angle*GRAD) 
        self.ddy = +math.sin(self.angle*GRAD) 
        
    def turn2heading(self):
        """rotate into direction of movement (dx,dy)"""
        self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
        
    def rotate2heading(self, seconds):
        """rotate slowly into direction of movement (dx,dy)"""
        self.oldangle = self.angle
        self.newangle = math.atan2(-self.dx, -self.dy)/math.pi*180.0
        if self.newangle > self.oldangle:
            self.angle += self.rotatespeed*seconds 
        elif self.newangle < self.oldangle:
            self.angle -= self.rotatespeed*seconds
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
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
        if abs(self.dx) > 0 : 
            self.dx *= self.friction  # make the Sprite slower over time
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.lifetime += seconds
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.position = Vec2d(self.x, self.y)
        #if self.x - self.width //2 < 0:
        #    self.x = self.width // 2
        #    self.dx *= -1 
        #if self.y - self.height // 2 < 0:
        #    self.y = self.height // 2
        #    self.dy *= -1
        #if self.x + self.width //2 > PygView.width:
        #    self.x = PygView.width - self.width //2
        #    self.dx *= -1
        #if self.y + self.height //2 > PygView.height:
        #    self.y = PygView.height - self.height //2
        #    self.dy *= -1
        print(self.x, self.y)
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # kill ?
        if self.hitpoints < 1:
            self.kill()
        if self.shortlife and self.lifetime > self.maxlifetime:
            self.kill()
            
            
class Explosion(FlyingObjectw):
    
    pics = []
    
    def init2(self):
        self.shortlife = True
        self.maxlifetime = 1
        self.animtime = 0
        self.animcycle = 1/16
        self.pic = 0
        
        
    def create_image(self):
        self.image = Explosion.pics[0]
        self.image0 = self.image
        
        
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
            self.rect = self.image0.get_rect()
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.shortlife and self.lifetime > self.maxlifetime:
            self.kill()
            
            
            
class Ship(FlyingObjectw):
    pass
            
            
class Shoot(FlyingObjectw):
    pass
    
        
class KinetikShoot(Shoot):
    
    def init2(self):
        self.damage = 500
        self.shortlife = True 
        self.imageage = 10
        self.maxage = 10
        self.age = 10
        self.cooldown = 0.1
        self.animtime = 0
        self.animatetime = 0
        
    def create_image(self):
        self.image = KinetikShoot.kinetikshootpic
        self.image0 = KinetikShoot.kinetikshootpic
        self.rect = self.image0.get_rect()
        
class LaserShoot(Shoot):
    
    def init2(self):
        self.damage = 100
        self.shortlife = True 
        self.rotate(self.angle)
        
    def create_image(self):
        self.image = LaserShoot.lasershootpic
        self.image0 = LaserShoot.lasershootpic
        self.rect = self.image0.get_rect()



class Plane(FlyingObjectw):
    images = []
    
    """A plane that patrols the skies"""
    def init2(self):
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 0
        self.turnspeed = 111
        self.damage = 10
        self.ddx = 0
        self.friction = 1
        self.ddy = 0
        #self.dx = 2
        #self.dy = 2
        self.movement = Vec2d(2,2)
        self.x = 650
        self.y = 350
        self.startpoint = Vec2d(0, 0)
        self.position = Vec2d(650, 350)
        self.path = [
                    Vec2d(625, 100),
                    Vec2d(600, 125),
                    Vec2d(550, 150),
                    Vec2d(600, 175),
                    Vec2d(625, 200),
                    Vec2d(650, 250),
                    Vec2d(675, 200),
                    Vec2d(700, 175),
                    Vec2d(750, 150),
                    Vec2d(700, 125),
                    Vec2d(675, 100),
                    Vec2d(650, 50)
                    ]
        self.newpoint = 1
        self.oldpoint = 0
        #ist     -----     sollte   
        #links   statt   unten
        #rechts  statt  oben 
        #unten   statt   links
        #oben    statt    rechts
        
    def turnleft(self, seconds):
        self.angle -= self.turnspeed * seconds
        self.movement.rotate(-self.turnspeed * seconds)
        self.rotate(self.turnspeed * seconds)
        
    def turnright(self, seconds):
        self.angle += self.turnspeed * seconds
        self.movement.rotate(self.turnspeed * seconds)
        self.rotate(self.turnspeed * seconds)
    
    def create_image(self):
        self.image = Hunter.hunterpic
        self.image0 = Hunter.hunterpic
        self.rect = self.image0.get_rect()
    
    def rotate(self, angle):
        (self.oldx, self.oldy) = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle * -1)
        self.rect = self.image.get_rect()
        self.rect.center = (self.oldx, self.oldy)
        
    def update(self, seconds):
        move2 = self.movement.normalized()
        self.rotate(move2.get_angle())
        self.position += seconds * self.speed * move2
        if self.position.x < 0:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = 0
        if self.position.x > PygView.width:
            self.position.x = PygView.width
        if self.position.y > PygView.height:
            self.position.y = PygView.height
            
        self.rect.centerx = round(self.position.x, 0)
        self.rect.centery = round(self.position.y, 0)
        
        if self.hitpoints < 1:
            self.kill()



class Dreadnaught(FlyingObjectw):
    images = []
    
    def init2(self):
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 30
        self.turnspeed = 11
        self.damage = 10
        self.ddx = 0
        self.friction = 1
        self.ddy = 0
        self.dx = 2
        self.dy = 2
        self.x = 850
        self.y = 175
        self.path = [
                    (850, 175),
                    (850, 125),
                    (875, 75),
                    (925, 50),   
                    (975, 50),    
                    (1025, 75),    
                    (1050, 125),    
                    (1050, 175),   
                    (1025, 225),  
                    (1000, 275),  
                    (1000, 325),    
                    (1025, 375),    
                    (1075, 400),
                    (1125, 400),   
                    (1175, 375), 
                    (1200, 325),  
                    (1200, 275),    
                    (1175, 225),    
                    (1125, 200),   
                    (1075, 200),   
                    (1025, 225),
                    (975, 250),
                    (925, 250), 
                    (875, 225)
                    ]
        self.newpoint = 1
        self.oldpoint = 0
        
    def create_image(self):
        self.image = Dreadnaught.dreadnaughtpic
        self.image0 = Dreadnaught.dreadnaughtpic
        self.rect = self.image0.get_rect()
        
    def update(self, seconds):
        #print(self.x, self.y, self.rect.center)
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction 
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.path[self.oldpoint][0] < self.path[self.newpoint][0]:
            dirx = 1
        elif self.path[self.oldpoint][0] > self.path[self.newpoint][0]:
            dirx = -1
        else:
            dirx = 0
        if self.path[self.oldpoint][1] < self.path[self.newpoint][1]:
            diry = 1
        elif self.path[self.oldpoint][1] > self.path[self.newpoint][1]:
            diry = -1
        else:
            diry = 0
        pointwechsel = False            
        if dirx != 0:
            if dirx == 1:
                if self.x > self.path[self.newpoint][0]:
                    pointwechsel = True
            else:
                if self.x < self.path[self.newpoint][0]:
                    pointwechsel = True
        if diry != 0:
            if diry == 1:
                if self.y > self.path[self.newpoint][1]:
                    pointwechsel = True
            else:
                if self.y < self.path[self.newpoint][1]:
                    pointwechsel = True
        if pointwechsel:
            if self.newpoint == len(self.path)-1:
                self.oldpoint = self.newpoint
                self.newpoint = 0
            else:
                tmp = self.newpoint
                self.newpoint += 1
                self.oldpoint = tmp
            (self.x, self.y) = self.path[self.oldpoint]
            pointwechsel = False
            self.dx = self.path[self.newpoint][0] - self.path[self.oldpoint][0]
            self.dy = self.path[self.newpoint][1] - self.path[self.oldpoint][1]
            tmpvec = Vec2d(self.dx,self.dy).normalized()
            self.dx = tmpvec.x * self.speed        
            self.dy = tmpvec.y * self.speed 
            self.turn2heading()      
            
            if self.hitpoints < 1:
                self.kill()



class Station(Ship):
    
    pics=[]
    
    def init2(self):
        checked = False
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 600
        self.age=999
        self.cooldown=999
        self.maxage=999
        self.turnspeed = 11
        self.damage = 10
        self.ddx = 0
        self.friction = 1
        self.ddy = 0
        self.x = 650
        self.y = 550
        self.position = Vec2d (650, 550)
        self.startpoint = Vec2d(0, 0)
        self.side = 1
        self.image = Station.pics[0]
        self.image0 = Station.pics[0]
        self.i = 0
        self.di = 1
        self.imageage = 0
        self.angle = 270
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self._layer = 4
        self.dx = 0
        self.dy = 0
        #self.rotate(self.angle)
        self.animatetime = 1 / len(Station.pics)            
        
    def animate(self):
        self.i += self.di
        if self.i == len(Station.pics)-1:
            self.i = 0
            #self.di = -1
        #elif self.i == 0:
            #self.di=1
        self.image = Station.pics[self.i]
            

        
class Mothership(Ship):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        checked = False
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 30
        self.turnspeed = 11
        self.damage = 10
        self.ddx = 0
        self.friction = 1
        self.ddy = 0
        self.dx = 0
        self.dy = 0
        self.x = 100
        self.y = 275
        self.position = Vec2d (100, 275)
        self.startpoint = Vec2d(0, 0)
        self.path = [
        
        #            (100, 325),    
        #            (100, 275,),    
        #            (125, 225,),    
        #            (175, 200,),    
        #            (225, 200,),    
        #            (275, 225,),    
        #            (325, 250,),    
        #            (375, 250,),    
        #            (425, 225,),    
        #            (450, 175,),    
        #            (450, 125,),    
        #            (425, 75,),    
        #            (375, 50,),    
        #            (325, 50,),    
        #            (275, 75,),    
        #            (250, 125,),    
        #            (250, 175,),    
        #            (275, 225,),    
        #            (300, 275,),    
        #            (300, 325,),   
        #            (275, 375,),    
        #            (225, 400,),    
        #            (175, 400,),    
        #            (125, 375,)
                    ]
        self.newpoint = 1
        self.oldpoint = 0
                    
                      
                      
                      
    def create_image(self):
        self.image = Mothership.mothershippic
        self.image0 = Mothership.mothershippic
        self.rect = self.image0.get_rect()
    
    
    def goto(self, punkt):
        self.x = self.gotos[punkt][0]
        self.y = self.gotos[punkt][1]
        self.dx = self.gotos[punkt][2]
        self.dy = self.gotos[punkt][3]
        self.rotate(self.gotos[punkt][4])
        #self.image = pygame.transform.rotate(self.image0, self.gotos[punkt][4]) 
        self.angle = self.gotos[punkt][4]
     
     
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction 
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        #if self.path[self.oldpoint][0] < self.path[self.newpoint][0]:
        #    dirx = 1
        #elif self.path[self.oldpoint][0] > self.path[self.newpoint][0]:
        #    dirx = -1
        #else:
        #    dirx = 0
        #if self.path[self.oldpoint][1] < self.path[self.newpoint][1]:
        #    diry = 1
        #elif self.path[self.oldpoint][1] > self.path[self.newpoint][1]:
        #    diry = -1
        #else:
        #    diry = 0
        #pointwechsel = False            
        #if dirx != 0:
        #    if dirx == 1:
        #        if self.x > self.path[self.newpoint][0]:
        #            pointwechsel = True
        #    else:
        #        if self.x < self.path[self.newpoint][0]:
        #            pointwechsel = True
        #if diry != 0:
        #    if diry == 1:
        #        if self.y > self.path[self.newpoint][1]:
        #            pointwechsel = True
        #    else:
        #        if self.y < self.path[self.newpoint][1]:
        #            pointwechsel = True
        #if pointwechsel:
        #    if self.newpoint == len(self.path)-1:
        #        self.oldpoint = self.newpoint
        #        self.newpoint = 0
        #    else:
        #        tmp = self.newpoint
        #        self.newpoint += 1
        #        self.oldpoint = tmp
        #    (self.x, self.y) = self.path[self.oldpoint]
        #    pointwechsel = False
        #    self.dx = self.path[self.newpoint][0] - self.path[self.oldpoint][0]
        #    self.dy = self.path[self.newpoint][1] - self.path[self.oldpoint][1]
        #    tmpvec = Vec2d(self.dx,self.dy).normalized()
        #    self.dx = tmpvec.x * self.speed        
        #    self.dy = tmpvec.y * self.speed 
        #    self.turn2heading()      
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.hitpoints < 1:
            self.kill()   
        
        
class Hunter(Ship):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        self.mass = 150
        checked = False
        self.ziel = 2
        self.lifetime =-1
    
    
    def create_image(self):
        self.image = Hunter.hunterpic
        self.image0 = Hunter.hunterpic
        self.rect = self.image0.get_rect()
    
    
class Bomber(Ship):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        self.mass = 150
        checked = False
        self.ziel = 2
        
         
    def create_image(self):
        self.image = Bomber.bomberpic
        self.image0 = Bomber.bomberpic
        self.rect = self.image0.get_rect()
         
        
class Paladin(Ship):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        self.mass = 150
        checked = False
        self.ziel = 2
        self.lifetime =-2
    
    
    def create_image(self):
        self.image = Paladin.paladinpic
        self.image0 = Paladin.paladinpic
        self.rect = self.image0.get_rect()
 
 
class Frigate(Ship):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        self.mass = 150
        checked = False
        self.ziel = 2
    
    
    def create_image(self):
        self.image = Frigate.frigatepic
        self.image0 = Frigate.frigatepic
        self.rect = self.image0.get_rect()
        
               

def write(background, text, x=10, y=10, color=(159, 159, 159),
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
    
def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .x .y, .dx, dy
           by Leonard Michlmayr"""
        # here we do some physics: the elastic
        # collision
        #
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.x - sprite2.x
        diry = sprite1.y - sprite2.y
        #
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        #
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        # (dirx,diry) is perpendicular to the mirror
        # surface. We use the dot product to
        # project to that direction.
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            # no distance? this should not happen,
            # but just in case, we choose a random
            # direction
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        # We are done. (dirx * dp, diry * dp) is
        # the projection of the velocity
        # perpendicular to the virtual mirror
        # surface. Subtract it twice to get the
        # new direction.
        #
        # Only collide if the sprites are moving
        # towards each other: dp > 0
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp



class Shape():
    
    def __init__(self, startpoint, pointlist, zoom=1, angle=0, color=100, width=1):
        self.startpoint = startpoint
        self.pointlist = pointlist
        self.rotationpoint = Vec2d(0,0)
        self.zoom = zoom
        self.angle = angle
        self.color = color
        self.width = width
    
    def forward(self, delta=1):
        deltavec = Vec2d(delta, 0)
        deltavec.rotate(self.angle)
        self.startpoint += deltavec
    
    def rotate(self, delta_angle=1):
        """alters pointlist by rotation with angle from rotationpoint"""
        self.angle += delta_angle
        #print(self.angle)
        for point in self.pointlist:
            point.rotate(delta_angle)    
        
    def draw(self, screen):
        oldpoint = self.pointlist[0]
        #pygame.draw.line(self.screen, self.color, (0,0),(100,10),2)
        #pygame.draw.line(self.screen, self.color, (100,10),(10,150),2)
        self.color2 = (random.randint(80,120), self.color, random.randint(80,120))
        for point in self.pointlist:
            #print("painting from point", oldpoint.x, oldpoint.y, "to", point.x, point.y)
            pygame.draw.line(screen, self.color2,
                (self.startpoint.x + oldpoint.x * self.zoom,
                 self.startpoint.y + oldpoint.y * self.zoom),
                (self.startpoint.x + point.x * self.zoom,
                 self.startpoint.y + point.y * self.zoom)
                 ,self.width)
            oldpoint = point






class PygView(object):
    width = 0
    height = 0
  
    def __init__(self, width=1301, height=701, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        tmp = pygame.image.load(os.path.join("data","background01.jpg"))
        self.background = pygame.transform.scale(tmp, (self.width, self.height))
        # violet
        for x in range(0, 1301, 50):
            pygame.draw.line(self.background, (128, 0, 128), (x, 0), (x, 701), 3 if x%100 == 0 else 1)
        for y in range(0, 701, 50):
            pygame.draw.line(self.background, (128, 0, 128), (0, y), (1301, y), 3 if y%100 == 0 else 1)
        #for radius in range(10, 200, 30):
        #    pygame.draw.circle(self.background, (4, 127, 0), (650, 350), radius, 5)
        self.background.convert()#convert_alpha()
        Hunter.hunterpic = pygame.image.load(os.path.join("data","Hunter.png")).convert_alpha()
        Bomber.bomberpic = pygame.image.load(os.path.join("data","Bomber.png")).convert_alpha()
        Paladin.paladinpic = pygame.image.load(os.path.join("data","Paladin.png")).convert_alpha()
        Frigate.frigatepic = pygame.image.load(os.path.join("data","Frigate.png")).convert_alpha()
        Mothership.mothershippic = pygame.image.load(os.path.join("data","Mothership.png")).convert_alpha()
        Dreadnaught.dreadnaughtpic = pygame.image.load(os.path.join("data","Dreadnaught.png")).convert_alpha()
        
        for filename in ["0", "1","2", "3", "4", "5", "6", "7", "8", "9", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18", "19", 
                         "20", "21", "22", "23", "24", "25", "26", "27", "28", 
                         "29", "30", "31", "32", "33", "34", "35"]:
            Station.pics.append(pygame.image.load(os.path.join("data", "Station"+filename+".png")))
        #tmp = pygame.image.load(os.path.join("data","shield.png")).convert_alpha()
        #Shoot.shootpic = pygame.transform.scale(tmp, (25, 25))
        tmp = pygame.image.load(os.path.join("data","Torpedo.png")).convert_alpha()
        KinetikShoot.kinetikshootpic = pygame.transform.scale(tmp, (25, 25))
        
        for filename in ["1a", "1aa", "1aaa", "1aaaa", "2a", "2aa", "2aaa", "2aaaa", "3a", "3aa", "3aaa", "3aaaa", "4a", "4aa", "4aaa", "4aaaa", 
                         "1b", "1bb", "1bbb", "1bbbb", "2b", "2bb", "2bbb", "2bbbb", "3b", "3bb", "3bbb", "3bbbb", "4b", "4bb", "4bbb", "4bbbb", ]:
            tmp = pygame.image.load(os.path.join("data", "explosion_"+filename+".png")).convert_alpha()
            Explosion.pics.append(tmp)
        
        
                
        #tmp = pygame.image.load(os.path.join("data","Laser.png")).convert_alpha()
        #LaserShoot.lasershootpic = pygame.transform.scale(tmp, (5000, 1))
        #self.background = pygame.Surface(self.screen.get_size()).convert()  
        #self.background.fill((255,255,255)) # fill background white
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
        #self.bulletgroup = pygame.sprite.Group()
        self.shipgroup = pygame.sprite.Group()
        self.bombergroup = pygame.sprite.Group()
        self.huntergroup = pygame.sprite.Group()
        self.paladingroup = pygame.sprite.Group()
        self.frigategroup = pygame.sprite.Group()
        self.mothershipgroup = pygame.sprite.Group()
        self.dreadnaughtgroup = pygame.sprite.Group()
        self.stationgroup = pygame.sprite.Group()
        self.shootgroup = pygame.sprite.Group()
        self.explogroup = pygame.sprite.Group()
        self.planegroup = pygame.sprite.Group()
        #Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Frigate.groups = self.allgroup, self.frigategroup
        Mothership.groups = self.allgroup, self.mothershipgroup
        Dreadnaught.groups = self.allgroup, self.dreadnaughtgroup
        Station.groups = self.allgroup, self.stationgroup
        Hunter.groups = self.allgroup, self.huntergroup
        Bomber.groups = self.allgroup, self.bombergroup
        Paladin.groups = self.allgroup, self.paladingroup
        #Bullet.groups = self.allgroup, self.bulletgroup
        KinetikShoot.groups = self.allgroup, self.shootgroup 
        LaserShoot.groups = self.allgroup, self.shootgroup
        Explosion.groups = self.allgroup, self.explogroup
        Plane.groups = self.allgroup, self.planegroup
        # create Ship
        self.mothership1 = Mothership (startpoint=Vec2d(100,325))
        self.dreadnaught1 = Dreadnaught (startpoint=Vec2d(850,175))
        self.station1 = Station (startpoint=Vec2d(650,600))
        self.plane1 = Plane (startpoint=Vec2d(650,200))
        
        
        self.dreeck = Shape( Vec2d(650, 350),
                                         (Vec2d(0, 0),
                                          Vec2d(0, -10),
                                          Vec2d(30, -10),
                                          Vec2d(30, -40),
                                          Vec2d(50, 0),
                                          Vec2d(30, 40),
                                          Vec2d(30, 10),
                                          Vec2d(0, 10),
                                          Vec2d(0, 0)
                                         ), width = 10)
        
        
        
        
        

    def run(self):
        """The mainloop"""
        
        lasers = []
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                #---------------- press once keyhandler----------------    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # -----------------pressed keyhandler ------------------           
            pressedkeys = pygame.key.get_pressed()
            #if pressedkeys[pygame.K_LEFT]:
            #    self.plane1.movement.rotate(-10)
            #if pressedkeys[pygame.K_RIGHT]:
            #    self.plane1.movement.rotate(10)
            if pressedkeys[pygame.K_w]:
                self.plane1.speed += 1
            if pressedkeys[pygame.K_s]:
                self.plane1.speed -= 1
            if pressedkeys[pygame.K_a]:
                self.plane1.turnleft(seconds)
            if pressedkeys[pygame.K_d]:
                self.plane1.turnright(seconds)
                    
            
            
            
                    #if event.key == pygame.K_b:
                    #    Ball(x=random.randint(0,PygView.width-100)) # add big balls!
                    #if event.key == pygame.K_c:
                    #    Bullet(radius=5, x=0,y=0, dx=200, dy=200)
                    #if event.key ==pygame.K_1:
                    #    self.bomber1.goto1()
                    #if event.key ==pygame.K_2:
                    #    self.bomber1.goto2()
                    #if event.key ==pygame.K_3:
                    #    self.bomber1.goto3()
                    #if event.key == pygame.K_1:
                    #    KinetikShoot(x=self.mothership1.x, y=self.mothership1.y, dx=self.mothership1.dx*10, dy=self.mothership1.dy*10, )
                    #if event.key == pygame.K_2:
                    #    LaserShoot(x=self.mothership1.x, y=self.mothership1.y, dx=self.mothership1.dx*50, dy=self.mothership1.dy*50, angle=self.mothership1.angle+90)
                    #    pygame.draw.line(self.screen, (255, 82, 0), (self.mothership1.x, self.mothership1.y ), (self.mothership1.x+self.mothership1.dx*20, self.mothership1.y+self.mothership1.dy*20))
                    #    laser.append([(255, 82, 0), (self.mothership1.x, self.mothership1.y ), (self.mothership1.x+self.mothership1.dx*20, self.mothership1.y+self.mothership1.dy*20)])
                    #    for x in range(15):
                    #        lasers.append([(255, 82, 0), (self.mothership1.x, self.mothership1.y ), (self.mothership1.x+self.mothership1.dx*200, self.mothership1.y+self.mothership1.dy*200)])
                    #if event.key == pygame.K_3:
                    #    Explosion(x=self.mothership1.x, y=self.mothership1.y, dx=self.mothership1.dx, dy=self.mothership1.dy)
                    #if event.key == pygame.K_l:
                    #    self.plane1.angle += 15
                    #    self.plane1.rotate()
                    #if event.key == pygame.K_k:
                    #    self.plane1.angle -= 15
                    #    self.plane1.rotate()
                        
                
           
            
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            #pygame.draw.line(self.screen)
            for line in lasers:
                pygame.draw.line(self.screen, line[0], line[1], line[2])
            if len(lasers) >0:
                del lasers[0]
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME:{:6.3} MINUTES:{:6.4} SECONDS".format(
                           self.clock.get_fps(), self.playtime//60, self.playtime))
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            # ---------- collision detection between ball and bullet sprites ---------
            #for ball in self.ballgroup:
               #crashgroup = pygame.sprite.spritecollide(ball, self.bulletgroup, False, pygame.sprite.collide_circle)
               #for bullet in crashgroup:
                   #elastic_collision(ball, bullet) # change dx and dy of both sprites
                   #ball.hitpoints -= bullet.damage
            # --------- collision detection between ball and other balls
            #for ball in self.ballgroup:
                #crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
                #for otherball in crashgroup:
                    #if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
                        #elastic_collision(ball, otherball) # change dx and dy of both sprites
            # ---------- collision detection between bullet and other bullets
            #for bullet in self.bulletgroup:
                #crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
                #for otherbullet in crashgroup:
                    #if bullet.number > otherbullet.number:
                         #elastic_collision(bullet, otherball) # change dx and dy of both sprites
            # -------- remove dead -----
            #for sprite in self.ballgroup:
            #    if sprite.hitpoints < 1:
            #        sprite.kill()
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)  
            # fahrtrichtung plane1
            pygame.draw.line(self.screen, (0,255,0), (self.plane1.position.x, self.plane1.position.y), 
                                                   (self.plane1.position.x + self.plane1.movement.x * 10,
                                                    self.plane1.position.y + self.plane1.movement.y * 10),
                                                    3)
            # Vector von plane1 zu mothership1
            #mommy = Vec2d(self.mothership1.x, self.mothership1.y) - self.plane1.position
            #mommy = mommy.normalized()
            #pygame.draw.line(self.screen, (0,255,200), (self.plane1.position.x, self.plane1.position.y), 
            #                                       (self.plane1.position.x + mommy.x * 10,
            #                                        self.plane1.position.y + mommy.y * 10),
            #                                        3)
            
            # -------- draw cannons ------------
            
            # cannon plane aiming at nearest player 
            c1 =  self.mothership1.position - self.plane1.position 
            c2 =  self.station1.position - self.plane1.position
            #print("c1=", c1, "c2=", c2)
            if c1.get_length() < c2.get_length():
                c = c1
            else:
                c = c2
            c = c.normalized()
            c *= 10
            pygame.draw.line(self.screen, (200,50,0), (self.plane1.position.x,
                                                    self.plane1.position.y),
                                                    (self.plane1.position.x + c.x,
                                                    self.plane1.position.y + c.y),
                                                    2) 
            
            

            #  mothership1 aiming at nearest player 
            d1 =  self.plane1.position - self.mothership1.position 
            d2 =  self.station1.position - self.mothership1.position
            if d1.get_length() < d2.get_length():
                d = d1
            else:
                d = d2
            d = d.normalized()
            d *= 10
            pygame.draw.line(self.screen, (100,100,100), (self.mothership1.position.x,
                                                    self.mothership1.position.y),
                                                    (self.mothership1.position.x + d.x,
                                                    self.mothership1.position.y + d.y),
                                                    2)                             
                                                    
                                                    
                                                    
             #  station1 aiming at nearest player 
            e1 =  self.plane1.position - self.station1.position 
            e2 =  self.mothership1.position - self.station1.position
            if e1.get_length() < e2.get_length():
                e = e1
            else:
                e = e2
            e = e.normalized()
            e *= 10
            pygame.draw.line(self.screen, (100,100,100), (self.station1.position.x,
                                                    self.station1.position.y),
                                                    (self.station1.position.x + d.x,
                                                    self.station1.position.y + d.y),
                                                    2)                                                                       
                                                    
                                                                 
                                                    
            
            
            # --------- (auto)fire -------
            
            speedfactor = 0.05
            if self.plane1.hitpoints > 0 and pressedkeys[pygame.K_LSHIFT]:
            #if random.random() < 0.1:
                move = c * speedfactor # + self.yanniks_ship.move
                KinetikShoot(self.screen, self.plane1.position+d, move*50, self.plane1.number, )                      
            
            if self.mothership1.hitpoints > 0 and pressedkeys[pygame.K_RSHIFT]:                                                
            #if random.random() < 0.1:
                move = d * speedfactor 
                KinetikShoot(self.screen, self.mothership1.position+d, move*50, self.mothership1.number, )   
            
            if self.station1.hitpoints > 0 and pressedkeys[pygame.K_z]:
                move = e * speedfactor
                KinetikShoot(self.screen, self.station1.position+d, move*50, self.station1.number, )   
            
            
            # arrow
            # print(self.dreeck.angle, self.mothership1.angle)
            self.dreeck.startpoint.x, self.dreeck.startpoint.y = self.mothership1.rect.center
            #self.dreeck.rotate(self.dreeck.angle - self.mothership1.angle)
            
            #self.dreeck.draw(self.screen)
                     
            # write text over everything 
            #write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            #write(self.screen, "Press c to add another bullet", x=self.width//2, y=350, center=True)
            # next frame
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    PygView().run() 
