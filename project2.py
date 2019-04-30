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
import copy			#	used for deepcopy of proc list

import process		#	custom process class

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

'''
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
    for i in range(0, len(free_spots)):
        if (free_spots[i][1] >= current_process[3]):
            return True
    return False


def place_process(cur_process, memoryArr, free_spots_pre, free_spots_post):

    found = False
    for i in range(0, len(free_spots_post)):
        if free_spots_post[i][1] >= cur_process[3]:
            found = True

            for j in range(free_spots_post[i][0], free_spots_post[i][0]+cur_process[3]):
                memoryArr[j] = cur_process[2]

            break

    if found == False:
        for i in range(0, len(free_spots_pre)):
            if free_spots_pre[i][1] >= cur_process[3]:
                found = True

                for j in range(free_spots_pre[i][0], free_spots_pre[i][0]+cur_process[3]):
                    memoryArr[j] = cur_process[2]

                break

'''
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
'''
def NextFit(processes, t_mem_move, frame_size, frame):
    mem_arr = ["."] * frame_size
    queue = []
    pre_free_spots = []
    post_free_spots = []


    for i in range(len(processes)):
        for j in range(len(processes[i].arrivalTimes)):
            temp = [processes[i].arrivalTimes[j], 2, processes[i].name, processes[i].size, processes[i]]
            queue.append(temp)

        for k in range(len(process[i].endTimes)):
            temp = [int(processes[i].endTimes[j])+int(processes[i].arrivalTimes[j]), 1, processes[i].name, processes[i].size, processes[i]]
            queue.append(temp)
    queue.sort()
    final_process = 0
    free_spots(final_process, mem_arr, pre_free_spots, post_free_spots)

    print("time 0ms: Simulator Started (Contiguous -- Next-Fit)")
    defrag_flag = False

    while queue != []:
        curr_process = queue[0]
        t = curr_process[0]

        if curr_process[1] == 2:
            if(defrag_flag):
                defrag_flag = False
            else:
                print("time", str(t)+"ms: Process", curr_process[2], "arrived (requires", curr_process[3], "frames)" )
            
            all_free_spots = free_spots_pre+free_spots_post
            
            fit = fit_check(curr_process,all_free_spots)

            if (fit):
                print("time", str(time)+"ms: Placed process", current_process[2] + ":")

            
'''



#########


def update_index(memoryArr, frameSize, current_process):

    for i in range(0, len(memoryArr)):
        if (memoryArr[i-1] == current_process[2]) & (memoryArr[i] != current_process[2]):
            return i
    return frameSize


def update_last_index(memoryArr, frameSize):
    for i in range(0, len(memoryArr)):
        if memoryArr[i] == '.':
            return i
    return frameSize


def check_for_fit(last_process, current_process, free_spots, memoryArr):
    for i in range(0, len(free_spots)):
        if (free_spots[i][1] >= current_process[3]):
            return True
    return False

def find_free_spots(memoryArr, free_spots_pre, free_spots_post, last_process):
    i = 0
    while i < len(memoryArr):

        if memoryArr[i] == ".":
            index = i

            num = 0

            while (memoryArr[i] == "."):
                num += 1
                i += 1
                if (i >= len(memoryArr)) | (i == last_process):
                    break

            if index >= last_process:
                free_spots_post.append([index, num])
            else:
                free_spots_pre.append([index, num])

        else:
            i += 1

def place_process(last_process, current_process, memoryArr, free_spots_pre, free_spots_post):

    found = False
    for i in range(0, len(free_spots_post)):
        if free_spots_post[i][1] >= current_process[3]:
            found = True

            for j in range(free_spots_post[i][0], free_spots_post[i][0]+current_process[3]):
                memoryArr[j] = current_process[2]

            break

    if found == False:
        for i in range(0, len(free_spots_pre)):
            if free_spots_pre[i][1] >= current_process[3]:
                found = True

                for j in range(free_spots_pre[i][0], free_spots_pre[i][0]+current_process[3]):
                    memoryArr[j] = current_process[2]

                break


def remove_process(current_process, memoryArr):

    for i in range(0, len(memoryArr)):
        if memoryArr[i] == current_process[2]:
            memoryArr[i] = '.'


