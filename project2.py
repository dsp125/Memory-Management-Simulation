"""
      FILE: project2.py
      Author(s): Clarisse Baes, Dhruv Patel, Michael Savini
      RCS ID: baesc, pateld7, savinm
      
      OPERATING SYSTEMS PROJECT #2
      INST: David Goldschmidt
      DUE DATE: 4/30/2019
      COMPLETE: NO
      

Test Terminal Inputs:
    
      DESCRIPTION:
      
             - In an operating system, each process has specific memory requirements. These memory requirements
             are met (or not) based on whether free memory is available to fulfill such requirements. In this project,
             contiguous and non-contiguous memory allocation schemes will be simulated. For contiguous memory 
             allocation, a dynamic partitioning scheme will be implemented.
       
      ARGUMENTS:
      
                     - argv[1]: The first command-line argument specifies the number of frames to show on a line. The examples 
                                show 32 frames per line. Note that this value might not be a power of two.
                     - argv[2]: The second command-line argument specifies the size of the memory, i.e., how many frames 
                                make up the physical memory. The examples show a memory consisting of 256 frames. Note that 
                                this value might not be a power of two.
                     - argv[3]: The third command-line argument specifies the name of the input file to read in for your simulation
                     - argv[4]: The fourth command-line argument defines tmemmove, which is the time, in milliseconds, 
                                that it takes to move one frame of memory during defragmentation.  
"""

##CLASS AND FILE IMPORTS

import sys
import copy            #    used for deepcopy of proc list

import process        #    custom process class

## REFRESH PROC LIST

def refresh(processes):
    for proc in processes:
        proc.complete = False
        proc.countComplete = 0
        proc.active = False
        proc.start = 0

## MAIN ALGORITHM EXECUTION

def execute( inputFile, frames, frameSize, timeMove):
    procList = []
    for i in inputFile:
        if(i[len(i)-1] == '\n'):
            i = i[:len(i)-1] 
        arr = i.split(' ')
        p = process.Process()
        for j in range(len(arr)):
            if j == 0:
                p.name = arr[j]
            elif j == 1:
                p.size = int(arr[j])
            else:
                time = arr[j].split('/')
                p.arrTimes.append(int(time[0]))
                p.endTimes.append(int(time[1]))
        procList.append(p)
    
    procList_copy = copy.deepcopy(procList)

    procList_copy_1 = copy.deepcopy(procList)

    procList_copy_2 = copy.deepcopy(procList)

    FirstFit(frames, frameSize, procList, timeMove, True)
    refresh(procList)

    #processes, t_mem_move, frame_size, frame
    
    NextFit(procList_copy,timeMove, frameSize, frames)
    refresh(procList)
    
    BestFit(frames, frameSize, procList_copy_1, timeMove, False)
    refresh(procList)
    
    NonContiguous(procList_copy_2, timeMove,frameSize,  frames)

## HELPER FUNCTIONS
def print_memory(mem_arr, frame, frame_size):
    print("="* frame)
    for i in range(frame_size):
        if( ((i + 1) % frame) == 0 ):
            if (i != 0):
                print(mem_arr[i])
        elif (i == frame_size - 1):
            print(mem_arr[i])
        else:
            print(mem_arr[i], end = "")
    print("="* frame)


def defrag(processes, t_mem_move, t, mem_arr):
    move = []
    for i in range(len (mem_arr)):
        inner_loop = len(mem_arr) - i - 1
        for j in range(inner_loop):
            if (mem_arr[j] == "." and mem_arr[j+1] != "."):
                if ( mem_arr[j + 1] not in move):
                    move.append(mem_arr[ j + 1])
                temp = mem_arr[j]
                mem_arr[j] = mem_arr[j + 1]
                mem_arr[j + 1] = temp

    output_frames = ""
    for i in range(len(move)):
        output_frames += move[i]
        if (i != len(move) - 1):
            output_frames += ", "

    
    moved_frames = 0
    for process in processes:
        if process.name in move:
            moved_frames += process.size
    t += (moved_frames * t_mem_move)


    print("time " + str(t) + "ms: Defragmentation complete (moved " + str(moved_frames) + " frames: " + output_frames + ")")
    return moved_frames

