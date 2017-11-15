
"""
author: Wilhelm Poigner
email: 3xtraktor@gmail.com
"""
import pygame 
import math
import random
import os
import operator

####

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

####

class VectorSprite(pygame.sprite.Sprite):
    
    def __init__(self, angle = 0, damage=10, friction=1.0, hitpoints=100, i=0, 
                 layer=4, mass=10, speed=20, x=650, y=350, 
                 pointlist = None, image = None, color=None, bossnumber=None, imagenr=None, 
                 position = Vec2d(650, 350), movement = Vec2d(0, 0), facing = 0):
                     
            self._layer      = layer 
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.image       = image
            self.imagenr     = imagenr
            self.create_image()
           
            self.rect        = self.image.get_rect()
            self.rect.center = (position.x, position.y) 
            
            self.age         = 0
            self.maxage      = 0
            self.angle       = angle
            self.bossnumber  = bossnumber
            
            if color is None: 
                self.color   = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            else:
                self.color   = color
            
            self.damage      = damage
            self.drift       = True
            self.friction    = friction 
            self.facing     = facing
            self.hitpointsfull = hitpoints  
            self.init2()   
            self.lifetime    = 0
            self.mass        = mass
            self.maxlifetime = 5
            self.movement    = movement
            
            if movement == Vec2d(0, 0):
                movement = Vec2d(random.randint(-200, 200), random.randint(-200, 200))
            
            self.pointlist   = pointlist
            self.position    = position
            self.target = None # Vector
            self.turnspeed   = 50   
            self.speed       = speed 
            self.shortlife   = False
            self.path= []
            self.navI = 0
            self.init2()
            
    def init2(self, pos, mov):
        pass
                    
                    
    def create_image(self):
        self.image0 = self.image
        if self.image is not None:
            self.rect = self.image.get_rect()
            return
        minx = 0
        miny = 0
        maxx = 50
        maxy = 50
        for point in self.pointlist:
            if point.x < minx:
                minx = point.x
            if point.x > maxx:
                maxx = point.x
            if point.y < miny:
                miny = point.y
            if point.y > maxy:
                maxy = point.y
        self.image = pygame.Surface((maxx, maxy))
        old = (0, 0)
        for pos in pointlist:
            pygame.draw.line(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), old, pos)
        #pygame.draw.circle(self.image, (255,0,0), (2,2), 2)
        self.image.convert_alpha()  
        self.image0 = self.image.copy()
        
    def kill(self):
        del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
        
    def animate(self):
        pass
        
    def init2(self):
        pass    
        
    def rotate(self, angle):
        (self.oldx, self.oldy) = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle * -1)
        self.rect = self.image.get_rect()
        self.rect.center = (self.oldx, self.oldy)
        
    def forward(self, delta=1):
        deltavec = Vec2d(delta, 0)
        deltavec.rotate(self.movement.angle)
        #self.position += deltavec
        self.movement += deltavec
       
    def turnfaceright(self, seconds):
        angle = self.facing
        angle += self.turnspeed * seconds 
        self.facing += self.turnspeed * seconds
        oldcenter = self.rect.center
        self.image = pygame.transform.rotozoom(self.image0, angle, 1)
        self.rect = self.image.get_rect() 
        #snakex += oldrect.centerx - newrect.centerx
        #snakey += oldrect.centery - newrect.centery
        #self.facing.rotate(-self.self.turnspeed * seconds)
        #self.image.rotate(self.self.turnspeed * seconds)
        self.rect.center = oldcenter
    
    def turnfaceleft(self, seconds):
        angle = self.facing
        angle -= self.turnspeed * seconds 
        self.facing -= self.turnspeed * seconds
        oldcenter = self.rect.center
        self.image = pygame.transform.rotozoom(self.image0, angle, 1)
        self.rect = self.image.get_rect() 
        #snakex += oldrect.centerx - newrect.centerx
        #snakey += oldrect.centery - newrect.centery
        #self.facing.rotate(-self.self.turnspeed * seconds)
        #self.image.rotate(self.turnspeed * seconds)
        self.rect.center = oldcenter
        
    def faceto(self, angle):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotozoom(self.image0, angle, 1)
        self.rect = self.image.get_rect() 
        self.rect.center = oldcenter
        
    def turnleft(self, seconds):
        self.movement.rotate(-self.turnspeed * seconds)
        self.rotate(self.turnspeed * seconds)
        
    def turnright(self, seconds):
        self.movement.rotate(self.turnspeed * seconds)
        self.rotate(self.turnspeed * seconds)
       
    def flyToNextNavPoint(self):
        i2 = (self.navI +1) % len(self.path)
        self.nextNav = self.path[i2]
        self.movement = self.nextNav - self.position
        
        
        
    def update(self, seconds):
        self.age += seconds 
        if self.maxage > 0 and self.age > self.maxage:
            self.kill()
            return
        self.position += self.movement * seconds
        self.rect.center = (self.position.x, self.position.y)
        # reached navpoint?
        if len(self.path) > 0:
            #print(self.position.get_distance(self.nextNav))
            if self.position.get_distance(self.nextNav) < 5:
                self.position = self.nextNav
                self.rect.center = (self.position.x, self.position.y)
                self.navI += 1
                self.flyToNextNavPoint()
                i3 = (self.navI +2) % len(self.path)
                self.target = self.path[i3]
        if self.target is not None:
            dif = self.target - self.position
            dif = Vec2d(-dif.x, dif.y) 
            dif.rotate(180)
            #targetfacing = dif.angle
            #print(targetfacing, self.facing)
            
            adiff = (dif.angle - self.facing - 0) %360 #reset at 360
            if adiff == 0:
                pass
            if adiff < 180:
                self.turnfaceright(seconds)
            elif adiff > 180:
                self.turnfaceleft(seconds)
                
            #self.faceto(dif.angle)
            #print(dif.angle)

