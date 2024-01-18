import threading
import StringReverse
from WorkerThreads import reader_thread
from WorkerThreads import writer_thread

def do_threads():
    t1 = threading.Thread(target=reader_thread, kwargs={"ID": 1})
    t1.start()

    t2 = threading.Thread(target=reader_thread, kwargs={"ID": 2})
    t2.start()

    t3 = threading.Thread(target=reader_thread, kwargs={"ID": 3})
    t3.start()

    t4 = threading.Thread(target=writer_thread, kwargs={"ID": 4})
    t4.start()

    t5 = threading.Thread(target=writer_thread, kwargs={"ID": 5})
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

if __name__ == "__main__":
    print()
    do_threads()
    print(f"Error count: {StringReverse.errorCount}")