def defrag_next_fit(processes, t_mem_move, t, mem_arr, curr_process_name):
    move = []
    for i in range(len (mem_arr)):
        inner_loop = len(mem_arr) - i - 1
        for j in range(inner_loop):
            if (mem_arr[j] == "." and mem_arr[j+1] != "."):
                if ( mem_arr[j + 1] not in move):
                    move.append(mem_arr[ j + 1])
                temp = mem_arr[j]
                mem_arr[j] = mem_arr[j + 1]
                mem_arr[j + 1] = temp

    output_frames = ""
    for i in range(len(move)):
        output_frames += move[i]
        if (i != len(move) - 1):
            output_frames += ", "

    
    moved_frames = 0
    for process in processes:
        if process.name in move:
            moved_frames += process.size
    if(moved_frames!= 0):
        print("time", str(t)+"ms: Cannot place process",curr_process_name, "-- starting defragmentation")
    t += (moved_frames * t_mem_move)

    if(moved_frames!=0):
        print("time " + str(t) + "ms: Defragmentation complete (moved " + str(moved_frames) + " frames: " + output_frames + ")")
    return moved_frames

def free_spots(final_process, mem_arr, pre_free_spots, post_free_spots):
    i = 0
    while i < len(mem_arr):
        if mem_arr[i] == ".":
            index = i
            num = 0
            while (mem_arr[i] == "."):
                num+=1
                i+=1
                if (i>=len(mem_arr)):
                    break

                if(i == final_process):
                    break
            temp = [index, num]
            if (index < final_process):
                pre_free_spots.append(temp)
            elif(index >= final_process):
                post_free_spots.append(temp)
            
        else:
            i+=1


def fit_check(curr_process, free_spots):
    for i in range(len(free_spots)):
        if (free_spots[i][1] >= curr_process[3]):
            return True
    return False


def place_process(cur_process, mem_arr, free_spots_pre, free_spots_post):

    found = False
    for i in range(0, len(free_spots_post)):
        if free_spots_post[i][1] >= cur_process[3]:
            found = True

            for j in range(free_spots_post[i][0], free_spots_post[i][0]+cur_process[3]):
                mem_arr[j] = cur_process[2]

            break

    if found == False:
        for i in range(0, len(free_spots_pre)):
            if free_spots_pre[i][1] >= cur_process[3]:
                found = True

                for j in range(free_spots_pre[i][0], free_spots_pre[i][0]+cur_process[3]):
                    mem_arr[j] = cur_process[2]

                break

def update(mem_arr, frame_size, cur_process):
    for i in range(len(mem_arr)):
        if (mem_arr[i-1] == cur_process[2]) and (mem_arr[i] != cur_process[2]):
            return i
    return frame_size


def set_process(cur_process, mem_Arr, pre_free_spots, post_free_spots):

    found = False
    for i in range(len(post_free_spots)):
        if post_free_spots[i][1] >= cur_process[3]:
            found = True
            for j in range(post_free_spots[i][0], post_free_spots[i][0]+cur_process[3]):
                mem_Arr[j] = cur_process[2]
            break

    if found == False:
        for i in range(len(pre_free_spots)):
            if pre_free_spots[i][1] >= cur_process[3]:
                for j in range(pre_free_spots[i][0], pre_free_spots[i][0]+cur_process[3]):
                    mem_Arr[j] = cur_process[2]

                break

def update_last(mem_arr, frame_size):
    for i in range(len(mem_arr)):
        if mem_arr[i] == ".":
            return i
    return frame_size


def clear_process(curr_process, mem_arr):
    for i in range(len(mem_arr)):
        if mem_arr[i] == curr_process[2]:
            mem_arr[i] = "."

