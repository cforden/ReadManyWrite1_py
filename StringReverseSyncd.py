# StringReverseSyncd - Synchronized (protected for multithreading) methods
# for reading and writing (reversing) strings demo

import threading

import StringReverse

readersCount = 0
readersCountCondition = threading.Condition()
isWriting = False
maxReaders = 0

def is_not_writing():
    return not isWriting

def readers_all_finished():
    return readersCount == 0

def Read():
    global readersCount
    with readersCountCondition:
        readersCountCondition.wait_for(is_not_writing)
        readersCount += 1
    # Any number of threads are allowed to read simultaneously, so no lock here:
    StringReverse.Read()
    with readersCountCondition:
        readersCount -= 1
        readersCountCondition.notify_all()
    DbgReadValidity()
    

def Write():
    global isWriting

    with readersCountCondition:
        readersCountCondition.wait_for(readers_all_finished)
        isWriting = True
        StringReverse.Write()
    isWriting = False


def DbgReadValidity():
    global maxReaders
    with readersCountCondition:
        if readersCount > maxReaders:
            maxReaders = readersCount
        if readersCount > 3 or readersCount < 0:
            with StringReverse.printLock:
                print(f"\nWARNING: readersCount: {readersCount}\n")

def GetMaxReaders():
    return maxReaders