def main(frame, frameSize, processes, tMemoryMove):

    # define data structure
    memoryArr = ['.']*frameSize
    time = 0
    free_spots_post = []
    free_spots_pre = []

    # set up queue
    process_queue = []
    for i in range(0, len(processes)):

        # process arrivals
        for j in range(0, len(processes[i].arrivalTimes)):
            process_queue.append([processes[i].arrivalTimes[j], 2, processes[i].name, processes[i].size, processes[i]])

        # process completions
        for j in range(0, len(processes[i].endTimes)):
            process_queue.append([int(processes[i].endTimes[j])+int(processes[i].arrivalTimes[j]), 1, processes[i].name, processes[i].size, processes[i]])

    process_queue.sort()
    # print(process_queue)

    # update free spots
    last_process = 0
    find_free_spots(memoryArr, free_spots_pre, free_spots_post, last_process)
    #print(free_spots)

    # start simulation
    print("time 0ms: Simulator Started (Contiguous -- Next-Fit)")
    defrag_token = False

    while len(process_queue) != 0:

        # prepare for next process
        current_process = process_queue[0]

        # increment time
        time = current_process[0]

        # welcome next process
        if current_process[1] == 2:
            if defrag_token == False:
                print("time", str(time)+"ms: Process", current_process[2], "arrived (requires", current_process[3], "frames)")
            else:
                defrag_token = False


            # print(free_spots_pre)
            # print(free_spots_post)
            # print(last_process)

            # check for fit
            fit = check_for_fit(last_process, current_process, free_spots_pre+free_spots_post, memoryArr)

            if fit == True:
                # place process
                print("time", str(time)+"ms: Placed process", current_process[2] + ":")
                place_process(last_process, current_process, memoryArr, free_spots_pre, free_spots_post)
                FirstFit.printMemory(frame, frameSize, memoryArr)
                last_process = update_index(memoryArr, frameSize, current_process)


                # current_process[4].size+=current_process[3]
                process_queue.pop(0)

                # update free spots
                free_spots_pre = []
                free_spots_post = []
                find_free_spots(memoryArr, free_spots_pre, free_spots_post, last_process)

                # print(free_spots_pre)
                # print(free_spots_post)
                # print(last_process)

            else:

                sum = 0
                free_spots = free_spots_pre + free_spots_post
                for i in range(0, len(free_spots)):
                    sum += (free_spots[i][1])

                if sum >= current_process[3]:
                    defrag_token = True
                    print("time", str(time)+"ms: Cannot place process", current_process[2], "-- starting defragmentation!")

                    framesMoved = FirstFit.defragment(memoryArr, processes, time, tMemoryMove)
                    time = (framesMoved*tMemoryMove)+time

                    for i in range(0, len(process_queue)):
                        process_queue[i][0] += tMemoryMove*framesMoved

                    last_process = update_last_index(memoryArr, frameSize)

                    # update free spots
                    free_spots_pre = []
                    free_spots_post = []
                    find_free_spots(memoryArr, free_spots_pre, free_spots_post, last_process)

                    # print(free_spots_pre)
                    # print(free_spots_post)

                    # print(process_queue)
                    # break
                    continue

                else:
                    print("time", str(time)+"ms: Cannot place process", current_process[2], "-- skipped!")
                    # print(process_queue)
                    process_queue.pop(0)
                    for i in range(0, len(process_queue)):
                        if current_process[2] in process_queue[i]:
                            index = i
                            break
                    process_queue.pop(index)
                    # print(process_queue)
                    # break



        elif current_process[1] == 1:
            print("time", str(time)+"ms: Process", current_process[2] + " removed:")

            # remove process
            remove_process(current_process, memoryArr)
            FirstFit.printMemory(frame, frameSize, memoryArr)
            # current_process[4].completed+=1

            process_queue.pop(0)

            # update free spots
            free_spots_pre = []
            free_spots_post = []
            find_free_spots(memoryArr, free_spots_pre, free_spots_post, last_process)


    # end simulation
    print("time", str(time)+ "ms: Simulator ended (Contiguous -- Next-Fit)\n")





###########






                                





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
