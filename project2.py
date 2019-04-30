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
import copy			#used for deepcopy of proc list

import process		#custom process class

## REFRESH PROC LIST

def refresh(processes):
    for proc in processes:
        proc.done = False
        proc.completed = 0
        proc.running = False
        proc.startTime = 0

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
                p.arrivalTimes.append(int(time[0]))
                p.endTimes.append(int(time[1]))
        procList.append(p)
    
    '''
    for i in procList:
        print(i.name)
        for j in range(len(i.arrivalTimes)):
            print(i.arrivalTimes[j])
            print(i.endTimes[j])
    '''
    
    procList_copy = copy.deepcopy(procList)

    FirstFit(frames, frameSize, procList, timeMove, True)
    refresh(procList)
	
    NextFit(frames, frameSize, procList_copy, timeMove)
    refresh(procList)
	
    BestFit(frames, frameSize, procList, timeMove, False)
    refresh(procList)
	
    NonContiguous(frames, frameSize, procList, timeMove, False)

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
            if (mem_arr[j] == "."):
                if (mem_arr[j+1] != "."):
                    if ( mem_arr[j + 1] not in move):
                        move.append(mem_arr[ j + 1])
                    temp = mem_arr[j]
                    mem_arr[j] = mem_arr[j + 1]
                    mem_arr[j + 1] = temp

    moved_frames = 0
    for process in processes:
        if process.name in move:
            moved_frames += process.size
    t += (moved_frames * t_mem_move)

    output_frames = ""
    for i in range(len(move)):
        output_frames += move[i]
        if (i != len(moved) - 1):
            output_frames += ", "

    print("time " + str(t) + "ms: Defragmentation complete (moved " + str(moved_frames) + " frames: " + output_frames + ")")
    return moved_frames

##ALGORITHMS
def NonContiguous(processes, t_mem_move, frame_size, frame):
    print("time 0ms: Simulator started (Non-Contiguous)")
    complete = 0
    mem_arr = ["."] * frame_size
    t = 0

    while(1):
        ##CHECK FOR PROC DONE RUNNING
        for process in processes:
            if(not process.done):
                if (t == process.endTimes[process.completed] + process.startTime):
                    if(process.running):
                        print("time " + str(t)"ms: Process " + str(process.name) + " removed:")
                        for j in range(len(mem_arr)):
                            if (process.name == mem_arr[j]):
                                mem_arr[j] = "."
                        process.running = False
                        process.completed += 1
                        if (process.completed == len(process.endTimes)):
                            process.done = True
                            complete += 1
                        print_memory(mem_arr, frame, frame_size)


        ## CHECK FOR ARRIVING PROC
        for process in processes:
            if (t == process.arrivalTimes[process.completed]):
                if (not process.done):
                    if (not process.running):
                        print("time " + str(t) + "ms: Process " + str(process.name) + " arrived (requires " + str(process.size) + " frame)" )
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
                                    process.startTime = t
                                    process.running = True
                                    print("time " + str(t) + "ms: Placed process " + str(process.name) + ":")
                                    print_memory(mem_arr, frame, frame_size)


        if (complete == len (process)): # DONE WITH ALL PROCESS
            break

        t += 1

    ##EXIT SIMULATION
    print("time " + str(t) + "ms: Simulator ended (Non-Contiguous)")
                                





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