##ALGORITHMS
def NonContiguous(processes, t_mem_move, frame_size, frame):
    print("time 0ms: Simulator started (Non-Contiguous)")
    complete = 0
    mem_arr = ["."] * frame_size
    t = 0

    while(1):
        ##CHECK FOR PROC DONE RUNNING
        for process in processes:
            if(not process.complete):
                if (t == process.endTimes[process.countComplete] + process.start):
                    if(process.active):
                        print("time " + str(t)+ "ms: Process " + str(process.name) + " removed:")
                        for j in range(len(mem_arr)):
                            if (process.name == mem_arr[j]):
                                mem_arr[j] = "."
                        process.active = False
                        process.countComplete += 1
                        if (process.countComplete == len(process.endTimes)):
                            process.complete = True
                            complete += 1
                        print_memory(mem_arr, frame, frame_size)


        ## CHECK FOR ARRIVING PROC
        for process in processes:
            if (not process.complete and (t == process.arrTimes[process.countComplete]) and not process.active):
                print("time " + str(t) + "ms: Process " + str(process.name) + " arrived (requires " + str(process.size) + " frames)" )
                count = 0
                for j in range(len (mem_arr)):
                    if (mem_arr[j] == "."):
                        count+=1
                        if (count == process.size):
                            count = 0
                            for k in range(len (mem_arr)):
                                if (mem_arr[k] == "."):
                                    count+=1
                                    mem_arr[k] = process.name
                                if (count == process.size):
                                    break
                            process.start = t
                            process.active = True
                            print("time " + str(t) + "ms: Placed process " + str(process.name) + ":")
                            print_memory(mem_arr, frame, frame_size)
                            break
                    if (j == len(mem_arr) -1):
                        process.countComplete+=1
                        if (process.countComplete == len(process.endTimes)):
                            process.complete = True
                            complete +=1
                        print("time " + str(t)+ "ms: Cannot place process " +process.name +" -- skipped!" )


        if (complete == len(processes)): # DONE WITH ALL PROCESS
            break

        t += 1

    ##EXIT SIMULATION
    print("time " + str(t) + "ms: Simulator ended (Non-Contiguous)")


def NextFit(processes, t_mem_move, frame_size, frame):
    mem_arr = ["."] * frame_size
    queue = []
    pre_free_spots = []
    post_free_spots = []
    t = 0


    for i in range(len(processes)):
        for j in range(len(processes[i].arrTimes)):
            temp = [processes[i].arrTimes[j], 2, processes[i].name, processes[i].size, processes[i]]
            queue.append(temp)

        for k in range(len(processes[i].endTimes)):
            temp = [int(processes[i].endTimes[k])+int(processes[i].arrTimes[k]), 1, processes[i].name, processes[i].size, processes[i]]
            queue.append(temp)
    queue.sort()
    final_process = 0
    free_spots(final_process, mem_arr, pre_free_spots, post_free_spots)

    print("time 0ms: Simulator started (Contiguous -- Next-Fit)")
    defrag_flag = False

    while queue != []:
        curr_process = queue[0]
        t = curr_process[0]

        if curr_process[1] == 2:
            if(defrag_flag):
                defrag_flag = False
            else:
                print("time", str(t)+"ms: Process", curr_process[2], "arrived (requires", curr_process[3], "frames)" )
            
            all_free_spots = pre_free_spots+post_free_spots
            
            fit = fit_check(curr_process,all_free_spots)

            if (fit):
                print("time", str(t)+"ms: Placed process", curr_process[2] + ":")
                set_process(curr_process, mem_arr, pre_free_spots, post_free_spots)
                print_memory(mem_arr, frame, frame_size)
                final_process = update(mem_arr, frame_size, curr_process)

                queue.pop(0)

                pre_free_spots = []
                post_free_spots = []
                free_spots(final_process, mem_arr, pre_free_spots, post_free_spots)

            else:
                sumation = 0
                all_free_spots = pre_free_spots+post_free_spots
                for i in range(len(all_free_spots)):
                    sumation += all_free_spots[i][1]
                
                if sumation >= curr_process[3]:
                    defrag_flag = True
                    # print("time", str(t)+"ms: Cannot place process", curr_process[2], "-- starting defragmentation")
                    moved_frames = defrag_next_fit(processes, t_mem_move, t, mem_arr, curr_process[2])
        
                    t = (moved_frames*t_mem_move) + t

                    for i in range(len(queue)):
                        queue[i][0] += t_mem_move*moved_frames

                    final_process = update_last(mem_arr,frame_size)
                    pre_free_spots = []
                    post_free_spots = []
                    free_spots(final_process, mem_arr, pre_free_spots, post_free_spots)

                    continue

                else:
                    print("time", str(t)+"ms: Cannot place process", curr_process[2], "-- skipped!")
                    queue.pop(0)
                    for i in range(len(queue)):
                        if curr_process[2] in queue[i]:
                            index = i
                            break
                    queue.pop(index)
        elif (curr_process[1] == 1):
            print("time", str(t)+"ms: Process", curr_process[2] + " removed:")
            clear_process(curr_process, mem_arr)
            print_memory(mem_arr, frame, frame_size)

            queue.pop(0)
            pre_free_spots = []
            post_free_spots = []
            free_spots(final_process, mem_arr, pre_free_spots, post_free_spots)

    # end simulation
    print("time", str(t)+ "ms: Simulator ended (Contiguous -- Next-Fit)\n")

