#!/usr/bin/python3
import sys
import process
import FirstFit


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

            # print(free_spots_pre)
            # print(free_spots_post)

            # update last process
            # last_process = update_last_index(last_process, memoryArr)


    # end simulation
    print("time", str(time)+ "ms: Simulator ended (Contiguous -- Next-Fit)\n")