####

class Fragment(VectorSprite):
    
    def init2(self, pos=Vec2d(300,300), mov=None):
        self.position = pos
        if mov is None:
            self.movement = Vec2d(random.randint(-50,50), 
                                  random.randint(-50,50))
        else:
            self.movement = mov
        self.maxage = random.randint(1,3) # in seconds
        
        
    def create_image(self):
        self.color = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, self.color, (5,5), 3)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()  
        self.image0 = self.image.copy()
        

        

####

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

####

class PygView(object):
  
    width = 0
    height = 0
    gridsize = 50
    pictures = {}
  
    def __init__(self, width=1300, height=700, gridsize=50, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("ESC to quit")
        PygView.width = width    # also self.width 
        PygView.height = height  # also self.height
        PygView.gridsize = gridsize 
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        tmp = pygame.image.load(os.path.join("data","background06.jpg"))
        self.background = pygame.transform.scale(tmp, (self.width, self.height))
        self.grid()
        PygView.pictures["hunterpic"] = pygame.image.load(os.path.join("data","Hunter.png")).convert_alpha()
        PygView.pictures["bomberpic"] = pygame.image.load(os.path.join("data", "Bomber.png")).convert_alpha()
        PygView.pictures["paladinpic"] = pygame.image.load(os.path.join("data", "Paladin.png")).convert_alpha()
        PygView.pictures["frigatepic"] = pygame.image.load(os.path.join("data", "Frigate.png")).convert_alpha()
        PygView.pictures["mothershippic"] = pygame.image.load(os.path.join("data", "Mothership.png")).convert_alpha()
        PygView.pictures["dreadnaughtpic"] = pygame.image.load(os.path.join("data", "Dreadnaught.png")).convert_alpha()
        for filename in ["0", "1","2", "3", "4", "5", "6", "7", "8", "9", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18", "19", 
                         "20", "21", "22", "23", "24", "25", "26", "27", "28", 
                         "29", "30", "31", "32", "33", "34", "35"]:
            PygView.pictures["station"+filename+"pic"] = pygame.image.load(os.path.join("data", "Station"+filename+".png")).convert_alpha()
        
        PygView.pictures["torpedopic"] = pygame.image.load(os.path.join("data", "Torpedo.png")).convert_alpha()
        
        for filename in ["1a", "1aa", "1aaa", "1aaaa", "2a", "2aa", "2aaa", "2aaaa", "3a", "3aa", "3aaa", "3aaaa", "4a", "4aa", "4aaa", "4aaaa", 
                         "1b", "1bb", "1bbb", "1bbbb", "2b", "2bb", "2bbb", "2bbbb", "3b", "3bb", "3bbb", "3bbbb", "4b", "4bb", "4bbb", "4bbbb", ]:
            PygView.pictures["explosion_"+filename+"pic"] = pygame.image.load(os.path.join("data", "explosion_"+filename+".png")).convert_alpha()
        
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)


    def grid(self):
        for x in range(0, self.width, PygView.gridsize):
            pygame.draw.line(self.background, (128, 0, 128), (x, 0), (x, 701), 3 if x%100 == 0 else 1)
        for y in range(0, self.height, PygView.gridsize):
            pygame.draw.line(self.background, (128, 0, 128), (0, y), (1301, y), 3 if y%100 == 0 else 1)
        self.background.convert()#convert_alpha()
 
    def paint(self):
        """painting ships on the surface"""
        #groups
        self.allgroup =  pygame.sprite.LayeredUpdates()
        self.vectorspritegroup = pygame.sprite.Group()
        
        VectorSprite.groups = self.allgroup, self.vectorspritegroup
        
        self.station1 = Vec2d(325, 250)
        self.station2 = Vec2d(650, 450)
        self.station3 = Vec2d(975, 250)
        
        self.nadim = VectorSprite(image = PygView.pictures["hunterpic"])
        w = PygView.width
        h = PygView.height
        self.nadim.path = [Vec2d(round(w*0.5,0), round(h*0.5,0)),
                           Vec2d(round(w*0.6,0), round(h*0.25,0)),
                           Vec2d(round(w*0.75,0),round(h*0.25,0)),
                           Vec2d(round(w*0.95,0),round(h*0.5,0)),
                           Vec2d(round(w*0.75,0),round(h*0.75,0)),
                           Vec2d(round(w*0.6,0), round(h*0.75,0)),
                           Vec2d(round(w*0.5,0), round(h*0.5,0)), 
                           Vec2d(round(w*0.4,0), round(h*0.25,0)),
                           Vec2d(round(w*0.25,0),round(h*0.25,0)),
                           Vec2d(round(w*0.05,0),round(h*0.5,0)),
                           Vec2d(round(w*0.25,0),round(h*0.75,0)),
                           Vec2d(round(w*0.4,0), round(h*0.75,0))
                          ]
        self.nadim.position = self.nadim.path[0]
        self.nadim.flyToNextNavPoint()    
        
    def run(self):
        """-----------The mainloop------------"""
        self.paint() 
        running = True
        while running:
            # --------- update time -------------            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            
            
            # ------------ event handler: keys pressed and released -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                    if event.key == pygame.K_0:
                        self.nadim.target = None
                    if event.key == pygame.K_1:
                        self.nadim.target = self.station1
                    if event.key == pygame.K_2:
                        self.nadim.target = self.station2
                    if event.key == pygame.K_3:
                        self.nadim.target = self.station3
                        
            # --------- pressed key handler --------------            
            pressedkeys = pygame.key.get_pressed() 
            if pressedkeys[pygame.K_a]:
                self.nadim.movement.rotate(-5)
            if pressedkeys[pygame.K_d]:
                self.nadim.movement.rotate(+5)
            if pressedkeys[pygame.K_w]:
                self.nadim.forward(+1)
            if pressedkeys[pygame.K_s]:
                self.nadim.forward(-1)
            if pressedkeys[pygame.K_q]:
                self.nadim.turnfaceleft(seconds)
                self.nadim.facing -= 5 * -1
            if pressedkeys[pygame.K_e]:
                self.nadim.turnfaceright(seconds)
                self.nadim.facing += 5 * -1    
            if pressedkeys[pygame.K_SPACE]:
                Fragment()
                
            
            # ----- collision detection -----
            
            # -------- draw cannons ------------

            # ---------- update screen ----------- 
            self.screen.blit(self.background, (0, 0))
            write(self.screen, "FPS: {:6.3}  PLAYTIME:{:6.3} MINUTES:{:6.4} SECONDS".format(
                           self.clock.get_fps(), self.playtime//60, self.playtime))
            # fahrtrichtung nadim
            #self.nadimmove = self.nadim.movement.normalized() * 5
            pygame.draw.line(self.screen, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), 
                                                   (self.nadim.position.x, self.nadim.position.y), 
                                                   (self.nadim.position.x + self.nadim.movement.x * 1,
                                                    self.nadim.position.y + self.nadim.movement.y * 1),
                                                    10)
            
            self.allgroup.update(seconds) 
            self.allgroup.draw(self.screen)  
            pygame.display.flip()
        pygame.quit()
    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView().run()


