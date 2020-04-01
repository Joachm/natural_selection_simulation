import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random


DIFF_EAT = 0.85

MUT_BIG = 1.1
MUT_SMALL = 0.85
DAYS = 200 
DAY_LENGTH = 40

START_POP = 10

SLOW_FACTOR = 0.

WORLD_SIZE = 40

VISUALIZE_WORLD = True
PAUSE_TIME = 0.001


START_ENERGY = 50

START_SIZE = 2
SMALL_THRES = 1.8
BIG_THRES = 2.3

SMALLEST = 0.8
BIGGEST = 5

SMALL_SPEED = 3
NORMAL_SPEED = 2
BIG_SPEED = 2

class Environment:

    def __init__(self, size):
        self.size = size
        self.world = np.zeros((size))


    def placeFood(self, numFood):
        for i in range(numFood):
            x = np.random.randint(self.size[0])
            y = np.random.randint(self.size[1])
            self.world[x,y] = -1

class Bot:

    def __init__(self, name, size):
        self.name = name
        self.startEnergy = START_ENERGY - size**SLOW_FACTOR
        self.energy = self.startEnergy  #(50-size) - size**SLOW_FACTOR
        self.size = size
        self.hunger = self.size
        self.speed = NORMAL_SPEED
        self.out  = True
        if self.size <= SMALL_THRES:
            self.speed = SMALL_SPEED
        elif self.size > BIG_THRES:
            self.speed = BIG_SPEED
        self.x = None
        self.y = None
        self.alive = True

    def getStartingPoint(self, world, wSize):
    
        self.x  = random.randint(0,wSize[0]-1)
        self.y = random.randint(0,wSize[1]-1)
        world[self.x,self.y] = START_SIZE
    
    def clip(self, wSize):
        self.x = np.clip(self.x,0, wSize[0]-1)
        self.y = np.clip(self.y,0, wSize[1]-1)

    def searchFood(self, world, wSize):
        xs = [self.x, self.x+1,self.x-1]
        ys = [self.y, self.y+1, self.y-1]
        
        xs = np.clip(xs, 0,wSize[0]-1)
        ys = np.clip(ys, 0,wSize[1]-1)

        for i in xs:
            for j in ys:
                if (world[i,j] == -1) or (world[i,j]<self.size-DIFF_EAT and world[i,j]>0):

                    coin = np.random.randint(4)
                    if i == self.x+1 and j == self.y+1:     
                        if coin == 0:
                            self.x += i - self.x
                            self.energy -= 1
                        else:
                            self.y += j - self.y
                            self.energy -=1

                    elif i == self.x+1 and j == self.y-1:     
                        if coin == 1:
                            self.x += i - self.x
                            self.energy -= 1
                        else:
                            self.y += j - self.y
                            self.energy -=1
                    
                    elif i == self.x-1 and j == self.y+1:     
                        if coin == 2:
                            self.x += i - self.x
                            self.energy -= 1
                        else:
                            self.y += j - self.y
                            self.energy -=1

                    elif i == self.x-1 and j == self.y-1:     
                        if coin == 3:
                            self.x += i - self.x
                            self.energy -= 1
                        else:
                            self.y += j - self.y
                            self.energy -=1
                    else:
                        self.x += i-self.x
                        self.y += j-self.y
                        self.energy -=1

                    self.clip(wSize)
                    return True
    
    def pickFood(self, world):
        if (world[self.x, self.y] == -1) :
            self.hunger -= np.random.uniform(0.8, 1.1)
            #print('hunger now:', self.hunger)
        elif world[self.x, self.y] < self.size-DIFF_EAT and world[self.x, self.y]>0:
            self.hunger -= 2
            #print('hunger now', self.hunger)
        
        #if self.hunger <= -:
            #self.out = False
        #    world[self.x, self.y] = 0

    def checkForDanger(self, world, wSize):
        xs = [self.x, self.x+1,self.x-1, self.x+2]#, self.x+3]
        ys = [self.x, self.y+1, self.y-1, self.y+2]#, self.y+3]
        
        xs = np.clip(xs, 0,wSize[0]-1)
        ys = np.clip(ys, 0,wSize[1]-1)

        for i in xs:
            for j in ys:
                if world[i,j]> self.size+DIFF_EAT:

                    coin = np.random.randint(4)
                    if i == self.x+1 and j == self.y+1:     
                        if coin == 0:
                            self.x += self.x - i
                            self.energy -= 2
                        else:
                            self.y += self.y-j
                            self.energy -=2

                    elif i == self.x+1 and j == self.y-1:     
                        if coin == 1:
                            self.x +=  self.x-i
                            self.energy -= 2
                        else:
                            self.y += self.y-j
                            self.energy -=2
                    
                    elif i == self.x-1 and j == self.y+1:     
                        if coin == 2:
                            self.x += self.x-i
                            self.energy -= 2
                        else:
                            self.y += self.y-j
                            self.energy -=2

                    elif i == self.x-1 and j == self.y-1:     
                        if coin == 3:
                            self.x += self.x-i
                            self.energy -= 2
                        else:
                            self.y +=self.y-j
                            self.energy -=2
                    else:
                        self.x += self.x-i
                        self.y += self.y-j
                        self.energy -=2

                    self.clip(wSize)
                    return True
 

    def checkForBots(self, world, wSize, dead):
        
        xs = [self.x+1,self.x-1]
        ys = [self.y+1, self.y-1]
        
        xs = np.clip(xs, 0,wSize[0]-1)
        ys = np.clip(ys, 0,wSize[1]-1)
        
        for i in xs:
            for j in ys:
                
                if world[i,j]> self.size+DIFF_EAT:
                    self.alive=False
                    dead.append(self.name)
                    #print('killed')
                elif world[i,j] > self.size+0.3:
                    self.energy -= 2
        


    def move(self, world, wSize, dead):
        m = np.random.randint(4)
        world[self.x,self.y] = 0
        if self.energy>0: 
            
            for step in range(self.speed): 
                
                if self.checkForDanger(world, wSize):
                    continue
                elif self.searchFood(world,wSize):
                    self.clip(wSize)
                    self.pickFood(world)
                else:
                    if m == 0:
                        self.x-= 1 
                        if self.x< 0:
                            self.x=0
                        else:
                            self.energy -= 1
                    elif m == 1:
                        self.x+= 1
                        if self.x > wSize[0]-1:
                            self.x = wSize[0]-1
                        else:
                            self.energy -= 1
                    elif m ==2:
                        self.y-=1
                        if self.y<0:
                            self.y=0
                        else:
                            self.energy -= 1
                    elif m == 3:
                        self.y+=1
                        if self.y > wSize[1]-1:
                            self.y = wSize[1]-1
                        else:
                            self.energy -= 1
                

        self.checkForBots(world, wSize, dead)
        
        self.x = np.clip(self.x, 0,wSize[0]-1)
        self.y = np.clip(self.y, 0, wSize[1]-1)

        world[self.x,self.y] = self.size
        

    def status(self, newBots, dead):
        
        
        if self.hunger < -1:
            newName = int(str(self.name)+str(np.random.randint(10)))
            newBots[newName] = self.size #Bot(newName, 100, 2,2,None,None)
            #print(newName)
        
        elif self.hunger <= -3:
            newName = int(str(self.name)+str(np.random.randint(10)))
            newName2 = int(str(self.name)+str(np.random.randint(10)))
            
            newBots[newName] = self.size
            newBots[newName2] = self.size
        
    
        elif self.hunger >= min(2,self.size):
            self.alive = False
            self.x = None
            dead.append(self.name)
            self.y = None
            

