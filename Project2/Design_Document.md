## Background & Description

### Background

#### What is memory and memory leak? 

* A memory in computer is just like a human brain. It is used to store data and instructions. Computer memory is the storage space in the computer, where data is to be processed and instructions required for processing are stored.

* Memory leak refers to that you apply to the system for allocating memory for use (New / malloc), and then the system applies for a piece of memory space for this object in the heap memory, but when we finish using it, it does not belong to the system (delete), causing the unused object to occupy the memory unit all the time, so that the system will no longer be able to allocate it to the required program.

#### What are the hazards of memory leak?

* The harm of a memory leak may not be very great, but the consequences of memory leak accumulation are very serious, no matter how much memory, sooner or later will be used up, resulting in memory leak.

### Description

* As we all know, memory is an important part of the computer, and it is the key to store the data used by CPU. However, we cannot intuitively obtain the memory information used by each process. Therefore, our team hopes to design and develop a tool on the Linux platform, which can display the memory usage and possible memory leakage of the processes that we want to observe in real time, and make real-time statistics on the memory usage of the processes and the threads in the system. For example, the size of memory allocated to the process, the usage ranking of each process. In addition, the record of memory allocation and release can help us better understand the process of memory allocation and collection, and detect the memory leakage in a process, including the leakage of memory and file handle. To avoid the harm of memory leakage to the computer.

  Now, there are instructions that show how memory is being used. Take "free" as an example, this instruction can display memory usage in KB or MB. We can also set intervals to update memory usage. In addition, "free" can also display the memory usage in the buffer. We're going to build on that.

## Implementation

The project code will be implemented in C/C++ and simulated and tested on Ubuntu.

We will refer to the [heapusage](https://github.com/d99kris/heapusage) and other relevant projects and materials to implement:

* [heapusage](https://github.com/d99kris/heapusage): Open source projects on GitHub, mainly focus on detecting memory leaks.
* [sanitizers](https://github.com/google/sanitizers): Documentation can be viewed at [Leak Sanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer). Leak Sanitizer is a memory leak detector developed by Google and the tool is supported on x86_64 Linux and OS X.

real-time statistics system process and its thread memory usage. Detect memory allocation in a process. Detect whether there is a memory leak in a process.

* Realize the memory usage information statistics, and the memory statistics should be sorted and displayed in real time.
* The encoding implementation detects the memory allocation and release in the specific process.
* The encoding implementation detects the allocation and release of the file handle in the specific process.
* Statistic process memory allocation and release, confirm whether there is leakage, if there is leakage, point out the leakage suspicious code

## Expected goals

In this project, we expect to build a real-time visual memory detection and statistics tool.

### Our steps

* Read the source code of Linux to see how Linux manages memory (such as free command)（DDL5.7）
* Build a simple cli program to view the current process of memory status statistics(DDL 5.14)
* In depth understanding of memory leaks, detection of a specific memory application and release (DDL 5.21)
* Further improve the program to detect whether there is a memory leak and build a better GUI interface(DDL 5.28)

### Final goals

* Real time statistics system process and thread memory usage
  * Coding is used to realize the statistics of memory usage information, and the memory statistics data are sorted and displayed in real time;

* Check the memory allocation and release in a process
  * Coding can detect memory allocation and release in specific process;
  * Encoding can detect the allocation and release of file handle in specific process;

*  Check whether there is a memory leak in a process
  * Count the process memory allocation and release, confirm whether there is leakage, if there is leakage, point out the suspicious code;

## Divisor

| Name   | ID       | Divisor   |
| ------ | -------- | --------- |
| 赵奕帆 | 11812020 | developer |
| 任博韬 | 11811509 | developer |
| 高昊天 | 11812011 | tester    |

