#!/usr/bin/python3

def printMemory(frame, frameSize, memoryArr):
    print('='*frame)
    for i in range(frameSize):
        if(((i+1)%frame == 0 and i != 0) or i == frameSize-1):
            print(memoryArr[i])
        else:
            print(memoryArr[i], end='')
    print('='*frame)

def defragment(memoryArr, processes, t, tMemoryMove):
    moved = []
    '''
    for i in range(len(memoryArr)):
        if(memoryArr[i] == '.'):
            for j in range(i,len(memoryArr)):
                if(memoryArr[j] != '.'):
                    moved.append(memoryArr[j])
    '''

    #Bubble sort by .'s
    for i in range(len(memoryArr)):
        for j in range(0,len(memoryArr)-i-1):
            if(memoryArr[j] == '.' and memoryArr[j+1] != '.'):
                if(memoryArr[j+1] not in moved):
                    moved.append(memoryArr[j+1])
                memoryArr[j], memoryArr[j+1] = memoryArr[j+1], memoryArr[j]
    
    formatedString = ''
    for i in range(len(moved)):
        if(i == len(moved)-1):
            formatedString += moved[i]
        else:
            formatedString += moved[i] + ", "
    
    framesMoved = 0
    for i in processes:
        if i.name in moved:
            framesMoved += i.size
    t += framesMoved*tMemoryMove
    print("time %dms: Defragmentation complete (moved %d frames: %s)" %(t, framesMoved, formatedString))
    return framesMoved


def main(frame, frameSize, processes, tMemoryMove, contiguous):
    memoryArr = ['.']*frameSize
    t = 0
    completed = 0

    #Simulation start
    if(contiguous):
        print("time 0ms: Simulator started (Contiguous -- First-Fit)")
    else:
        print("time 0ms: Simulator started (Non-Contiguous)")
    while(True):

        #Checking if a process is done running
        for i in processes:
            if(not i.done and t == i.endTimes[i.completed] + i.startTime and i.running):
                print("time %dms: Process %s removed:" %(t, i.name))
                for j in range(len(memoryArr)):
                    if(memoryArr[j] == i.name):
                        memoryArr[j] = '.'
                i.completed += 1          
                i.running = False
                if(i.completed == len(i.endTimes)):
                    completed += 1
                    i.done = True
                printMemory(frame, frameSize, memoryArr)

        #Checking if a process is arriving
        for i in processes:
            if(not i.done and i.arrivalTimes[i.completed] == t and not i.running):
                print("time %dms: Process %s arrived (requires %d frames)" %(t, i.name, i.size))
                count = 0
                location = 0
                numDots = 0
                for j in range(len(memoryArr)): #Checking if it can be added
                    if(memoryArr[j] != '.'):
                        count = 0
                    else:
                        if(count == 0):
                            location = j
                        count += 1
                        numDots += 1
                        if(count == i.size): #Enough space for process
                            print("time %dms: Placed process %s:" %(t, i.name))
                            i.running = True
                            i.startTime = t
                            for k in range(i.size):
                                memoryArr[location+k] = i.name
                            printMemory(frame, frameSize, memoryArr)
                            break
                    
                    if(j == len(memoryArr)-1): #Not enought space
                        if(contiguous and numDots >= i.size): #Eligible for defragmentation
                            print("time %dms: Cannot place process %s -- starting defragmentation" %(t, i.name))
                            framesMoved = defragment(memoryArr, processes, t, tMemoryMove)
                            t += framesMoved*tMemoryMove
                            i.startTime = t
                            for k in processes:
                                if(not k.done):
                                    if k.running:
                                        k.startTime += tMemoryMove*framesMoved
                                    for l in range(k.completed,len(k.endTimes)):
                                        #k.endTimes[l] += tMemoryMove*framesMoved
                                        k.arrivalTimes[l] += tMemoryMove*framesMoved
                            for k in range(len(memoryArr)):
                                if(memoryArr[k] == '.'):
                                    for l in range(i.size):
                                        memoryArr[k+l] = i.name
                                    break
                            print("time %dms: Placed process %s:" %(t, i.name))
                            printMemory(frame, frameSize, memoryArr)
                            i.running = True
                        else: #Not eligible for defragmentation
                            count = 0
                            location = 0
                            defragged = False
                            i.completed += 1
                            if(i.completed == len(i.endTimes)):
                                completed += 1
                                i.done = True
                            print("time %dms: Cannot place process %s -- skipped!" %(t, i.name))
            

        #All processes completed
        if(completed == len(processes)):
            break

        #Increment time
        t += 1
        
    #Simulation is over
    if(contiguous):
        print("time %dms: Simulator ended (Contiguous -- First-Fit)\n" %(t))
    else:
        print("time %dms: Simulator ended (Non-Contiguous)" %(t))
