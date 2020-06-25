# -*- coding: utf-8 -*-
"""
Author - John Apo
Class - CPS 470
Assignment - Homework 2: Simulation of Memory Allocation Strategies
Creation Date - Tuesday June 23 10:11:47 2020
Due Date - Thursday June 25 13:59:59 2020

Purpose: Study the performances of the memory allocation strategies first-fit, next-fit, best-fit, worst-fit 
through a series of request and release operations
""" 

import random
import copy 
import matplotlib.pyplot as plt 


"""
printMemory prints the contents of the physical memory
"""
def printMemory():
    ctr = 0
    block = 1
    
    # print(memory) # Debugging
    
    while(ctr < len(memory)):
        if(memory[ctr] > 0):
            for i in range(memory[ctr]):
                print(block)
            block += 1
        else:
            for i in range(abs(memory[ctr])):
                print("-")
        
        ctr = ctr + abs(memory[ctr])
    
    return


"""
firstFit runs the First-Fit memory allocation algorithm
"""
def firstFit(requestSize):
    full = False
    allocated = False
    ctrSearches = 0
    index = 0
    
    # print("Start of First-Fit, size is ", requestSize) # Debugging
    while(index < len(memory) and not allocated):
        ctrSearches += 1
        if(memory[index] < 0 and abs(memory[index]) >= requestSize): # Allocate memory
            allocated = insSpecificLoc(index, requestSize)
        else:
            index += abs(memory[index]) # Keep iterating through array
            
    if(not allocated):
        full = True # stop inserting memory because its full

    ffSearches[requestSize - minR] += ctrSearches
    
    # print("End of First-Fit") # Debugging
    # print(memory)
    
    return full


"""
bestFit runs the Best-Fit memory allocation algorithm
"""
def bestFit(requestSize):
    allocated = False
    full = False
    bestHole = len(memory)
    ctrSearches = 0
    insIndex = -1
    index = 0
    
    # print("Start of Best-Fit") # Debugging
    while(index < len(memory)): # Search entire length of memory for best hole to allocate memory
        ctrSearches += 1
        if(memory[index] < 0): # Find empty holes
            if(abs(memory[index]) >= requestSize): # Find empty holes with big enough size
                if(abs(memory[index]) < bestHole): # Compare to current best hole size
                    bestHole = abs(memory[index])
                    insIndex = index
        index += abs(memory[index]) # Keep iterating through array
    
    if(insIndex > -1):
        allocated = insSpecificLoc(insIndex, requestSize)
        
    if(not allocated):
        full = True # stop inserting memory because its full
        
    bfSearches[requestSize - minR] += ctrSearches
    # print("End of Best-Fit") # Debugging
    
    return full


"""
worstFit runs the Worst-Fit memory allocation algorithm
"""
def worstFit(requestSize):
    allocated = False
    full = False
    worstHole = 0
    ctrSearches = 0
    insIndex = -1
    index = 0
    
    # print("Start of Worst-Fit") # Debugging
    while(index < len(memory)): # Search entire length of memory for best hole to allocate memory
        ctrSearches += 1
        if(memory[index] < 0): # Find empty holes
            if(abs(memory[index]) >= requestSize): # Find empty holes with big enough size
                if(abs(memory[index]) > worstHole): # Compare to current best hole size
                    worstHole = abs(memory[index])
                    insIndex = index
        index += abs(memory[index]) # Keep iterating through array
    
    if(insIndex > -1):
        allocated = insSpecificLoc(insIndex, requestSize)
        
    if(allocated == False):
        full = True # stop inserting memory because its full
        
    wfSearches[requestSize - minR] += ctrSearches
    # print("End of Worst-Fit") # Debugging
    
    return full


"""
checkAllocation returns the number of allocated spaces of memory
"""
def checkAllocation():
    allocMem = 0
    
    for i in range(len(memory)):
        if(memory[i]>0):
            allocMem = allocMem + memory[i]
            
    return allocMem


"""
checkBlocks returns the number of blocks allocated
"""
def checkBlocks():
    allocBlocks = 0
    
    for i in range(len(memory)):
        if(memory[i]>0):
            allocBlocks += 1
            
    return allocBlocks


"""
checkBlockInd takes a block number and finds its index in memory to be used in freeBlock()
"""
def checkBlockInd(blockNum):
    blockCtr = 1
    retInd = 0
    
    for i in range(len(memory)):
        if(memory[i] > 0 and blockCtr == blockNum):
            retInd = i
        else:
            blockCtr += 1
            
    return retInd


