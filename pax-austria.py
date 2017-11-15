import random

class Ship(object):
    number = 0
    #book={}
    starfleet_book = {}
    klingon_book = {}
    romulan_book= {}
    borg_book={}
    
    def __init__(self,):
        self.number = Ship.number
        Ship.number += 1
        #Ship.book[self.number] = self
        self.hitpoints = 2
        self.armor = 1
        self.damage = 1
        self.firerate = 1.0
        self.attack = 0.2
        self.dodge = 0.2
        self.speed = 1

    def update (self, seconds):
        pass
        
class StarfleetShip(Ship):
    
    def __init__(self):
        super(Starfleetship, self).__init__()
        Ship.starfleet_book[self.number]=self
        
class KlingonShip(Ship):
    
    def __init__(self):
        super(Klingonship, self).__init__()
        Ship.klingon_book[self.number]=self
        
class RomulanShip(Ship):
    
    def __init__(self):
        super(Romulanship, self).__init__()
        Ship.romulan_book[self.number]=self
        
class BorgShip(Ship):
    
    def __init__(self):
        super(Borgship, self).__init__()
        Ship.borg_book[self.number]=self
        
        
        
        
class Shoot(object):
    
    def __init__(self,):
        super(Shoot, self).__init__()
        self.kinetik=5
        self.laser=5
        self.damage=5

class Kinetikshoot(Shoot):
    
    def __init__(self,):
        super(Kinetikshoot, self).__init__()
        self.kinetik=5
        self.laser=0
        self.damage=5

class Lasershoot(Shoot):
    
    def __init__(self,):
        super(Lasershoot, self).__init__()
        self.kinetik=0
        self.laser=5
        self.damage=5
                
class Shield(object):
    
    def __init__(self, ):
        super(Shield, self).__init__()
        self.hitpoints=50
        self.regeneration=2  
      
class Station(Ship):
    
    def __init__(self,):
        super(Station, self).__init__()
        self.hitpoints = 1000
        self.armor = 0
        self.damage = 0
        self.firerate = 0
        self.attack = 0.0
        self.dodge = 0.00001
        self.points = 5
        self.speed = 0
        
    def update(self, seconds):
        self.points += 1
        options = []
        if self.points > 0:
            options.append("Hunter")
        if self.points > 2:
            options.append("Bomber")
        if len(options) > 0:
            answer = input("Buy?" + str(options))
            if answer == "Bomber":
                Bomber()
            if answer == "Hunter":
                Hunter()
                
class Mothership(Ship):
    
    def __init__(self,):
        super(Mothership, self).__init__()
        self.hitpoints = 800
        self.armor = 0
        self.damage = 0
        self.firerate = 0
        self.attack = 0.0
        self.dodge = 0.01
        self.points = 5
        self.speed = 1
        
    def update(self, seconds):
        self.points += 1
        options = []
        if self.points > 0:
            options.append("Hunter")
        if self.points > 2:
            options.append("Bomber")
        if len(options) > 0:
            answer = input("Buy?" + str(options))
            if answer == "Bomber":
                Bomber()
            if answer == "Hunter":
                Hunter()
               
class Battleship(Ship):
    
    def __init__(self,):
        super(Battleship, self).__init__()
        self.hitpoints = 700
        self.armor = 0
        self.damage = 0
        self.firerate = 10
        self.attack = 4.4
        self.dodge = 0.2
        self.speed = 1
    
    def update(self, seconds):
        pass

class Hunter(Ship):
    
    def __init__(self,):
        super(Hunter, self).__init__()
        self.hitpoints = 8
        self.armor = 3
        self.damage = 2
        self.firerate = 1.0
        self.attack = 0.6
        self.dodge = 0.7
        self.speed = 1
        
class MiniHunter(Ship):
    def __init__(self,):
        super(MiniHunter, self).__init__()
        self.hitpoints = 5
        self.armor = 2
        self.damage = 4
        self.firerate = 1.2
        self.attack = 0.8
        self.dodge = 0.9
        self.speed = 1

class Bomber(Ship):
    def __init__(self,):
        super(Bomber, self).__init__()
        self.hitpoints = 7
        self.armor = 3
        self.damage = 5
        self.firerate = 0.5
        self.attack = 0.6
        self.dodge = 0.3
        self.speed = 1

class MiniBomber(Ship):
    def __init__(self,  ):
        super(MiniBomber, self).__init__( )
        self.hitpoints = 8
        self.armor = 3
        self.damage = 7
        self.firerate = 0.6
        self.attack = 0.9
        self.dodge = 0.4
        self.speed = 1
        
class Paladin(Ship):
    def __init__(self,  ):
        super(PaladinM, self).__init__( )
        self.hitpoints = 15
        self.armor = 5
        self.damage = 10
        self.firerate = 0.5
        self.attack = 0.8
        self.dodge = 0.4
        self.speed = 1
                
class Frigate(Ship):
    def __init__(self,  ):
        super(Frigate, self).__init__( )
        self.hitpoints = 40
        self.armor = 13
        self.damage = 25
        self.firerate = 1.1
        self.attack = 0.75
        self.dodge = 0.07
        self.speed = 1

def fire(attacker, defender):
    attack=random.random()
    dodge=random.random()
    if attack < attacker.attack:
        print("Schuss abgefeuert!")
        if dodge < defender.dodge:
            print("Ziel ausgewichen!")
        else:
            print("Treffer!")
            defender.hitpoints-=attacker.damage
    else:
        print("Fehlschuss")
 
           
#s = Station(1)
#Hunter(1)
#Bomber(1)

#Flottenbau
StarfleetShip()
StarfleetShip()
StarfleetShip()
KlingonShip()
KlingonShip()
KlingonShip()

for x in range(Ship.number+10):
	pass
