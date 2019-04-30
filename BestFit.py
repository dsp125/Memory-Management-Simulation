#!/usr/bin/python3

def printMemory(frame, frame_size, memArr):
    print('='*frame)
    for i in range(frame_size):
        if(((i+1)%frame == 0 and i != 0) or i == frame_size-1):
            print(memArr[i])
        else:
            print(memArr[i], end='')
    print('='*frame)

def defragment(memArr, processes, time, tMemMove):
    moved = []
    '''
    for i in range(len(memArr)):
        if(memArr[i] == '.'):
            for j in range(i,len(memArr)):
                if(memArr[j] != '.'):
                    moved.append(memArr[j])
    '''

    #Bubble sort by .'s
    for i in range(len(memArr)):
        for j in range(0,len(memArr)-i-1):
            if(memArr[j] == '.' and memArr[j+1] != '.'):
                if(memArr[j+1] not in moved):
                    moved.append(memArr[j+1])
                memArr[j], memArr[j+1] = memArr[j+1], memArr[j]
    
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
    time += framesMoved*tMemMove
    print("time %dms: Defragmentation complete (moved %d frames: %s)" %(time, framesMoved, formatedString))
    return framesMoved


def main(frame, frame_size, processes, tMemMove, contiguous):
    memArr = ['.']*frame_size
    time = 0
    numComplete = 0

    #Simulation start
    print("time 0ms: Simulator started (Contiguous -- Best-Fit)")
    while(True):

        #Checking if a process is done running
        for i in processes:
            if(not i.done and time == i.endTimes[i.completed] + i.startTime and i.running):
                print("time %dms: Process %s removed:" %(time, i.name))
                for j in range(len(memArr)):
                    if(memArr[j] == i.name):
                        memArr[j] = '.'
                i.completed += 1          
                i.running = False
                if(i.completed == len(i.endTimes)):
                    numComplete += 1
                    i.done = True
                printMemory(frame, frame_size, memArr)

        #Checking if a process is arriving
        for i in processes:
            if(not i.done and i.arrivalTimes[i.completed] == time and not i.running):
                print("time %dms: Process %s arrived (requires %d frames)" %(time, i.name, i.size))
                counter = 0
                dots = {}
                loc = 0
                num_dots = 0
                for j in range(len(memArr)): #Checking if it can be added
                    if(memArr[j] != '.'):
                        counter = 0
                    else:
                        if(counter == 0):
                            loc = j
                        counter += 1
                        num_dots += 1
                        if(counter >= i.size): #Enough space for process
                            dots[loc] = counter

                if(len(dots) > 0):
                    loc = -1
                    counters = 0
                    print("time %dms: Placed process %s:" %(time, i.name))
                    i.running = True
                    i.startTime = time
                    for x in dots:
                        if(loc == -1):
                            loc = x
                            counters = dots[x]
                        if(dots[x] < counters):
                            loc = x
                            counters = dots[x]
                    for x in range(i.size):
                        memArr[loc+x] = i.name
                    printMemory(frame, frame_size, memArr)
                elif(num_dots >= i.size): #Defragmentation
                    print("time %dms: Cannot place process %s -- starting defragmentation" %(time, i.name))
                    framesMoved = defragment(memArr, processes, time, tMemMove)
                    time += framesMoved*tMemMove
                    i.startTime = time
                    for x in processes:
                        if(not x.done):
                            if x.running:
                                x.startTime += tMemMove*framesMoved
                            for j in range(x.completed,len(x.endTimes)):
                                x.arrivalTimes[j] += tMemMove*framesMoved
                    for x in range(len(memArr)):
                        if(memArr[x] == '.'):
                            for j in range(i.size):
                                memArr[x+j] = i.name
                            break
                    print("time %dms: Placed process %s:" %(time, i.name))
                    printMemory(frame, frame_size, memArr)
                    i.running = True
                else: #Cant be Defragmented
                    counter = 0
                    loc = 0
                    i.completed += 1
                    if(i.completed == len(i.endTimes)):
                        numComplete += 1
                        i.done = True
                    print("time %dms: Cannot place process %s -- skipped!" %(time, i.name))
            

        #All processes completed
        if(numComplete == len(processes)):
            break

        #Increment time
        time += 1
        
    #Simulation is over
    print("time %dms: Simulator ended (Contiguous -- Best-Fit)\n" %(time))