"""
insertRequest inserts initial requests into the block of memory
"""
def insertRequest(loc, size):
    filled = False
    index = 0
    
    while(index < len(memory) and not filled):
        if(memory[index] < 0 and (index <= loc) and (abs(memory[index]) + index >= loc + size)):
            next = abs(memory[index]) + index
            memory[index] = index - loc
            memory[loc] = size
            memory[loc + size] = (loc + size) - next
            filled = True
        else:
            index += abs(memory[index])
    
    return filled


"""
insSpecificLoc inserts requests from each memory allocation algorithm
"""
def insSpecificLoc(loc, size):
    filled = False
    holeSize = abs(memory[loc])
    
    if(memory[loc] < 0 and abs(memory[loc]) > size): # Allocating memory into a space with extra memory
        filled = True
        memory[loc] = size # Allocate first part of space to hold data
        memory[loc + size] = -(holeSize - size) # Reallocate rest of space to be empty space
    elif(memory[loc] < 0 and abs(memory[loc]) == size): # Allocating memory into a space the exact same size
        filled = True
        memory[loc] = size
    else:
        # Do Nothing
        filled = False
    
    return filled
    

"""
freeBlock frees a block of allocated memory
"""
def freeBlock(blockIndex):
    freed = False
    prev = -1
    cur = 0
    index = 0
    
    # Find the block
    while(not freed and cur < len(memory)):
        if(blockIndex == 1): # Special case
            if(memory[cur] > 0): # No free memory before this allocated block
                if(memory[memory[cur]] > 0): # No free memory after this block
                    memory[cur] = -memory[cur] # Set it to be free
                else: # Free memory after block and coalesce
                    memory[cur] = -memory[cur] + memory[memory[cur]]
            else: # Free memory prior to allocated block
                prev = 0
                cur = abs(memory[cur])
                if((memory[cur] + cur < len(memory)) and memory[memory[cur]] > 0): # No free memory after this block
                    memory[prev] = memory[prev] - memory[cur] # Set it to be free
                elif(memory[cur] + cur < len(memory)): # Free memory after block and coalesce
                    memory[prev] = memory[prev] - memory[cur] + memory[memory[cur]]
                else:
                    memory[prev] = memory[prev] - memory[cur] # set it to be free
                    
            freed = True
        
        else: # blockIndex != 1
            while(index < blockIndex): # Search for the right set of blocks
                prev = cur
                if(memory[cur] > 0):
                    index += 1
                else:
                    # Hole -- do nothing
                 
                 if(index < blockIndex):
                    cur = cur + abs(memory[cur])
                    
            if(memory[prev] > 0): # No free memory before this allocated block
                if((memory[cur] + cur < len(memory)) and memory[memory[cur]] > 0): # No free memory after this block
                    memory[cur] = -memory[cur] # Set it to be free
                elif(memory[cur] + cur < len(memory)): # Free memory after block and coalesce
                    memory[cur] = -memory[cur] + memory[memory[cur]]
                else:
                    memory[prev] = memory[prev] - memory[cur] # Set it to be free
            else: # Free memory prior to allocated block
                if((memory[cur] + cur < len(memory)) and memory[memory[cur]] > 0): # No free memory after this block
                    memory[prev] = memory[prev] - memory[cur] # Set it to be free
                elif(memory[cur] + cur < len(memory)): # Free memory after block and coalesce 
                    memory[prev] = memory[prev] - memory[cur] + memory[memory[cur]]
                else:
                    memory[prev] = memory[prev] - memory[cur] # Set it to be free
            
            freed = True
                    
    print("Block %s freed." % (blockIndex))
    printMemory()
    
    return freed


"""
plotPoints graphs the outcomes of 3 memory allocation algorithms: First-Fit, Best-Fit, and Worst-Fit
"""
def plotPoints(rSize):
    
    # Plot results for Memory Utilization
    fig, ax = plt.subplots()
    ax.set(xlabel="d", ylabel="Memory Utilization", 
        title="Average Memory Utilization using Same Memory & Same Requests")
    ax.plot(rSize, ffUtil, label="First-Fit")
    ax.plot(rSize, bfUtil, label="Best-Fit")
    ax.plot(rSize, wfUtil, label="Worst-Fit")
    ax.legend()
    fig.savefig("UtilizationGraph.png")
    plt.show() 
    
    # Plot results for Search Times
    fig, ax = plt.subplots()
    ax.set(xlabel="d", ylabel="Search Times", 
        title="Average Search Times using Same Memory & Same Requests")
    ax.plot(rSize, ffSearches, label="First-Fit")
    ax.plot(rSize, bfSearches, label="Best-Fit")
    ax.plot(rSize, wfSearches, label="Worst-Fit")
    ax.legend()
    fig.savefig("TimeGraph.png")
    plt.show()
    
    return


