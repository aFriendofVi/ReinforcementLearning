
# coding: utf-8

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import random
from IPython import display
import time
import pickle
import os
float_formatter = lambda x: "%.4f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})
pd.options.display.float_format = '{:20,.3f}'.format


from AGame import *

# In[5]:

def getP(C):
    P = C/np.sum(C,axis=2)[:,:,np.newaxis]
    return(P)


userName  = input('Tell me your name...and your soul!')

while len(userName) == 0:
    userName = input('...OK, Only name?')

    
# In[ ]:
env = aGame(name2 = userName)
V = np.zeros(env.observation_space.n)
C = np.zeros([env.action_space.n,env.observation_space.n,env.observation_space.n])+0.01
R = np.zeros([env.action_space.n,env.observation_space.n,env.observation_space.n])
Pi = np.random.randint(env.action_space.n,size = (env.observation_space.n))
P = getP(C)
# P = np.zeros([env.observation_space.n,env.observation_space.n,])+1/(env.observation_space.n)
# V0List = []



try:
    f = open('train_'+userName+'.pickle','rb') 
    V, C, P, R, Pi, rationality = pickle.load(f)
    f.close()
    rationality = min(0.9,rationality)
except FileNotFoundError:
    # if new player
    f = open('train.pickle','rb')
    V, C, P, R, Pi ,rationality= pickle.load(f)
    f.close()
    rationality = 0.5
    C= C/np.max(C)*10



# In[6]:

#f = open('train.pickle','rb') 
#V, C, P, R, Pi = pickle.load(f)
#f.close()


# In[11]:

episodeMax = 1000
gamma = 0.99
done = False
weight = 0.50

rList = []
avgRList = []
flag = True

score = [0,0]
reward = [0,0]

for episode in range(episodeMax):
    rationality += 0.1
    score[0] = score[0]+ max(0,reward[0])
    score[1] = score[1]+ max(0,reward[1])
    display.clear_output(wait=True)
    print('Episode ',episode+1)
    state = env.reset()
    done = False
#     V0List.append(V[0])
    while not done:
        display.clear_output(wait=True)
        print('You have won '+str(score[1])+' out of '+str(score[0]+score[1])+'!')
        env.render()
        statePre = state
        if np.random.rand()<rationality:
            a1 = Pi[statePre[0]]
        else:
            a1 = np.random.randint(3)
            
        raw = input('What is your move?: ')

        while raw not in ['1','2','3','4'] or raw == None:
            raw = input('Please choose from 1-4: ')
            
        a2 = int(raw)-1
        if a2 == 3:
            exit()
        
        if env.P1.ki ==0 and a1 ==1:
            a1 = 2
            
        if env.P2.ki ==0 and a2 ==1:
            a1 = 2
        
        state,reward,done,info = env.step(a1,a2)
        display.clear_output(wait=True)
        env.render()
#         time.sleep(0.3)
        R[a1,statePre[0],state[0]] =  R[a1,statePre[0],state[0]]*(1-weight) + reward[0]*weight
        R[a2,statePre[1],state[1]] =  R[a2,statePre[1],state[1]]*(1-weight) + reward[1]*weight
        C[a1,statePre[0],state[0]] += 0.5
        C[a2,statePre[1],state[1]] += 0.5
        P = getP(C)
        
        # evaluate the current policy
        V[statePre[0]] = V[statePre[0]]*(1-weight)+(weight)*np.dot(P[a1,statePre[0],:],(R[a1,statePre[0],:]+V*gamma).T)
        V[statePre[1]] = V[statePre[1]]*(1-weight)+(weight)*np.dot(P[a2,statePre[1],:],(R[a2,statePre[1],:]+V*gamma).T)
        
        # improve policy
#         QBest = V
        Qsa =np.einsum('ijk,ijk->ji',P[:,:,:],R[:,:,:]+V[np.newaxis,np.newaxis,:]*gamma)
        Pi = np.argmax(Qsa+0.1*np.random.rand(env.observation_space.n,env.action_space.n),axis = 1)
        
        if done:
            x = input('Press anykey to start a new game or Ctrl+C to exit.')

    # Saving the train result
    f = open('train_'+userName+'.pickle', 'wb')  
    pickle.dump([V, C, P, R, Pi, rationality], f)
    f.close()




# In[ ]:

V.reshape(4,4)