def FirstFit(frame, frame_size, processes, tMemMove, contig):
    memArr = ['.']*frame_size
    time = 0
    numComplete = 0

    #Start Simulating Print Statements

    if(contig):
        print("time 0ms: Simulator started (Contiguous -- First-Fit)")
    else:
        print("time 0ms: Simulator started (Non-Contiguous)")
    while(True):
        #while process isactive
        for i in processes:
            check = not i.complete and time == i.endTimes[i.countComplete] + i.start and i.active
            if(check):
                print("time %dms: Process %s removed:" %(time, i.name))
                for j in range(len(memArr)):
                    if(memArr[j] == i.name):
                        memArr[j] = '.'
                i.countComplete += 1          
                i.active = False
                if(i.countComplete == len(i.endTimes)):
                    numComplete += 1
                    i.complete = True
                print_memory(memArr, frame, frame_size)


        #Arrival Checks
        for i in processes:
            if(not i.complete and i.arrTimes[i.countComplete] == time and not i.active):
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
                            i.active = True
                            i.start = time
                            for k in range(i.size):
                                memArr[loc+k] = i.name
                            print_memory(memArr, frame, frame_size)
                            break
                    
                    if(j == len(memArr)-1): #If At Capacity
                        if(contig and dots >= i.size): #Start Defragmentation
                            print("time %dms: Cannot place process %s -- starting defragmentation" %(time, i.name))
                            frames_moved = defrag(processes, tMemMove, time, memArr)
                            time += frames_moved*tMemMove
                            i.start = time
                            for k in processes:
                                if(not k.complete):
                                    if k.active:
                                        k.start += tMemMove*frames_moved
                                    for l in range(k.countComplete,len(k.endTimes)):
                                        k.arrTimes[l] += tMemMove*frames_moved
                            for k in range(len(memArr)):
                                if(memArr[k] == '.'):
                                    for l in range(i.size):
                                        memArr[k+l] = i.name
                                    break
                            print("time %dms: Placed process %s:" %(time, i.name))
                            print_memory(memArr, frame, frame_size)
                            i.active = True
                        else: #Can't Defragment
                            counter = 0
                            loc = 0
                            # defrag = False
                            i.countComplete += 1
                            if(i.countComplete == len(i.endTimes)):
                                numComplete += 1
                                i.complete = True
                            print("time %dms: Cannot place process %s -- skipped!" %(time, i.name))
            

        #Done with processes
        if(numComplete == len(processes)):
            break
        time += 1
        
    #Done but for real this time
    if(contig):
        print("time %dms: Simulator ended (Contiguous -- First-Fit)\n" %(time))
    else:
        print("time %dms: Simulator ended (Non-Contiguous)" %(time))