"""
Main is the primary method that does everything include starting the simulation
"""
def main():
    global memory
    
    # Keeps track of the memory utilization per request size of each memory allocation algorithm
    global ffUtil
    global bfUtil 
    global wfUtil
    # Instatiate vars
    ffUtil = []
    bfUtil = []
    wfUtil = []
    
    # Keeps track of the number of holes examined by each memory allocation algorithm
    global ffSearches 
    global bfSearches
    global wfSearches
    # Instatiate vars
    ffSearches = []
    bfSearches = []
    wfSearches = []
    
    # global firstFitBlocks = [] # Number of blocks allocated in first fit
    # global bestFitBlocks = [] # Number of blocks allocated in best fit
    # global worstFitBlocks = [] # Number of blocks allocated in worst fit
    
    global minR
    minR = 2 # Minimum d value, hard-coded for simulation
    maxR = 10 # Maximum d value, hard-coded for simulation
    n = 0 # input var
    s = -1 # size var
    
    while (n < 1):
        n = int(input("Enter the physical memory size, n > 0: ")) # Manually entering physical memory size
    
    memory = [0] * n
    memory[0] = -n
    printMemory()
    
    d = int(input("Enter the average request size, d: ")) # Manually entering avg request siZe
    v = int(input("Enter the request size standard deviation, v: ")) # Manually entering std dev
    
    # Fill memory randomly to achieve ~50%
    utilNum = float(0.0)
    while(utilNum < 0.25):
        while(s < 0 or s >= n):
            s = int(random.gauss(d, v))
            
        filled = False
        
        while(not filled):
            loc = random.randint(0 , n-1)
            filled = insertRequest(loc, s)
        utilNum += float(s) / len(memory)
            
    printMemory()
    origUtil = checkAllocation()
    
    # Start of simulation
    rSize = []
    z = range(minR, maxR) # Testing different average request sizes; hard-coded for this simulation
    origMem = copy.deepcopy(memory)
    
    for i in z:
        print("Size d is ", i)
        rSize.append(i) # This is x-axis for graphing purposes
        
        # Initialize this iteration's current utilization of memory
        ffUtil.append(origUtil) 
        bfUtil.append(origUtil) 
        wfUtil.append(origUtil)
        
        # Initialize this iteration's current search amount
        ffSearches.append(0) 
        bfSearches.append(0) 
        wfSearches.append(0)
        
        # Flag when request cannot be met
        ffDone = False 
        bfDone = False
        wfDone = False
        
        memory = copy.deepcopy(origMem)
        while (ffDone == False): # Loops through First-Fit simulation until insert request cannot be met
            # randNum = random.gauss(i, v) # random sized request for more variability
            # ffDone = firstFit(randNum)
            ffDone = firstFit(i)
        # Free random block
        blocks = checkBlocks()
        randFree = random.randint(1, blocks)
        freeBlock(randFree)
        ffUtil[i - minR] = checkAllocation()
                
        memory = copy.deepcopy(origMem) # Reset memory to original values
        while(bfDone == False): # Loops through Best-Fit simulation until insert request cannot be met
            # randNum = random.gauss(i, v) # random sized request for more variability
            # bfDone = bestFit(randNum)
            bfDone = bestFit(i)
        # Free random block
        blocks = checkBlocks()
        randFree = random.randint(1, blocks)
        freeBlock(randFree)
        bfUtil[i - minR] = checkAllocation()
        
        memory = copy.deepcopy(origMem) # Reset memory to original values
        while(wfDone == False): # Loops through Worst-Fit simulation until insert request cannot be met
            # randNum = random.gauss(i, v) # random sized request for more variability
            # wfDone = worstFit(randNum)
            wfDone = worstFit(i)
        # free random block
        blocks = checkBlocks()
        randFree = random.randint(1, blocks)
        freeBlock(randFree)
        wfUtil[i - minR] = checkAllocation()
        
        # Change utilization number from spaces of allocated memory to ratio of allocated : total
        ffUtil[i-minR] = ffUtil[i-minR] / len(memory)
        bfUtil[i-minR] = bfUtil[i-minR] / len(memory)
        wfUtil[i-minR] = wfUtil[i-minR] / len(memory)
        
        plotPoints(rSize)
    
    # Print out data for debugging and exporting purposes
    print("First-Fit Utilization")
    print(ffUtil)
    print("Best-Fit Utilization")
    print(bfUtil)
    print("Worst-Fit Utilization")
    print(wfUtil)
    print("First-Fit Searches/Time")
    print(ffSearches)
    print("Best-Fit Searches/Time")
    print(bfSearches)
    print("Worst-Fit Searches/Time")
    print(wfSearches)
    return


"""
Required script to run program
"""
if __name__ == "__main__":
    
    #execute only if run as a script
    main()