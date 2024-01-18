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
    time.sleep(1e-7)
    is_valid(theString)
    time.sleep(1e-7)
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

