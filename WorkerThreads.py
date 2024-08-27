import threading
import time

from StringReverseSyncd import Read
from StringReverseSyncd import Write
from StringReverse import printLock

MAX_LOOP = 1000;
STATUS_LOOPS = 100;
# Also see REVERSALS_PER_WRITE StringReverse Write(), to increase string-corruptions

READER_THREADS = 3
WRITER_THREADS = 2

total_reads = 0
total_reads_lock = threading.Lock()
total_writes = 0
total_writes_condition = threading.Condition()

def reader_thread(**kwargs):
    ID = kwargs.get("ID")
    global total_reads
    for thread_local_reads in range(MAX_LOOP):
        if not reads_are_not_hogging():
            with total_writes_condition:
                total_writes_condition.wait_for(reads_are_not_hogging, 1e-8)
        Read()
        if thread_local_reads % STATUS_LOOPS == 0:
            with printLock:
                print(f"Reader {ID}, iteration {thread_local_reads}")
        with total_reads_lock:
            total_reads += 1

def writer_thread(**kwargs):
    ID = kwargs.get("ID")
    global total_writes
    for thread_local_writes in range(MAX_LOOP):
        if not writes_are_not_hogging():
            with total_writes_condition:
                total_writes_condition.wait_for(writes_are_not_hogging, 1e-8)
        Write()
        if thread_local_writes % STATUS_LOOPS == 0:
            with printLock:
                print(f"Writer {ID}, iteration {thread_local_writes}")
        with total_writes_condition:
            total_writes += 1
        if reads_are_not_hogging():
            with total_writes_condition:
                total_writes_condition.notify_all()
        time.sleep(1e-8)


def reads_are_not_hogging():
    return total_reads/READER_THREADS < total_writes/WRITER_THREADS + 5

def writes_are_not_hogging():
    return total_reads/READER_THREADS > total_writes/WRITER_THREADS + 7
