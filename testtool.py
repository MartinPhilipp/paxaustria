import random

class Ship(object):
    number = 0
    #book = {}
    federation_book = {}
    klingon_book = {}
    romulan_book = {}
    borg_book ={}

    
    def __init__(self):
        self.number = Ship.number
        Ship.number += 1
        #Ship.book[self.number] = self
        self.hitpoints = 2
        self.armor = 1
        self.damage = 1
        self.firerate = 1
        self.attack = 0.2
        self.dodge = 0.2
        
      

    def update (self, seconds):
        pass

class FederationShip(Ship):
	
	def __init__(self):
		super(FederationShip, self).__init__() # ruft die Ship.__init__ auf
		Ship.federation_book[self.number] = self
		
class KlingonShip(Ship):
	
	def __init__(self):
		super(KlingonShipShip, self).__init__() # ruft die Ship.__init__ auf
		Ship.klingon_book[self.number] = self
		
class RomulanShip(Ship):
	
	def __init__(self):
		super(RomulanShip, self).__init__() # ruft die Ship.__init__ auf
		Ship.romulan_book[self.number] = self		
		
class BorgShip(Ship):
	
	def __init__(self):
		super(BorgShip, self).__init__() # ruft die Ship.__init__ auf
		Ship.borg_book[self.number] = self		
		
		
		

class Shoot(object):
	
	def __init__(self, party=1):
		super(Shoot, self).__init__(party)
		self.kinetik=5
		self.laser=5
		self.damage=5

class Kinetikshoot(Shoot):
	
	def __init__(self, party):
		super(Kinetikshoot, self).__init__(party)
		self.kinetik=5
		self.laser=0
		self.damage=5

class Lasershoot(Shoot):
	
	def __init__(self, party):
		super(Lasershoot, self).__init__(party)
		self.kinetik=0
		self.laser=5
		self.damage=5
				
class Shield(object):
	
	def	__init__(self, party=1):
		super(Shield, self).__init__(party)
		self.hitpoints=50
		self.regeneration=2  
	  
   

class Kinetikshoot(Shoot):
    
    def __init__(self, party):
        super(Kinetikshoot, self).__init__(party)
        self.kinetik=5
        self.laser=0
        self.damage=5

class Lasershoot(Shoot):
    
    def __init__(self, party):
        super(Lasershoot, self).__init__(party)
        self.kinetik=0
        self.laser=5
        self.damage=5
                
class Shield(object):
    
    def __init__(self, party=1):
        super(Shield, self).__init__(party)
        self.hitpoints=50
        self.regeneration=2  

class Alien(Ship):
    
    def __init__(self, party=5):
        self.party=party
        self.number=Ship.number
        Ship.number+=1
        Ship.aliens[self.number]=self
        self.hitpoints=2
        self.armor = 1
        self.damage=1
        self.firerate=0.1
        self.attack=0.2
        self.dogde=0.2
      

class Station(Ship):
    
    def __init__(self, party):
        super(Station, self).__init__(party)
        self.hitpoints = 1000
        self.armor = 1
        self.damage = 0
        self.firerate = 0
        self.attack = 0.0
        self.dodge = 0.00001
        self.points = 5
        
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
                Bomber(self.party)
            if answer == "Hunter":
                Hunter(self.party)
                
class Mothership(Ship):
    
    def __init__(self, party):
        super(Mothership, self).__init__(party)
        self.hitpoints = 800
        self.armor = 1
        self.damage = 0
        self.firerate = 0
        self.attack = 0.0
        self.dodge = 0.01
        self.points = 5
        
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
                Bomber(self.party)
            if answer == "Hunter":
                Hunter(self.party)
               

class Mothershipbattery(Ship):
    def __init__(self, party):
        super(Mothershipbattery, self).__init__(party)
        self.hitpoints = 60
        self.damage = 25
        self.firerate = 0.6
        self.attack = 0.8
        self.dodge = 0.01
                
class Battleship(Ship):
    
    def __init__(self, party):
        super(Battleship, self).__init__(party)
        self.hitpoints = 700
        self.armor = 1
        self.damage = 0
        self.firerate = 10
        self.attack = 4.4
        self.dodge = 0.2
    
    def update(self, seconds):
        pass

class Hunter(Ship):
    
    def __init__(self, party):
        super(Hunter, self).__init__(party)
        self.hitpoints = 8
        self.armor = 1
        self.damage = 2
        self.firerate = 1.0
        self.attack = 0.6
        self.dodge = 0.7
        
class MiniHunter(Ship):
    def __init__(self, party):
        super(MiniHunter, self).__init__(party)
        self.hitpoints = 5
        self.armor = 1
        self.damage = 4
        self.firerate = 1.2
        self.attack = 0.8
        self.dodge = 0.9

class Bomber(Ship):
    def __init__(self, party):
        super(Bomber, self).__init__(party)
        self.hitpoints = 10
        self.armor = 1
        self.damage = 5
        self.firerate = 0.5
        self.attack = 0.9
        self.dodge = 0.4

class MiniBomber(Ship):
    def __init__(self, party):
        super(MiniBomber, self).__init__(party)
        self.hitpoints = 8
        self.armor = 1
        self.damage = 7
        self.firerate = 0.6
        self.attack = 0.9
        self.dodge = 0.4
        
class PaladinM(Ship):
    def __init__(self, party):
        super(PaladinM, self).__init__(party)
        self.hitpoints = 15
        self.armor = 1
        self.damage = 10
        self.firerate = 0.5
        self.attack = 0.8
        self.dodge = 0.4

class PaladinS(Ship):
    def __init__(self, party):
        super(PaladinS, self).__init__(party)
        self.hitpoints = 25
        self.armor = 1
        self.damage = 12
        self.firerate = 0.4
        self.attack = 0.8
        self.dodge = 0.2
                
class Frigate(Ship):
    def __init__(self, party):
        super(Frigate, self).__init__(party)
        self.hitpoints = 40
        self.armor = 1
        self.damage = 25
        self.firerate = 1.1
        self.attack = 0.75
        self.dodge = 0.07

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

# flotten erschaffen

FederationShip()
FederationShip()
FederationShip()
KlingonShip()
KlingonShip()
KlingonShip()


for x in range(Ship.number+1):
    # weitermachen, multi-party-battles
       
        
