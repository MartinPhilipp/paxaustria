class FlyingObject(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0 # current number for new Sprite
    numbers = {} # {number: Sprite}
  
    
    def __init__(self, radius = 50,speed = 20, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, friction=1.0, mass=10,
                 hitpoints=100, damage=10, bossnumber = None, imagenr = None):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number # unique number for each sprite
        FlyingObject.number += 1 
        FlyingObject.numbers[self.number] = self
        self.radius = radius
        self.mass = mass
        self.damage = damage
        self.imagenr = imagenr
        self.bossnumber = bossnumber
        self.hitpoints = hitpoints
        self.hitpointsfull = hitpoints
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.turnspeed = 5   # only important for rotating
        self.speed = speed      # only important for ddx and ddy
        self.angle = 0
        self.X = 0
        self.Y = 0
        self.heading = Vec2d(0,1) # north
        
        self.x = x           # position
        self.y = y
        self.dx = dx         # movement
        self.dy = dy
        self.ddx = 0 # acceleration and slowing down. set dx and dy to 0 first!
        self.ddy = 0
        self.friction = friction # 1.0 means no friction at all
        if color is None: # create random color if no color is given
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        self.create_image()
        self.rect= self.image.get_rect()
        self.init2()
        
    def init2(self):
        pass # for specific init stuff of subclasses, overwrite init2
        
    def kill(self):
        del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
            
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        
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
    
    def rotate(self):
          """rotate because changes in self.angle"""
          self.oldcenter = self.rect.center
          self.image = pygame.transform.rotate(self.image0, self.angle)
          self.rect = self.image.get_rect()
          self.rect.center = self.oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction  # make the Sprite slower over time
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # alive?
        if self.hitpoints < 1:
            self.kill()

class FlyingObjectw(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }
    
    def __init__(self, radius = 50, color=None, x=320, y=240,
                 dx=None, dy=None, layer=4, hitpoints=100, mass=10, damage=10, angle=0):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number # unique number for each sprite
        FlyingObject.number += 1 
        FlyingObject.numbers[self.number] = self 
        self.radius = radius
        self.mass = mass
        self.lifetime = 0
        self.damage = damage
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.x = x
        self.y = y
        self.gotos={}
        self.maxlifetime=5
        self.shortlife=False
        self.angle=angle
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
        self.hitpoints = hitpoints
        self.hitpointsfull = hitpoints
        self.create_image()
        self.rect= self.image.get_rect()
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        self.init2()
        
    def rotate(self, angle):
        (self.oldx, self.oldy) = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.oldx, self.oldy)
        #print ("Helo")
        
    def kill(self):
        del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
        
    def init2(self):
        pass # for subclasses
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        self.image0 = self.image.copy()
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.lifetime += seconds
        self.x += self.dx * seconds
        self.y += self.dy * seconds
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
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # kill ?
        if self.hitpoints < 1:
            self.kill()
        if self.shortlife and self.lifetime > self.maxlifetime:
            self.kill()
