import numpy as np
import random
from IPython import display
import time
import os

class space:
    def __init__(self, stype,dimension):
        self.space_type = stype
        self.n = dimension
    def __repr__(self):
        return(''.join([self.space_type,'(',str(self.n),')']))

def chunks(l, n):
    result = []
    for i in range(0, len(l), n):
        result.append( l[i:i + n])
    return(result)

def showLine(txt,width = 64,wall = '|'):
    n = width - 4 
    if len(txt)>n:
        txt = txt[0:n]
    front = round((n-len(txt))/2)
    end = n-front -len(txt)
    print(wall+' '+' '*front+txt+' '*end+' '+wall)

def screen(txtList,height = 20,width = 64,roof = '=',wall = '|'):
    os.system('cls' if os.name == 'nt' else 'clear')
    n = width - 4
    m = height -4
    if len(txtList)>m:
        txtList = txtList[0:m]
    front = round((m-len(txtList))/2)
    end = m-front -len(txtList)
    print(roof*width)
    for i in range(front+1):
        print(wall,' '*n,wall)
    for txt in txtList:
        showLine(txt,width  = width,wall = wall)
    for i in range(end+1):
        print(wall,' '*n,wall)
    print(roof*width)

class player:
    def __init__(self,name = 'Robot'):
        self.name = name
        self.ki = 0 
        self.score = 0

    def gatherKi(self):
        if self.ki <3:
            self.ki = self.ki+1
            
    def attack(self):
        if self.ki>0:
            self.ki = self.ki-1

    def win(self):
        self.score =  self.score +1

    def reset(self):
        self.ki = 0
#         self.score = 0

class aGame:
                
    def __init__(self,name1='Robot',name2='Xiaoli Hu'):
        self.observation_space = space('Discrete',16)
        self.action_space = space('Discrete',3)
        self.P1 = player(name = name1)
        self.P2 = player(name = name2)
        self.score = 0
        self.observation = 0
        self.table = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])-1
        self.reward = [0,0]
        self.done = False
        self.info = 'HAHAHAHA'
        self.actionNames = ['GATHERS KI','ATTACKS','DEFEND']
#         self.actionNames = ['攒气','攻击','防御']
        self.a1 = 2
        self.a2 = 2
        
    
    def reset(self):
        self.P1.reset()
        self.P2.reset()
        self.updateObservation()
        self.observation = [0,0]
        self.reward = [0,0]
        self.done = False
        return(self.observation)
    
    def updateObservation(self):
        self.observation = [self.table[self.P1.ki,self.P2.ki],self.table[self.P2.ki,self.P1.ki]]
    
    def step(self,a1,a2):
        if self.P1.ki ==0 and a1 ==1:
            a1 = 2
        if self.P2.ki ==0 and a2 ==1:
            a2 = 2
        self.a1 = a1
        self.a2 = a2
        self.reward = [0,0]
        if not self.done:
            # ATTACK VS KI
            if a1 == 0:
                #if np.random.rand()>0.0:
                self.P1.gatherKi()
                    
                if a2 == 1:
                    self.reward = [-1,1]
                    self.done = True
                    self.info = ['Player '+self.P2.name+' '+self.actionNames[self.a2]+' and '+' wins!']
                    self.P2.win()

            if a2 == 0:
                #if np.random.rand()>0.0:
                self.P2.gatherKi()
                    
                if a1 == 1:
                    self.reward = [1,-1]
                    self.done = True
                    self.info = ['Player '+self.P1.name+ ' '+self.actionNames[self.a1]+' and '+' wins!']
                    self.P1.win()
            
            #KI BURST
            if a1 ==2 and a2==1 and self.P2.ki==3:
                self.reward = [-1,1]
                self.done = True
                self.info = ['Ki Burst!!','Player '+self.P2.name+ ' '+self.actionNames[self.a2]+' and '+' wins!']
                self.P2.win()

            if a1 ==1 and a2==2 and self.P1.ki==3:
                self.reward = [1,-1]
                self.done = True
                self.info = ['Ki Burst!!','Player '+self.P1.name+ ' '+self.actionNames[self.a1]+' and '+' wins!']
                self.P1.win()
                
            #DOUBLE ATTACKS
            if a1 == 1 and a2 ==1:
                if self.P1.ki == 3 and self.P2.ki <3:
                    self.reward = [1,-1]
                    self.done = True
                    self.info = ['Ki Burst!!','Player '+self.P1.name+ ' '+self.actionNames[self.a1]+' and '+' wins!']
                    self.P1.win()
                if self.P2.ki == 3 and self.P1.ki <3:
                    self.reward = [-1,1]
                    self.done = True
                    self.info = ['Ki Burst!!','Player '+self.P2.name+ ' '+self.actionNames[self.a2]+' and '+' wins!']
                    self.P2.win()
                    
            #PENALIZE ATTACK
            if a1 == 1:
                self.P1.attack()
            if a2 == 1:
                self.P2.attack()
                
        self.updateObservation()
                
        return self.observation,self.reward,self.done,self.info
    
    def render(self):
        if self.done:
            screen(self.info)
        else:
            screen(['XXXX A weird Game XXXX',' ',
                    self.P1.name+' '+self.actionNames[self.a1],' ',
                    '===========================================', ' ',
                    self.P1.name+' Ki: ['+'*'*self.P1.ki+'-'*(3-self.P1.ki)+']',' ',
                    self.P2.name+' Ki: ['+'*'*self.P2.ki+'-'*(3-self.P2.ki)+']',' ',
                    '===========================================',' ',
                    self.P2.name+' '+self.actionNames[self.a2],' ',
                   '[1]GATHER Ki  [2]ATTACK  [3]DEFEND  [4]Exit Game'])