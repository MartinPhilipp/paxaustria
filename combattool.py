import random

class Ship(object):
    
    number = 0
    book = {}
    
    def __init__(self, hp=-1, arm=-1, dmg=-1, fr=-1, att=-1, dgd=-1):
        self.number=Ship.number
        Ship.number+=1
        Ship.book[self.number]=self
        
        
        if hp == -1:
            self.hitpoints=random.randint(5,40)
        else:
            self.hitpoints=hp
        
        if arm == -1:
            self.armor=random.randint(2,13)
        else:
            self.armor=arm
            
        if dmg == -1:
            self.damage=random.randint(2,25)
        else:
            self.damage=dmg
            
        if fr == -1:
            self.firerate=random.uniform(0.4,1.2)
        else:
            self.firerate=fr
            
        if att == -1:
            self.attack=random.uniform(0.6,0.9)
        else:
            self.attack=att
        
        if dgd == -1:
            self.dodge=random.uniform(0.2,0.9)
        else:
            self.dodge=dgd  
        
    def show(self):
        txt=""
        atts=[x for x in dir(self) if not "__" in x]
        for a in atts:
            txt+="{}: {}\n".format(a, self.__getattribute__(a))
        print (txt)
        return txt


iks_vilad=Ship(hp=30, arm=13, dmg=30, fr=0.8, att=0.8, dgd=0.5)
iks_vilad.show()        
uss_napolen=Ship(hp=40, arm=13, dmg=25, fr=1.1, att=0.7, dgd=0.07)
uss_napolen.show()

def fire(attacker, defender):
    attack=random.random()
    dodge=random.random()
    print("Schuss abgefeuert!")
    if attack+attacker.attack > dodge+defender.dodge:
        print("Treffer!")
        defender.hitpoints-=attacker.damage
    else:
        print("Fehlschuss")

v_iks=0
v_uss=0
iks_hp=iks_vilad.hitpoints
uss_hp=uss_napolen.hitpoints

for x in range(1000):
    while iks_vilad.hitpoints>0 and uss_napolen.hitpoints>0:
        fire(uss_napolen, iks_vilad)
        if iks_vilad.hitpoints>0:
            fire (iks_vilad, uss_napolen)
    if uss_napolen.hitpoints>0:
        v_uss+=1
    else:
        v_iks+=1
    uss_napolen.hitpoints=uss_hp
    iks_vilad.hitpoints=iks_hp

print("results uss:{} iks:{}".format(v_uss, v_iks))
