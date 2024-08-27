Python code demos the multithreading design pattern of either allowing many threads to read an object simultaneously or, 
when modifying that object, allowing only a single thread to write to it.

Note that because Python's Global Interpreter Lock makes Python single-threaded, these demos have 
little practical use.

The QueueLess branch takes about a minute for this demo to run and conclude printing to the console.  Run main.py.

The main branch has a message queue that could be made to enforce one of many possible fairness policies
to prioritize reading vs. writing. 

See also similar demos I wrote in other languages:
- C#:  https://github.com/cforden/ReadManyWrite1_CS
- C++  https://github.com/cforden/ReadManyWrite1_Cpp
Those are multithreaded languages for which those demos could be useful.
