# Raw (unsynchronized) read, and write operations for threading demo

import threading
import time

REVERSALS_PER_WRITE = 1; 

theForwardString = "Hello, World!"
theBackwardString = theForwardString[::-1]

theString = bytearray(theForwardString, encoding='utf8');
errorCount = 0

printLock = threading.Lock()

def is_valid(string):
    decodedString = string.decode("utf-8")
    # todo: change to char-by-char comparison
    # to avoid Python's inherent thread-safety
    if decodedString == theForwardString:
        return True
    if decodedString == theBackwardString:
        return True
    
    # Error detected
    global errorCount
    errorCount += 1
    with printLock:
        err_msg = "Error: Corrupted string: " + decodedString
        print(err_msg)

def Read():
    is_valid(theString)
    return theString

def Write():
    global theString
    for i in range(REVERSALS_PER_WRITE):
        is_valid(theString)
        reverse_string_in_place(theString)
        is_valid(theString)

def reverse_string_in_place(theStr):
    left = 0
    right = len(theStr) - 1
    while left < right:
        # swap 
        temp = theStr[left]
        theStr[left] = theStr[right]
        theStr[right] = temp

        # Move pointers towards the middle
        left += 1
        right -= 1
        time.sleep(1e-7)