def BestFit(frame, frame_size, processes, tMemMove, contig):
    memArr = ['.']*frame_size
    time = 0
    numComplete = 0

    #begin simulation  
    print("time 0ms: Simulator started (Contiguous -- Best-Fit)")
    while(True):
        #while processes active 
        for i in processes:
            if(not i.complete and time == i.endTimes[i.countComplete] + i.start and i.active):
                print("time %dms: Process %s removed:" %(time, i.name))
                for j in range(len(memArr)):
                    if(memArr[j] == i.name):
                        memArr[j] = '.'
                i.countComplete += 1          
                i.active = False
                if(i.countComplete == len(i.endTimes)):
                    numComplete += 1
                    i.complete = True
                print_memory(memArr, frame, frame_size)
        #Checking if a process is arriving
        for i in processes:
            # print("PROCESS NAME: " + i.name + " COMPLETE: " + str(i.complete) + " ARR TIME: " + str(i.arrTimes[i.countComplete]) + " ACTIVE: " + str(i.active) + " INDEX: " + str(i.countComplete))
            if(not i.complete and i.arrTimes[i.countComplete] == time and not i.active):
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
                    i.active = True
                    i.start = time
                    for x in dots:
                        if(loc == -1):
                            loc = x
                            counters = dots[x]
                        if(dots[x] < counters):
                            loc = x
                            counters = dots[x]
                    for x in range(i.size):
                        memArr[loc+x] = i.name
                    print_memory(memArr, frame, frame_size)
                elif(num_dots >= i.size): #Defragmentation
                    print("time %dms: Cannot place process %s -- starting defragmentation" %(time, i.name))
                    framesMoved = defrag(processes, tMemMove, time, memArr)
                    time += framesMoved*tMemMove
                    i.start = time
                    for x in processes:
                        if(not x.complete):
                            if x.active:
                                x.start += tMemMove*framesMoved
                            for j in range(x.countComplete,len(x.endTimes)):
                                x.arrTimes[j] += tMemMove*framesMoved
                    for x in range(len(memArr)):
                        if(memArr[x] == '.'):
                            for j in range(i.size):
                                memArr[x+j] = i.name
                            break
                    print("time %dms: Placed process %s:" %(time, i.name))
                    print_memory(memArr, frame, frame_size)
                    i.active = True
                else: #Cant be Defragmented
                    counter = 0
                    loc = 0
                    i.countComplete += 1
                    if(i.countComplete == len(i.endTimes)):
                        numComplete += 1
                        i.complete = True
                    print("time %dms: Cannot place process %s -- skipped!" %(time, i.name))
        #All available processes are complete
        if(numComplete == len(processes)):
            break
        time += 1    
    #Completed the simulation. Congrats!
    print("time %dms: Simulator ended (Contiguous -- Best-Fit)\n" %(time))

##INPUT PARSING AND MAIN EXECUTION

if __name__ == "__main__":
    #Argument Check
    if(len(sys.argv) < 5):
        print("Invalid number of arguments provided")
        sys.exit()

    #Frame Check
    frames = sys.argv[1]
    try:
        frames = int(frames)
    except:
        print("Invalid number of frames provided (not integer)")
        sys.exit()

    #Frame Size Check
    frameSize = sys.argv[2]
    try:
        frameSize = int(frameSize)
    except:
        print("Invalid frame size provided (not integer)")
        sys.exit()

    #Infile Check
    try:
        #print(argv[3])
        inputFile = open(sys.argv[3], 'r')
    except:
        print("Input file does not exist")
        sys.exit()

    #Time for Memory Move Check
    timeMove = sys.argv[4]
    try:
        timeMove = int(timeMove)
    except:
        print("Invalid time provided for memory move (not integer)")
        sys.exit()
    
    execute(inputFile, frames, frameSize, timeMove)