# Fantasy Name Generator URL Scrubber

# Created by Bryce Baker
# Created on 10/5/22

# Last Edited: 10/9/22

#%% Notes

## Return to list

# Gendered/Options: Deva, Githyanki, Githzerai, Goblin
# Half-Elf, Half-Orc, Harengon, Kalashtar, Lizardfolk, Loxodon, Satyr, 
# Shadar-kai, Shifter, Simic Hybrid,Tiefling, Vedalken, Wilden, Archdevil,
# Archfey, Demon lord, Giant

# Multi-Named: Centaur, Hobgoblin, Kenku, Gnoll, Hag

# Both: Deep Gnome, Dragonborn, Drow, Duergar, Dwarf, Elf, Firbolg, Gnome, 
# Goliath, Halfling, Human, Leonin, Minotaur, Orc, Tabaxi, Triton, Dragons,
# Genies, Ogre

# None: Grung, Shardmind, Beholder, Bullywug, Mind flayer, Myconid, Pixie, Treant, Troll, Troglodyte

# Source: ???

#%% Notes

#%% Imports

from urllib.request import Request, urlopen
import re
import random

import numpy as np

#%% Imports

#%% Swear List

url_SC = Request("https://www.fantasynamegenerators.com/scripts/swearCheck.js?r",  headers = {'User-Agent': 'Mozilla/5.0'})
SW = urlopen(url_SC).read().decode()
SL = re.findall("var swear=(.*?);var", SW, re.DOTALL)[-1]

swear_list = SL[2:-2].split('","')
swear_list = [each_string.capitalize() for each_string in swear_list]

#%% Swear List

#%% Functions

def mononym(url):
    
    req = Request(url,  headers = {'User-Agent': 'Mozilla/5.0'})
    website = urlopen(req).read().decode()
    
    temp0 = re.findall("var (.*?) br=", website, re.DOTALL)[-1]
    temp1 = temp0.split()
    
    name = []
    
    for i in range(len(temp1)):
        
        if i >= 9:
            
            name.append(temp1[i][7:-6].split('","'))
        
        else:
            
            name.append(temp1[i][6:-6].split('","'))
        
    return name

def checker(temp_name, used_names):
    
    if temp_name not in swear_list and temp_name not in used_names:
                
        return temp_name

def syllable_gen(syl):
    
    rng = []
    
    for j in range(len(syl)):
        
        rng.append(random.choice(syl[j]))
        
    return rng

def pattern(syllables, list_order):
    
    temp = []
    
    for k in range(len(list_order)):
        
        temp += syllables[list_order[k]]
        
    return ''.join(temp).capitalize()

def reroll(rr, syllables, random_choices):
    
    if rr[0] != rr[1]:
    
        if len(rr) == 2:
            
            while random_choices[rr[0]] == random_choices[rr[1]]:
                
                random_choices[rr[0]] = random.choice(syllables[rr[0]])
            
            return random_choices[rr[0]]
        
        elif len(rr) == 3:
            
            while random_choices[rr[0]] == random_choices[rr[1]] or random_choices[rr[0]] == random_choices[rr[2]]:
                
                random_choices[rr[0]] = random.choice(syllables[rr[0]])
                
            return random_choices[rr[0]]
            
    else:
        
        return random_choices[rr[0]]

def gens(val, total, iterator, syllables, random_choices, orders, rerolls):
    
    while val * (total / len(orders)) <= iterator <= (val + 1) * total / len(orders):
        
        random_choices[rerolls[val][0]] = reroll(rerolls[val], syllables, random_choices)
        
        if iterator + 1 >= (val + 1) * total / len(orders):
            
            val += 1
            
            return val, pattern(random_choices, orders[val - 1])

        else:
            
            return val, pattern(random_choices, orders[val])

#%% Functions

#%% Class