numBots = START_POP


population = [0]
sizes = []
food = [0]

foodLeft = 0
allBots = {}
for i in range(numBots):
    allBots[i] = Bot(i, 2)


for day in range(DAYS):
    if len(allBots) == 0:
        break
    print()
    print('day', day)
    env = Environment((WORLD_SIZE,WORLD_SIZE))
    numFood = random.randint(30,50)
    env.placeFood(numFood + int(foodLeft/2))
    food.append(numFood)

    dead = []

    for i in allBots.keys():
        if allBots[i].alive:
            allBots[i].out = True
            allBots[i].getStartingPoint(env.world, env.size)
            allBots[i].hunger =allBots[i].size
            allBots[i].energy = allBots[i].startEnergy 

    newBots = {}

    for time in range(DAY_LENGTH):

        if VISUALIZE_WORLD == True:
            #'''
            sns.heatmap(env.world, -1, 3, cbar=False)
            plt.title(str(day)+' '+str(time))
            plt.pause(PAUSE_TIME)
            plt.clf()
            #'''
        for i in allBots.keys():
            if allBots[i].alive and allBots[i].out:
                allBots[i].move(env.world, env.size, dead)
        

    for i in allBots.keys():
        if allBots[i].alive and allBots[i].out:
            allBots[i].status(newBots, dead)

    dead = set(dead)
    for i in dead:
        del allBots[i]

    for i in newBots.keys():
        allBots[i] = Bot(i, np.clip(newBots[i]*np.random.uniform(MUT_SMALL,MUT_BIG),SMALLEST,BIGGEST))

    print(len(newBots), 'born')
    print(len(dead), 'died')

    population.append(len(allBots))
    sizes.append([allBots[i].size for i in allBots.keys()])
    
    foodLeft = len(np.where(env.world==-1)[0])
    
plt.plot(population)
plt.plot(food)
plt.title('population size')
plt.show()

for i in range(len(sizes)):
    plt.scatter(np.full((len(sizes[i],)),i),sizes[i])
plt.title('evolution of sizes')
plt.xlabel('days')
plt.ylabel('size')
plt.show()








