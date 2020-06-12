# -*- coding: utf-8 -*-
"""
Author - John Apo
Class - CPS 470
Assignment - Homework 1: Simulation of Scheduling Algorithms
Creation Date - Tuesday June 2 11:32:16 2020
Due Date - Thursday June 11 11:59:59 2020

Purpose: Study the impact for 3 scheduling algorithms First In First Out (FIFO), Shortest Job First (SJF),
and Shortest Remaining Time (SRT) on the average turnaround time of concurrent processes, via a time-based simulation
""" 

import random
import statistics 
import copy 
import matplotlib.pyplot as plt 

"""
createTable initalizes the process table used to process algorithms in this simulation

Table Indices:
0 = Process
1 = Active; indicates whether the process is currently competing for CPU
2 = Arrival Time; random int in uniform distribution from 0-k
3 = Total CPU Time; random int in Gaussian (normal) distribution with simulation parameters d & v
4 = Remaining CPU time; initialized to Total CPU Time
5 = Turnaround time 
"""

def createTable(n, k, d, v) : 
    processTable = [] # Process Table; refer to the table legend for contents

    for i in range(n): # Loops for n processes determined in main
        active = 0   # Initializes process state (1 = active)
        arrivalTime = random.randint(0, k) # Sets random arrival time (Ai)
        
        if arrivalTime == 0: 
            active = 1 # Sets process to active if arrival time is start of simulation
        CPUTime = int(random.gauss(d, v)) # Sets random Total CPU Time (Ti) from Gaussian distribution
        processTable.append([i + 1, active, arrivalTime, CPUTime, CPUTime, 0]) 
    
    return processTable 


"""
runFIFO runs the First In First Out (FIFO) scheduling algorithm
"""
def runFIFO(table, ready, running): 
    
    if running != -1: 
        first = running 
    else: 
        min = table[ready[0]][2] 
        first = ready[0] 
        for i in range(1, len(ready)): 
            if table[ready[i]][2] < min: 
                min = table[ready[i]][2] 
                first = ready[i] 
                
    return first 

"""
runSJF runs the Shortest Job First (SJF) scheduling algorithm
"""
def runSJF(table, ready, running):
    
    if running != -1:
        first = running
    else:
        shortest = table[ready[0]][3]
        first = ready[0]
        for i in range(1, len(ready)):
            if table[ready[i]][3] < shortest:
                shortest = table[ready[i]][3]
                first = ready[i]
                
    return first


"""
runSRT runs the Shortest Remaining Time (SRT) scheduling algorithm
"""
def runSRT(table, ready, running):
    shortest = table[ready[0]][4]
    first = ready[0]
    
    for i in range(1, len(ready)):
        if table[ready[i]][4] < shortest:
            shortest = table[ready[i]][4]
            first = ready[i]
            
    return first


"""
isRunning looks to see if any processes are in the running state
"""
def isRunning(remaining):
    running = False

    for i in range(len(remaining)):
        if remaining[i] > 0:
            running = True
            break
        
    return running


"""
activeProcesses returns list of current active processes
"""
def activeProcesses(newTable, t):
    currProcesses = []
    
    for i in range(len(newTable)):
        if newTable[i][1] == 1:
            currProcesses.append(i)
        elif newTable[i][2] <= t and newTable[i][5] == 0:
            newTable[i][1] = 1
            currProcesses.append(i)
            
    return currProcesses


"""
simulateOnce performs a single simulation that uses all 3 scheduling algorithms
"""
def simulateOnce(n, k, d, v):
    originalTable = createTable(n, k, d, v) # Initialize process table
    algMethods = [runFIFO, runSJF, runSRT] # Simulates the 3 scheduling algorithms
    ATT = []

    # Iterates through the 3 scheduling algorithms (FIFO, SJF, SRT)
    for i in range(len(algMethods)):
        newTable = copy.deepcopy(originalTable) # Copies original table so it can be modified

        t = 0 # Initial time = 0
        running = -1 # Var for if process is running; -1 = currently running

        # Loop for simulation
        while isRunning([sublist[4] for sublist in newTable]):
            ready = activeProcesses(newTable, t)
            t += 1
            if ready:
                running = algMethods[i](newTable, ready, running)
                newTable[running][4] -= 1
                if newTable[running][4] <= 0:
                    newTable[running][1] = 0
                    newTable[running][5] = t - newTable[running][2]
                    running = -1 # Processes are not running anymore
                    
        # Calculates the Average Turnaround Time (ATT)            
        TTs = [sublist[5] for sublist in newTable]
        ATT.append(statistics.mean(TTs))

    return ATT
  
    
"""
plotPoints graphs all 3 scheduling algorithms; taken from example in class
"""
def plotPoints(CPUAvgs, FIFO, SJF, SRT):
    
    # Plot results now
    fig, ax = plt.subplots()
    ax.set(xlabel="d", ylabel="d/ATT", 
        title="d/ATT over d for Scheduling Algorithm")
    ax.plot(CPUAvgs, FIFO, label="FIFO")
    ax.plot(CPUAvgs, SJF, label="SJF")
    ax.plot(CPUAvgs, SRT, label="SRT")
    ax.legend()
    fig.savefig("SchedulingGraph.png")
    plt.show() 
    
    return
    

"""
Main is the primary method that does everything include starting the simulation
"""
def main():
    
    # n = int(input("Enter the number of processes: ")) # Manual number of processes
    n = random.randint(0, 20); # Automated number of processes; hard-coded to cap at 20 for this simulation
    k = 1000 #  Uniform distribution max used in the arrival time;  hard-coded to 1000 for this simulation, but put to 100 to create graph for visual differentiation purposes
    CPUAvgs = [] # ds / times for plotting
    FIFO = [] # d/ATT ratios for FIFO
    SJF = [] # d/ATT ratios for SJF
    SRT = [] # d/ATT ratios for SRT

    for i in range(30):
        print("Iteration", i + 1, "of 30")
        
        # d = 10 * (i + 1)
        # d = 20 * (i + 1)
        # d = 40 * (i + 1)
        # d = 80 * (i + 1)
        d = 100 * (i + 1) # Average CPU Time; hard-coded to 100 for this simulation
        # d = 160 * (i + 1)
        # d = 320 * (i + 1)
        # d = 640 * (i + 1)
        # d = 1280 * (i + 1)
        # d = 2560 * (i + 1)
        # d = 5120 * (i + 1)
        
        v = d / 10 # Standard Deviation
        ATTs = simulateOnce(n, k, d, v)
        CPUAvgs.append(d)

        FIFO.append(d / ATTs[0])
        SJF.append(d / ATTs[1])
        SRT.append(d / ATTs[2])
        plotPoints(CPUAvgs, FIFO, SJF, SRT) # Plotted after each iteration for debugging purposes
    
    # Plots scheduling algorithms once 
    # plotPoints(CPUAvgs, FIFO, SJF, SRT)
        
    # Prints out all d/ATT values for debugging / Excel graphing purposes
    print("N processes: " + str(n))
    print("\nFIFO d/ATTs")
    print(FIFO)
    print("\nSJF d/ATTs")
    print(SJF)
    print("\nSRT d/ATTs")
    print(SRT)
    
    return
    
        
"""
Required script to run program
"""
if __name__ == "__main__":
    
    #execute only if run as a script
    main()