class name_gen:
    
    def __init__(self, source, race, gender = 'agender'):
        
        self.gender = gender
        
        if source == "dnd":
            
            self.race = "https://www.fantasynamegenerators.com/scripts/dnd%s.js" % race
            
        else:
            
            self.race = "https://www.fantasynamegenerators.com/scripts/%s.js" % race
        
    def aarakocra(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 1, 4])
        order.append([0, 1, 2, 3, 4])
        rr.append([4, 0])
        rr.append([0, 0])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def bugbears(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 3, 4])
        order.append([0, 1, 2, 3, 4])
        rr.append([4, 0])
        rr.append([0, 0])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def changelings(self, n = 10):
        
        i = 0
        nms = mononym(self.race)
        names = []
        
        order = [0, 1, 2]
        
        while i < n:
            
            rngs = syllable_gen(nms)
            
            while rngs[0] == rngs[2]:
                    
                rngs[2] = random.choice(nms[2])
            
            name = pattern(rngs, order)
            
            names.append(checker(name, names))
            i = len(names)
            
        return names
    
    def genasi(self, element = 'Fire'):
        
        element = element.capitalize()
        nms = mononym(self.race)
        
        if element == 'Fire':
        
            return nms[0]
        
        elif element == 'Water':
        
            return nms[1]
        
        elif element == 'Earth':
        
            return nms[2]
        
        elif element == 'Air':
        
            return nms[3]
        
    def kobold(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 1, 3])
        order.append([0, 1, 2, 1, 3])
        rr.append([3, 0])
        rr.append([2, 0, 3])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def locathah(self, n = 10):
        
        i = 0
        nms = mononym(self.race)
        names = []
        
        order = [0, 1, 2, 3, 4]
        
        while i < n:
            
            rngs = syllable_gen(nms)
        
            while rngs[0] == rngs[2] or rngs[2] == rngs[4]:
                
                rngs[2] = random.choice(nms[2])
                
            names.append(checker(pattern(rngs, order), names))
            i = len(names)
            
        return names
    
    def tortle(self, n = 10):
        
        i = 0
        nms = mononym(self.race)
        names = []
        
        order1 = [0, 1, 4]
        order2 = [0, 1, 2, 3, 4]
        
        while i < n:
            
            rngs = syllable_gen(nms)
            
            if i < n / 2:
                    
                while rngs[0] == "" and "" == rngs[4]:
                    
                    rngs[0] = random.choice(nms[0])
                
                name = pattern(rngs, order1)
                
            else:
                
                name = pattern(rngs, order2)
                
            names.append(checker(name, names))
            i = len(names)
            
        return names
    
    def verdan(self, n = 10):
        
        i = 0
        j = 1
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 1, 6])
        order.append([0, 1, 2, 3, 6])
        order.append([0, 1, 2, 3, 4, 5, 6])
        rr.append([0,0])
        rr.append([2, 0, 6])
        rr.append([4, 2, 6])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            
            if i <= n * 1/ 3:
                    
                while rngs[6] == "":
                    
                    rngs[6] = random.choice(nms[6])
                
                name = pattern(rngs, order[0])
                
            else:
                
                j, name = gens(j, n, i, nms, rngs, order, rr)
                
            names.append(checker(name, names))
            i = len(names)
            
        return names
    
    def warforged(self):
        
        return mononym(self.race)[0]
    
    def yuanti(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 1, 2, 4, 5])
        order.append([0, 1, 2, 1, 3, 4, 5])
        rr.append([2, 0, 5])
        rr.append([3, 2, 5])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def aasimar(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([6, 7, 8, 9, 12])
        order.append([6, 7, 8, 9, 10, 11, 12])
        order.append([0, 1, 2, 3, 5])
        order.append([0, 1, 2, 3, 4, 3, 5])
        rr.append([8, 6, 12])
        rr.append([10, 8, 12])
        rr.append([2, 0, 5])
        rr.append([4, 2, 5])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def eladrin(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        order.append([0, 1])
        rr.append([0, 0])
        
        order.append([2, 3])
        rr.append([2, 2])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def fairy(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
        
        for k in range(4):
            
            order.append([k * 2, (k * 2) + 1])
            rr.append([k * 2, k * 2])
        
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names
    
    def githyanki(self, n = 10):
        
        i = 0
        j = 0
        
        names = []
        order = []
        rr = []
        
        nms = mononym(self.race)
    
        order.append([7, 8, 9, 10, 13])
        rr.append([9, 7, 13])
        
        order.append([7, 8, 9, 10, 11, 12, 13])
        rr.append([11, 9, 13])
    
        while i < n:
            
            rngs = syllable_gen(nms)
            j, name = gens(j, n, i, nms, rngs, order, rr)
            names.append(checker(name, names))
            
            i = len(names)
            
        return names

#%% Class

#%% Dungeons and Dragons NPCs

#%%% Aarakocra

bird_person = name_gen("dnd", "Aarakocra")
bird_person = bird_person.aarakocra()

print(bird_person, '\n')

#%%% Aarakocra

#%%% Bugbears

big_gobbo = name_gen("dnd", "Bugbears")
big_gobbo = big_gobbo.bugbears()

print(big_gobbo, '\n')

#%%% Bugbears

#%%% Changelings

changers = name_gen("dnd", "Changelings")
changers = changers.changelings()

print(changers, '\n')

#%%% Changelings

#%%% Genasi

fire_elem = name_gen("dnd", "Genasi")
fire_elem = fire_elem.genasi('Fire')

water_elem = name_gen("dnd", "Genasi")
water_elem = water_elem.genasi('water')

earth_elem = name_gen("dnd", "Genasi")
earth_elem = earth_elem.genasi('earth')

air_elem = name_gen("dnd", "Genasi")
air_elem = air_elem.genasi('air')

print(fire_elem, '\n')
print(water_elem, '\n')
print(earth_elem, '\n')
print(air_elem, '\n')

#%%% Genasi

#%%% Kobold

draggo = name_gen("dnd", "Kobolds")
draggo = draggo.kobold()

print(draggo, '\n')

#%%% Kobold

#%%% Locathah

fisherson = name_gen("dnd", "Locathah")
fisherson = fisherson.locathah()

print(fisherson, '\n')

#%%% Locathah

#%%% Verdan

mys = name_gen("dnd", "Verdan")
mys = mys.verdan()

print(mys, '\n')

#%%% Verdan

#%%% Warforged

robit = name_gen("dnd", "Warforged")
robit = robit.warforged()

print(robit, '\n')

#%%% Warforged

#%%% Yuan-Ti

snerson = name_gen("dnd", "YuanTi")
snerson = snerson.yuanti()

print(snerson, '\n')

#%%% Yuan-Ti

#%%% Aasimar

angelic = name_gen("dnd", "Aasimar")
angelic = angelic.aasimar()

print(angelic, '\n')

#%%% Aasimar

#%%% Eladrin

fey_elf = name_gen("dnd", "EladrinNames")
fey_elf = fey_elf.eladrin()

print(fey_elf, '\n')

#%%% Eladrin

#%%% Fairy

fey = name_gen("dnd", "FairyNames")
fey = fey.fairy()

print(fey, '\n')

#%%% Fairy

#%%% Githyanki

space_elf1 = name_gen("dnd", "Githyanki")
space_elf1 = space_elf1.githyanki()

print(space_elf1, '\n')

#%%% Githyanki

#%% Dungeons and Dragons NPCs





















