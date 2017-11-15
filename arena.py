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



class Ship(pygame.sprite.Sprite):
    
    
    
    images = []
    
    def __init__(self, x=320, y=240, i=0, angle=0, dx=0, dy=0):
        """create Ship"""
        pygame.sprite.Sprite.__init__(self, self.groups) 
        self.image = Ship.images[i]
        self.image0 = Ship.images[i]
        self.i=i
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = x, y
        self._layer = 4
        self.dx = dx
        self.dy = dy
        self.rotate(angle)
        
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)


def write(background, text, x=50, y=150, color=(0,0,0),
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
        tmp = pygame.image.load(os.path.join("data","background05.jpg"))
        self.background = pygame.transform.scale(tmp, (self.width, self.height)).convert()
        Ship.images.append(pygame.image.load(os.path.join("data","links.png")).convert_alpha())
        Ship.images.append(pygame.image.load(os.path.join("data","rechts.png")).convert_alpha())
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
        
        #Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Ship.groups = self.allgroup, self.shipgroup
        
        
        #self.ball1 = Ball(x=100, y=100) # creating a Ball Sprite
        #self.ball2 = Ball(x=200, y=100) # create another Ball Sprite
        self.links = Ship(x=400, y=350, angle=270, dx=4, dy=-1, i=0)
        self.rechts = Ship(x=900, y=350, angle=90, dx=-4, dy=1, i=1) 
    
        

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
                    if event.key == pygame.K_b:
                        Ship(x=random.randint(50, 600), y=random.randint(50, 650), angle=270, i=0, dx=4, dy=-1) # add balls!
                    
                    if event.key == pygame.K_v:
                        Ship(x=random.randint(700, 1250), y=random.randint(50, 650), angle=90, i=1, dx=-4, dy=1)
            # end of event handler
           
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)           
        
            # write text over everything 
            #write(self.screen, "Press b to add another ballöÖäÄüÜß",x=self.width//2, y=250, center=True)
            # write moving text (not a Sprite)
            write(self.screen, char, x, y, color=(0,0,0))
            y += dy * seconds
            if y > PygView.height:
                x = random.randint(0, PygView.width)
                y = 0
                char = random.choice( "0123456789abcdefghijklmnopqrstuvwxyz")
                
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
