from StringReverseSyncd import Read
from StringReverseSyncd import Write
from StringReverse import printLock

MAX_LOOP = 1000;
STATUS_LOOPS = 100;
# Also see REVERSALS_PER_WRITE StringReverse Write(), to increase string-corruptions

def reader_thread(**kwargs):
    ID = kwargs.get("ID")
    for i in range(MAX_LOOP):
        Read()
        if i % STATUS_LOOPS == 0:
            with printLock:
                print(f"Reader {ID}, iteration {i}")

def writer_thread(**kwargs):
    ID = kwargs.get("ID")
    for i in range(MAX_LOOP):
        Write()
        if i % STATUS_LOOPS == 0:
            with printLock:
                print(f"Writer {ID}, iteration {i}")


