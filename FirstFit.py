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
    
    frames_moved = 0
    for i in processes:
        if i.name in moved:
            frames_moved += i.size
    time += frames_moved*tMemMove
    print("time %dms: Defragmentation complete (moved %d frames: %s)" %(time, frames_moved, formatedString))
    return frames_moved


def main(frame, frame_size, processes, tMemMove, contig):
    memArr = ['.']*frame_size
    time = 0
    numComplete = 0

    #Start Simulating Print Statements

    if(contig):
        print("time 0ms: Simulator started (Contiguous -- First-Fit)")
    else:
        print("time 0ms: Simulator started (Non-Contiguous)")
    while(True):
        #while process is running
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

        #Arrival Checks
        for i in processes:
            if(not i.done and i.arrivalTimes[i.completed] == time and not i.running):
                print("time %dms: Process %s arrived (requires %d frames)" %(time, i.name, i.size))
                counter = 0
                loc = 0
                dots = 0
                for j in range(len(memArr)): #Can be added?
                    if(memArr[j] != '.'):
                        counter = 0
                    else:
                        if(counter == 0):
                            loc = j
                        counter += 1
                        dots += 1
                        if(counter == i.size): #Size Check
                            print("time %dms: Placed process %s:" %(time, i.name))
                            i.running = True
                            i.startTime = time
                            for k in range(i.size):
                                memArr[loc+k] = i.name
                            printMemory(frame, frame_size, memArr)
                            break
                    
                    if(j == len(memArr)-1): #If At Capacity
                        if(contig and numDots >= i.size): #Start Defragmentation
                            print("time %dms: Cannot place process %s -- starting defragmentation" %(time, i.name))
                            frames_moved = defragment(memArr, processes, time, tMemMove)
                            time += frames_moved*tMemMove
                            i.startTime = time
                            for k in processes:
                                if(not k.done):
                                    if k.running:
                                        k.startTime += tMemMove*frames_moved
                                    for l in range(k.completed,len(k.endTimes)):
                                        k.arrivalTimes[l] += tMemMove*frames_moved
                            for k in range(len(memArr)):
                                if(memArr[k] == '.'):
                                    for l in range(i.size):
                                        memArr[k+l] = i.name
                                    break
                            print("time %dms: Placed process %s:" %(time, i.name))
                            printMemory(frame, frame_size, memArr)
                            i.running = True
                        else: #Can't Defragment
                            counter = 0
                            loc = 0
                            defrag = False
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
    if(contig):
        print("time %dms: Simulator ended (Contiguous -- First-Fit)\n" %(time))
    else:
        print("time %dms: Simulator ended (Non-Contiguous)" %(time))
