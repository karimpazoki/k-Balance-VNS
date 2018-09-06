import random
import time
import numpy as np
import math

N = 50
M = 10
P = 6

kmax = min(P,20)
kmin = 2


'''  Inital potential points and clients  '''
Servers = set()
while len(Servers) < M :
    Servers.add((round(random.random()*100,3),round(random.random()*100,3)))
#Servers  = list(Servers)

Clients  = set()
while len(Clients) < N :
    Clients.add((round(random.random()*100,3),round(random.random()*100,3)))
#Clients  = list(Clients)


'''  Generate random solution for begining  '''
Solution = set(random.sample(set(Servers), P))

#print(Servers)
#print(Clients)
#print(Solution)



'''  Convert lists to numpy arrays'''
#Servers  = np.asarray(Servers)
#Clients  = np.asarray(Clients)
#Solution = np.asarray(Solution)


'''  take two point and calculate distance between theme '''
def Len(a, b):
    return round(math.sqrt(((a[0] - b[0])**2)+((a[1] - b[1])**2)),3)


'''  calculate Congestion delay on server 'a' '''
def Congestion(a,X):
    count = 0
    for i in Clients:
        minLen = Len(i,a)
        count += 1 
        for j in X:
            if Len(i,j) < minLen :
                count -= 1
                break;
    return count
    
'''  Find the max server  '''    
def findMax(X):
    Fmax = -1
    for a in X:
        if Congestion(a,X) > Fmax:
            Fmax = Congestion(a,X)
    return Fmax


'''  Find the min server '''
def findMin(X):
    Fmin = math.inf
    for a in X:
        if Congestion(a,X) < Fmin:
            Fmin = Congestion(a,X)
    return Fmin


'''  Calculate the diffrence between max and min server '''    
def BAL(X):
    return findMax(X) - findMin(X)


def LS1(X):
    Fmax = findMax(X)
    neighborPotential = Servers - X
    FmaxList = [x for i, x in enumerate(X) if Congestion(x,X) == Fmax]
    Ls1Neighborhood = []
    for i in FmaxList:
        I = set()
        I.add(i)
        R = set()
        for j in neighborPotential:
            R = X-I
            R.add(j)
            #print(R)
            Ls1Neighborhood.append(R)
        #print(Ls1Neighborhood)
        #time.sleep(20)
        
    return Ls1Neighborhood
    
            
def LS2(X):
    Fmin = findMin(X)
    neighborPotential = Servers - X
    FminList = [x for i, x in enumerate(X) if Congestion(x,X) == Fmin]
    Ls2Neighborhood = []
    for i in FminList:
        I = set()
        I.add(i)
        R = set()
        for j in neighborPotential:
            R = X-I
            R.add(j)
            Ls2Neighborhood.append(R)
    return Ls2Neighborhood


def LS3(X):
    Fmax = findMax(X)
    Fmin = findMin(X)
    FminList = [x for i, x in enumerate(X) if Congestion(x,X) == Fmin]
    FmaxList = [x for i, x in enumerate(X) if Congestion(x,X) == Fmax]
    Ls3Neighborhood = []
    neighborPotential = Servers - X
    print(set(FminList))
    L3 = X - set(FminList)
    L3 = L3 - set(FmaxList)
    for i in L3:
        I = set()
        I.add(i)
        R = set()
        for j in neighborPotential:
            R = X-I
            R.add(j)
            Ls3Neighborhood.append(R)
            Ls3Neighborhood.append(R)
    return Ls3Neighborhood
    

def findAllNeighbor(X):
    Neighbors = []
    Neighbors.append(LS1(X))
    if len(Neighbors) > 0:
        return Neighbors
    Neighbors.union(LS2(X))
    if len(Neighbors) > 0:
        return Neighbors
    Neighbors.union(LS3(X))
    if len(Neighbors) > 0:
        return Neighbors    
    return False


def bestNeighbor(X):
    Neighbors = findAllNeighbor(X)
    #print (Neighbors)
    #time.sleep(20)
    bestNeighbor = Neighbors[0]
    A=[{1,2},{3,4},{1,5}]
# print(list(map(list, A)))
    print(list(map(list,Neighbors)))
    #(bestNeighbor)
    time.sleep(20)
    for a in Neighbors:
        if BAL(a) < BAL(bestNeighbor):
            bestNeighbor = a
    return bestNeighbor


def NeighbourhoodChange(X, Xprime , k):
    if BAL(Xprime) < BAL(X):
        Xprime = X
        k = 1
    else:
        k = k+1


def VND(X, kmax):
    i =1
    while i > 0:
        k = 1
        while True:
            Xprime = bestNeighbor(X)
            print(Xprime)
            time.sleep(20)
            if Xprime == False:
                return
            NeighbourhoodChange(X, Xprime, k)
            if k == kmax:
                break
        i = i+1
        print(i)
    return X


'''
Function NeighbourhoodChange(x, x' , k);
    if f(x') < f(x) then
        x' ← x ;
        k ← 1 /* Make a move */;
    else
        k ← k + 1 /* Next neighborhood */;
    end


Function VND(x, kmax);
    repeat
        k ← 1;
        repeat
            x' ← arg miny∈Nk(x) f(x) /* Find the best neighbor in Nk (x) */;
            NeighbourhoodChange(x, x' , k) /* Change neighbourhood */;
        until k = kmax;
    until no improvement is obtained;
'''

VND(Solution , kmax)
 
 
 
 
 
 
 
 
 