
"""
author: Wilhelm Poigner
email: 3xtraktor@gmail.com
"""
import pygame 
import math
import random
import os
import operator
import Vector_2D as v


####


class VectorSprite(pygame.sprite.Sprite):
    
    def __init__(self, angle = 0, damage=10, friction=1.0, hitpoints=100, i=0, 
                 layer=4, mass=10, speed=15, x=650, y=350, 
                 pointlist = None, image = None, color=None, bossnumber=None, imagenr=None, 
                 position = v.Vec2d(650, 350), movement = v.Vec2d(0, 0), facing = 0):
                     
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
            
            if movement == v.Vec2d(0, 0):
                movement = v.Vec2d(random.randint(-200, 200), random.randint(-200, 200))
            
            self.pointlist   = pointlist
            self.position    = position
            self.target = None # Vector
            #self.turnspeed   = 50   
            self.turnspeed   = 5
            self.speed       = speed 
            self.shortlife   = False
            self.path= []
            self.navI = 0
            self.init2()
            
    def init2(self, position, mov):
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
        for position in pointlist:
            pygame.draw.line(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), old, position)
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
        deltavec = v.Vec2d(delta, 0)
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
        #self.movement.normalized()
        #print("movement norm:", self.movement.normalized())
        self.movement = self.movement.normalized() * self.speed
        
        
        
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
            if self.position.get_distance(self.nextNav) < 1:
                self.position = self.nextNav
                self.rect.center = (self.position.x, self.position.y)
                self.navI += 1
                self.flyToNextNavPoint()
                i3 = (self.navI +2) % len(self.path)
                self.target = self.path[i3]
        if self.target is not None:
            dif = self.target - self.position
            dif = v.Vec2d(-dif.x, dif.y) 
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
    
    def init2(self, position=v.Vec2d(300,300), mov=None):
        self.position = position
        if mov is None:
            self.movement = v.Vec2d(random.randint(-50,50), 
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
        
        
class Ufo(VectorSprite):
  
    def update(self, seconds):
        # --- chance to change movement vector ---
        if random.random() < 0.001:
            self.movement=v.Vec2d(random.randint(-80,80),
                              random.randint(-80,80))
        # --- bounce on screen edge ---
        if self.position.x < 0:
            self.position.x = 0
            self.movement.x *= -1
        elif self.position.x > PygView.width:
            self.position.x = PygView.width
            self.movement.x *= -1
        if self.position.y < 0:
            self.position.y = 0
            self.movement.y *= -1
        elif self.position.y > PygView.height:
            self.position.y = PygView.height
            self.movement.y *= -1
        VectorSprite.update(self, seconds)
  
    def create_image(self):
        self.image = pygame.Surface((100, 90))
        pygame.draw.polygon(self.image, (255, 0, 0), [(0, 45), (20, 0), (100, 45), (20, 90)],1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha() 
        

        

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



def paint_hex(background, middle, radius, color=(64,64,64)):
    
    start= v.Vec2d(middle.x, middle.y)
    pointlist = []
    line = v.Vec2d(0, radius)
    pointlist.append(middle+line)
    line.rotate(90+60)
    
    for s in range(6):
       pointlist.append(pointlist[-1]+line)
       line.rotate(60)
       
    pygame.draw.polygon(background, color, [(p.x, p.y) for p in pointlist],1)  


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
        pygame.draw.ellipse(self.background, (64,64,64), (PygView.width/4, PygView.height/7, PygView.width/2, PygView.height/7*5), 1)
        pygame.draw.polygon(self.background, (64,64,64), (
                                                          (0,0),
                                                          (PygView.width/14*3, 0),
                                                          (PygView.width/28*5, PygView.height/14),
                                                          (PygView.width/28*5, PygView.height/14*13),
                                                          (PygView.width/14*3, PygView.height),
                                                          (0, PygView.height),
                                                          ), 0)
        pygame.draw.polygon(self.background, (64,64,64), (
                                                          (PygView.width,0),
                                                          (PygView.width/14*11, 0),
                                                          (PygView.width/28*23, PygView.height/14),
                                                          (PygView.width/28*23, PygView.height/14*13),
                                                          (PygView.width/14*11, PygView.height),
                                                          (PygView.width, PygView.height),
                                                          ), 0)
        # self.grid()
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
        for x in range (0, PygView.width, 150):
            for y in range (0, PygView.height, 87):
                paint_hex(self.background, v.Vec2d(x, y), 50)
        for x in range (0, PygView.width, 150):
            for y in range (0, PygView.height, 87):
                paint_hex(self.background, v.Vec2d(x+75, y+45), 50)


    def grid(self, color1=(128,0,128), color2=(200,0,200), bold=5):
        
        for x in range(0, self.width, PygView.gridsize):
            pygame.draw.line(self.background, color1, (x, 0), (x, 701),  1)
        for y in range(0, self.height, PygView.gridsize):
            pygame.draw.line(self.background, color1, (0, y), (1301, y), 1)
        counter = 0
        for x in range(0, self.width, PygView.gridsize):
            counter += 1
            if counter % bold == 0:
                pygame.draw.line(self.background, color2, (x, 0), (x, 701),  3)
        counter = 0
        for y in range(0, self.height, PygView.gridsize):
            counter += 1
            if counter % bold == 0:
                pygame.draw.line(self.background, color2, (0, y), (1301, y), 3)
            
            
 
    def paint(self):
        """painting ships on the surface"""
        #groups
        self.allgroup =  pygame.sprite.LayeredUpdates()
        self.vectorspritegroup = pygame.sprite.Group()
        
        VectorSprite.groups = self.allgroup, self.vectorspritegroup
        
        self.station1 = v.Vec2d(325, 250)
        self.station2 = v.Vec2d(650, 450)
        self.station3 = v.Vec2d(975, 250)
        
        #self.nadim = VectorSprite(image = PygView.pictures["hunterpic"])
        #w = PygView.width
        #h = PygView.height
        #self.nadim.path = [v.Vec2d(round(w*0.5,0), round(h*0.5,0)),
        #                   v.Vec2d(round(w*0.6,0), round(h*0.25,0)),
        #                   v.Vec2d(round(w*0.75,0),round(h*0.25,0)),
        #                   v.Vec2d(round(w*0.95,0),round(h*0.5,0)),
        #                   v.Vec2d(round(w*0.75,0),round(h*0.75,0)),
        #                   v.Vec2d(round(w*0.6,0), round(h*0.75,0)),
        #                   v.Vec2d(round(w*0.5,0), round(h*0.5,0)), 
        #                   v.Vec2d(round(w*0.4,0), round(h*0.25,0)),
        #                   v.Vec2d(round(w*0.25,0),round(h*0.25,0)),
        #                   v.Vec2d(round(w*0.05,0),round(h*0.5,0)),
        #                   v.Vec2d(round(w*0.25,0),round(h*0.75,0)),
        #                   v.Vec2d(round(w*0.4,0), round(h*0.75,0))
        #                  ]
        #self.nadim.position = self.nadim.path[0]
        #self.nadim.flyToNextNavPoint()    
        
        self.dreadnaught = VectorSprite(image = PygView.pictures["dreadnaughtpic"])
        w = PygView.width
        h = PygView.height
        self.dreadnaught.path = [v.Vec2d(round(w*0.250,0), round(h*0.50,0)),
        
                                  v.Vec2d(round(w*0.250,0), round(h*0.55,0)),
                                  v.Vec2d(round(w*0.255,0), round(h*0.60,0)),
                                  v.Vec2d(round(w*0.275,0), round(h*0.65,0)),
                                  v.Vec2d(round(w*0.310,0), round(h*0.73,0)),
                                  v.Vec2d(round(w*0.350,0), round(h*0.80,0)),
                                  v.Vec2d(round(w*0.400,0), round(h*0.83,0)),
                                  v.Vec2d(round(w*0.425,0), round(h*0.84,0)),
                                  v.Vec2d(round(w*0.450,0), round(h*0.85,0)),
                                  v.Vec2d(round(w*0.475,0), round(h*0.85,0)),
                                 
                                 v.Vec2d(round(w*0.500,0), round(h*0.85,0)),
                                 
                                  v.Vec2d(round(w*0.525,0), round(h*0.85,0)),
                                  v.Vec2d(round(w*0.550,0), round(h*0.85,0)),
                                  v.Vec2d(round(w*0.575,0), round(h*0.84,0)),
                                  v.Vec2d(round(w*0.600,0), round(h*0.83,0)),
                                  v.Vec2d(round(w*0.650,0), round(h*0.80,0)),
                                  v.Vec2d(round(w*0.690,0), round(h*0.73,0)),
                                  v.Vec2d(round(w*0.725,0), round(h*0.65,0)),
                                  v.Vec2d(round(w*0.745,0), round(h*0.60,0)),
                                  v.Vec2d(round(w*0.750,0), round(h*0.55,0)),
                                 
                                 v.Vec2d(round(w*0.750,0), round(h*0.50,0)),
                                 
                                  v.Vec2d(round(w*0.750,0), round(h*0.45,0)),
                                  v.Vec2d(round(w*0.745,0), round(h*0.40,0)),
                                  v.Vec2d(round(w*0.725,0), round(h*0.35,0)),
                                  v.Vec2d(round(w*0.690,0), round(h*0.27,0)),
                                  v.Vec2d(round(w*0.650,0), round(h*0.20,0)),
                                  v.Vec2d(round(w*0.600,0), round(h*0.17,0)),
                                  v.Vec2d(round(w*0.575,0), round(h*0.16,0)),
                                  v.Vec2d(round(w*0.550,0), round(h*0.15,0)),
                                  v.Vec2d(round(w*0.525,0), round(h*0.15,0)),
                                 
                                 v.Vec2d(round(w*0.500,0), round(h*0.15,0)),
                                 
                                  v.Vec2d(round(w*0.475,0), round(h*0.15,0)),
                                  v.Vec2d(round(w*0.450,0), round(h*0.15,0)),
                                  v.Vec2d(round(w*0.425,0), round(h*0.16,0)),
                                  v.Vec2d(round(w*0.400,0), round(h*0.17,0)),
                                  v.Vec2d(round(w*0.350,0), round(h*0.20,0)),
                                  v.Vec2d(round(w*0.310,0), round(h*0.27,0)),
                                  v.Vec2d(round(w*0.275,0), round(h*0.35,0)),
                                  v.Vec2d(round(w*0.255,0), round(h*0.40,0)),
                                  v.Vec2d(round(w*0.250,0), round(h*0.45,0))
                                 ]
        self.dreadnaught.position = self.dreadnaught.path[0]
        self.dreadnaught.flyToNextNavPoint() 
        
        self.ufo1 = Ufo(v.Vec2d(PygView.width, 50), v.Vec2d(-50,0))
        
        
        
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
                        
                    #if event.key == pygame.K_0:
                    #    self.nadim.target = None
                    #if event.key == pygame.K_1:
                    #    self.nadim.target = self.station1
                    #if event.key == pygame.K_2:
                    #    self.nadim.target = self.station2
                    #if event.key == pygame.K_3:
                    #    self.nadim.target = self.station3
                        
            # --------- pressed key handler --------------  
            pressedkeys = pygame.key.get_pressed() 
            
            #if pressedkeys[pygame.K_a]:
            #    self.nadim.movement.rotate(-5)
            #if pressedkeys[pygame.K_d]:
            #    self.nadim.movement.rotate(+5)
            #if pressedkeys[pygame.K_w]:
            #    self.nadim.forward(+1)
            #if pressedkeys[pygame.K_s]:
            #    self.nadim.forward(-1)
            #if pressedkeys[pygame.K_q]:
            #    self.nadim.turnfaceleft(seconds)
            #    self.nadim.facing -= 5 * -1
            #if pressedkeys[pygame.K_e]:
            #    self.nadim.turnfaceright(seconds)
            #    self.nadim.facing += 5 * -1    
            #if pressedkeys[pygame.K_SPACE]:
            #    Fragment()
                
            
            # ----- collision detection -----
            
            # -------- draw cannons ------------

            # ---------- update screen ----------- 
            self.screen.blit(self.background, (0, 0))
            
            if pressedkeys[pygame.K_y]:
                pygame.draw.circle(self.screen, (64,64,64), self.dreadnaught.rect.center, 400, 2)
            if pressedkeys[pygame.K_y]:
                pygame.draw.circle(self.screen, (64,64,64), self.dreadnaught.rect.center, 175, 2)
            if pressedkeys[pygame.K_y]:
                pygame.draw.circle(self.screen, (64,64,64), self.dreadnaught.rect.center, 150, 2)
            if pressedkeys[pygame.K_y]:
                pygame.draw.circle(self.screen, (64,64,64), self.dreadnaught.rect.center, 125, 2)
            if pressedkeys[pygame.K_y]:
                pygame.draw.circle(self.screen, (64,64,64), self.dreadnaught.rect.center, 100, 2)
            #write(self.screen, "FPS: {:6.3}  PLAYTIME:{:6.3} MINUTES:{:6.4} SECONDS".format(
            #               self.clock.get_fps(), self.playtime//60, self.playtime))
            # fahrtrichtung nadim
            #self.nadimmove = self.nadim.movement.normalized() * 5
            #pygame.draw.line(self.screen, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), 
            #                                       (self.nadim.position.x, self.nadim.position.y), 
            #                                       (self.nadim.position.x + self.nadim.movement.x * 1,
            #                                        self.nadim.position.y + self.nadim.movement.y * 1),
            #                                        10)
            
            self.allgroup.update(seconds) 
            self.allgroup.draw(self.screen)  
            pygame.display.flip()
        pygame.quit()
    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView().run()

