# StringReverseSyncd - Synchronized (protected for multithreading) methods
# for reading and writing (reversing) strings

import threading
from collections import deque

import StringReverse

queue = deque()
READ = "read"
WRITE = "write"
qLock = threading.Lock()
readersCount = 0
readersCountCondition = threading.Condition()
isWriting = False
maxReaders = 0

def is_not_writing():
    return not isWriting

def readers_all_finished():
    return readersCount is 0

def Read():
    queue.appendleft(READ)

    # Now that we have pushed a read-request onto the queue,
    # wait for one to emerge from the queue:
    global readersCount
    canRead= False
    cmd = ""
    while not canRead:
        with readersCountCondition:
            readersCountCondition.wait_for(is_not_writing)
        with qLock:
            if len(queue) > 0:
                if queue[-1] is READ:
                    canRead = True
                    cmd = queue.pop()
                    with readersCountCondition:
                        readersCount += 1
                else:
                    # Yield so writing cmds to be popped off
                    continue
            else:
                with StringReverse.printLock:
                    print("\nERROR: input queue was empty after pushing a READ\n")
    # Any number of threads are allowed to read simultaneously, so no lock here:
    StringReverse.Read()
    with readersCountCondition:
        readersCount -= 1
        readersCountCondition.notify_all()
    DbgReadValidity(cmd)

def DbgReadValidity(cmd):
    if cmd is not READ:
        with StringReverse.printLock:
            print(f"\nERROR: Cmd should be READ, was {cmd}.\n")
    # not thread-safe but good enough for rough debug checking:
    global maxReaders
    if readersCount > maxReaders:
        maxReaders = readersCount
    if readersCount > 3 or readersCount < 0:
        with StringReverse.printLock:
            print(f"\nWARNING: readersCount: {readersCount}\n")
    
def Write():
    global isWriting
    queue.appendleft(WRITE)

    # now that we pushed a WRITE, try to POP one:
    canWrite = False
    while not canWrite:
        with qLock:
            if len(queue) > 0:
                with readersCountCondition:
                    readersCountCondition.wait_for(readers_all_finished)
                if queue[-1] is WRITE:
                    canWrite = True
                    isWriting = True
                    StringReverse.Write()
                    queue.pop()
            else:
                with StringReverse.printLock:
                    print("\nERROR: input queue was empty after pushing a WRITE.\n")
    isWriting = False
