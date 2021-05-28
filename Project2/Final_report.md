## Result analysis: 

* Compared with the expected goals of the design document, explain which expected goals have been achieved and what the effects are, discuss which goals have not been achieved and what the difficulties are. 

Here in design report we have mentioned that we will divide the project into two parts.

* The first part is to detect the memory, view the memory related information, and complete the GUI visualization.

### 第二部分为对内存泄露的检测，TODO

### Task1 

**What goals have been achieved**:

> * [x] Read Linux source code, mainly read the top and free commands.
> * [x] Analysis the `meminfo` file in the / proc folder and the status file in each process folder
> * [x] Re implement free command with Python
> * [x] Use Python to re implement the top command. Here we focus on more memory.
> * [x] Implement a simple GUI to present relevant information
> * [x] Sort columns by different memory properties
>
> Main features:
>
> * [x] Learn `wxPython` and use `wxPython` to implement GUI
> * [x] Show name of each process
> * [x] Show `pid  `  of each process
> * [x] Show `ppid`  of each process
> * [x] Show Peak usage of virtual memory of each process
> * [ ] Show Virtual memory currently in use of each process
> * [x] Show Physical memory currently in use in use of each process
> * [x] Show Peak usage of Physical memory memory of each process
> * [x] Represents the total memory of the system
> * [x] Represents the memory already used by the application
> * [x] Represents memory that is not currently in use
> * [x] Represents the memory shared by the process
> * [x] Use a grid to show the above information
> * [x] Implement sorting according to any of the above keywords
>
> In future:
>
> * [ ] Realize regular update of relevant information
> * [ ] Realize more user friendly GUI
> * [ ] Integrate the functions of task 1, task 2 and task 3 to form a complete app
> * [ ] Realize more functions in Windows System Monitor

To sum up, we have successfully implemented the functions described in our design documents.

But because of the limited time and energy, we can't do everything, so we put our future planning in the future section, such as implementing a better GUI, and implementing more Linux and windows task managers.

### Task 2 & 3 TODO



## Implementation: 

* Discuss the main technologies used in the project.

### Experimental hardware equipment:

**Linux version 4.15.0-142-generic (buildd@lgw01-amd64-039) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.12)) **

### Task1

根据我们在设计报告中所描述的，我们首先阅读 `linux` 关于内存相关命令的源码。

这里我们对top和free命令进行了深入的挖掘。

top命令的重要部分源码如下：

```c
/*
 * Copyright (c) 2008, The Android Open Source Project
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the 
 *    distribution.
 *  * Neither the name of Google, Inc. nor the names of its contributors
 *    may be used to endorse or promote products derived from this
 *    software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */
 
#include <ctype.h>
#include <dirent.h>
#include <grp.h>
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
 
//#include <cutils/sched_policy.h>
/**
typedef enum {
	SP_BACKGROUND = 0,
	SP_FOREGROUND = 1,
} SchedPolicy;
*/
//extern int get_sched_policy(int tid, SchedPolicy *policy);
 
struct cpu_info {
    long unsigned utime, ntime, stime, itime;
    long unsigned iowtime, irqtime, sirqtime;
};
 
#define PROC_NAME_LEN 64
#define THREAD_NAME_LEN 32
 
struct proc_info {
    struct proc_info *next;
    pid_t pid;
    pid_t tid;
    uid_t uid;
    gid_t gid;
    char name[PROC_NAME_LEN];
    char tname[THREAD_NAME_LEN];
    char state;
    long unsigned utime;
    long unsigned stime;
    long unsigned delta_utime;
    long unsigned delta_stime;
    long unsigned delta_time;
    long vss;
    long rss;
    int num_threads;
    char policy[32];
};
 
struct proc_list {
    struct proc_info **array;
    int size;
};
 
#define die(...) { fprintf(stderr, __VA_ARGS__); exit(EXIT_FAILURE); }
 
#define INIT_PROCS 50
#define THREAD_MULT 8
static struct proc_info **old_procs, **new_procs;
static int num_old_procs, num_new_procs;
static struct proc_info *free_procs;
static int num_used_procs, num_free_procs;
 
static int max_procs, delay, iterations, threads;
 
static struct cpu_info old_cpu, new_cpu;
 
static struct proc_info *alloc_proc(void);
static void free_proc(struct proc_info *proc);
static void read_procs(void);
static int read_stat(char *filename, struct proc_info *proc);
static void read_policy(int pid, struct proc_info *proc);
static void add_proc(int proc_num, struct proc_info *proc);
static int read_cmdline(char *filename, struct proc_info *proc);
static int read_status(char *filename, struct proc_info *proc);
static void print_procs(void);
static struct proc_info *find_old_proc(pid_t pid, pid_t tid);
static void free_old_procs(void);
static int (*proc_cmp)(const void *a, const void *b);
static int proc_cpu_cmp(const void *a, const void *b);
static int proc_vss_cmp(const void *a, const void *b);
static int proc_rss_cmp(const void *a, const void *b);
static int proc_thr_cmp(const void *a, const void *b);
static int numcmp(long long a, long long b);
static void usage(char *cmd);
 
int main(int argc, char *argv[]) {
    int i;
 
    num_used_procs = num_free_procs = 0;
 
    max_procs = 0;
    delay = 3;
    iterations = -1;
    proc_cmp = &proc_cpu_cmp;
    for (i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-m")) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Option -m expects an argument.\n");
                usage(argv[0]);
                exit(EXIT_FAILURE);
            }
            max_procs = atoi(argv[++i]);
            continue;
        }
        if (!strcmp(argv[i], "-n")) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Option -n expects an argument.\n");
                usage(argv[0]);
                exit(EXIT_FAILURE);
            }
            iterations = atoi(argv[++i]);
            continue;
        }
        if (!strcmp(argv[i], "-d")) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Option -d expects an argument.\n");
                usage(argv[0]);
                exit(EXIT_FAILURE);
            }
            delay = atoi(argv[++i]);
            continue;
        }
        if (!strcmp(argv[i], "-s")) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Option -s expects an argument.\n");
                usage(argv[0]);
                exit(EXIT_FAILURE);
            }
            ++i;
            if (!strcmp(argv[i], "cpu")) { proc_cmp = &proc_cpu_cmp; continue; }
            if (!strcmp(argv[i], "vss")) { proc_cmp = &proc_vss_cmp; continue; }
            if (!strcmp(argv[i], "rss")) { proc_cmp = &proc_rss_cmp; continue; }
            if (!strcmp(argv[i], "thr")) { proc_cmp = &proc_thr_cmp; continue; }
            fprintf(stderr, "Invalid argument \"%s\" for option -s.\n", argv[i]);
            exit(EXIT_FAILURE);
        }
        if (!strcmp(argv[i], "-t")) { threads = 1; continue; }
        if (!strcmp(argv[i], "-h")) {
            usage(argv[0]);
            exit(EXIT_SUCCESS);
        }
        fprintf(stderr, "Invalid argument \"%s\".\n", argv[i]);
        usage(argv[0]);
        exit(EXIT_FAILURE);
    }
 
    if (threads && proc_cmp == &proc_thr_cmp) {
        fprintf(stderr, "Sorting by threads per thread makes no sense!\n");
        exit(EXIT_FAILURE);
    }
 
    free_procs = NULL;
 
    num_new_procs = num_old_procs = 0;
    new_procs = old_procs = NULL;
 
    read_procs();
    while ((iterations == -1) || (iterations-- > 0)) {
        old_procs = new_procs;
        num_old_procs = num_new_procs;
        memcpy(&old_cpu, &new_cpu, sizeof(old_cpu));
        sleep(delay);
        read_procs();
        print_procs();
        free_old_procs();
    }
 
    return 0;
}
 
static struct proc_info *alloc_proc(void) {
    struct proc_info *proc;
 
    if (free_procs) {
        proc = free_procs;
        free_procs = free_procs->next;
        num_free_procs--;
    } else {
        proc = malloc(sizeof(*proc));
        if (!proc) die("Could not allocate struct process_info.\n");
    }
 
    num_used_procs++;
 
    return proc;
}
 
static void free_proc(struct proc_info *proc) {
    proc->next = free_procs;
    free_procs = proc;
 
    num_used_procs--;
    num_free_procs++;
}
 
#define MAX_LINE 256
 
static void read_procs(void) {
    DIR *proc_dir, *task_dir;
    struct dirent *pid_dir, *tid_dir;
    char filename[64];
    FILE *file;
    int proc_num;
    struct proc_info *proc;
    pid_t pid, tid;
 
    int i;
 
    proc_dir = opendir("/proc");
    if (!proc_dir) die("Could not open /proc.\n");
 
    new_procs = calloc(INIT_PROCS * (threads ? THREAD_MULT : 1), sizeof(struct proc_info *));
    num_new_procs = INIT_PROCS * (threads ? THREAD_MULT : 1);
 
    file = fopen("/proc/stat", "r");
    if (!file) die("Could not open /proc/stat.\n");
    fscanf(file, "cpu  %lu %lu %lu %lu %lu %lu %lu", &new_cpu.utime, &new_cpu.ntime, &new_cpu.stime,
            &new_cpu.itime, &new_cpu.iowtime, &new_cpu.irqtime, &new_cpu.sirqtime);
    fclose(file);
 
    proc_num = 0;
    while ((pid_dir = readdir(proc_dir))) {
        if (!isdigit(pid_dir->d_name[0]))
            continue;
 
        pid = atoi(pid_dir->d_name);
        
        struct proc_info cur_proc;
        
        if (!threads) {
            proc = alloc_proc();
 
            proc->pid = proc->tid = pid;
 
            sprintf(filename, "/proc/%d/stat", pid);
            read_stat(filename, proc);
 
            sprintf(filename, "/proc/%d/cmdline", pid);
            read_cmdline(filename, proc);
 
            sprintf(filename, "/proc/%d/status", pid);
            read_status(filename, proc);
 
            read_policy(pid, proc);
 
            proc->num_threads = 0;
        } else {
            sprintf(filename, "/proc/%d/cmdline", pid);
            read_cmdline(filename, &cur_proc);
 
            sprintf(filename, "/proc/%d/status", pid);
            read_status(filename, &cur_proc);
            
            proc = NULL;
        }
 
        sprintf(filename, "/proc/%d/task", pid);
        task_dir = opendir(filename);
        if (!task_dir) continue;
 
        while ((tid_dir = readdir(task_dir))) {
            if (!isdigit(tid_dir->d_name[0]))
                continue;
 
            if (threads) {
                tid = atoi(tid_dir->d_name);
 
                proc = alloc_proc();
 
                proc->pid = pid; proc->tid = tid;
 
                sprintf(filename, "/proc/%d/task/%d/stat", pid, tid);
                read_stat(filename, proc);
 
                read_policy(tid, proc);
 
                strcpy(proc->name, cur_proc.name);
                proc->uid = cur_proc.uid;
                proc->gid = cur_proc.gid;
 
                add_proc(proc_num++, proc);
            } else {
                proc->num_threads++;
            }
        }
 
        closedir(task_dir);
        
        if (!threads)
            add_proc(proc_num++, proc);
    }
 
    for (i = proc_num; i < num_new_procs; i++)
        new_procs[i] = NULL;
 
    closedir(proc_dir);
}
 
static int read_stat(char *filename, struct proc_info *proc) {
    FILE *file;
    char buf[MAX_LINE], *open_paren, *close_paren;
    int res, idx;
 
    file = fopen(filename, "r");
    if (!file) return 1;
    fgets(buf, MAX_LINE, file);
    fclose(file);
 
    /* Split at first '(' and last ')' to get process name. */
    open_paren = strchr(buf, '(');
    close_paren = strrchr(buf, ')');
    if (!open_paren || !close_paren) return 1;
 
    *open_paren = *close_paren = '\0';
    strncpy(proc->tname, open_paren + 1, THREAD_NAME_LEN);
    proc->tname[THREAD_NAME_LEN-1] = 0;
    
    /* Scan rest of string. */
    sscanf(close_paren + 1, " %c %*d %*d %*d %*d %*d %*d %*d %*d %*d %*d "
                 "%lu %lu %*d %*d %*d %*d %*d %*d %*d %lu %ld",
                 &proc->state, &proc->utime, &proc->stime, &proc->vss, &proc->rss);
 
    return 0;
}
 
static int read_cmdline(char *filename, struct proc_info *proc) {
    FILE *file;
    char line[MAX_LINE];
 
    line[0] = '\0';
    file = fopen(filename, "r");
    if (!file) return 1;
    fgets(line, MAX_LINE, file);
    fclose(file);
    if (strlen(line) > 0) {
        strncpy(proc->name, line, PROC_NAME_LEN);
        proc->name[PROC_NAME_LEN-1] = 0;
    } else
        proc->name[0] = 0;
    return 0;
}
 
static void read_policy(int pid, struct proc_info *proc) {
	/**
    SchedPolicy p;
    if (get_sched_policy(pid, &p) < 0)
        strcpy(proc->policy, "unk");
    else {
        if (p == SP_BACKGROUND)
            strcpy(proc->policy, "bg");
        else if (p == SP_FOREGROUND)
            strcpy(proc->policy, "fg");
        else
            strcpy(proc->policy, "er");
    }*/
}
 
static int read_status(char *filename, struct proc_info *proc) {
    FILE *file;
    char line[MAX_LINE];
    unsigned int uid, gid;
 
    file = fopen(filename, "r");
    if (!file) return 1;
    while (fgets(line, MAX_LINE, file)) {
        sscanf(line, "Uid: %u", &uid);
        sscanf(line, "Gid: %u", &gid);
    }
    fclose(file);
    proc->uid = uid; proc->gid = gid;
    return 0;
}
 
 
static void usage(char *cmd) {
    fprintf(stderr, "Usage: %s [ -m max_procs ] [ -n iterations ] [ -d delay ] [ -s sort_column ] [ -t ] [ -h ]\n"
                    "    -m num  Maximum number of processes to display.\n"
                    "    -n num  Updates to show before exiting.\n"
                    "    -d num  Seconds to wait between updates.\n"
                    "    -s col  Column to sort by (cpu,vss,rss,thr).\n"
                    "    -t      Show threads instead of processes.\n"
                    "    -h      Display this help screen.\n",
        cmd);
}
```

对上述重要代码进行一个总结，也是关于top命令内存部分的总结就是，查看/proc/文件夹下各个`pid` 文件夹中的/status文件，该文件中详细记录了各个进程相关的信息，

以1号进程的status文件为例，

```C
Name:	systemd
Umask:	0000
State:	S (sleeping)
Tgid:	1
Ngid:	0
Pid:	1
PPid:	0
TracerPid:	0
Uid:	0	0	0	0
Gid:	0	0	0	0
FDSize:	128
Groups:	 
NStgid:	1
NSpid:	1
NSpgid:	1
NSsid:	1
VmPeak:	  250956 kB
VmSize:	  185420 kB
VmLck:	       0 kB
VmPin:	       0 kB
VmHWM:	    5952 kB
VmRSS:	    4212 kB
RssAnon:	    1332 kB
RssFile:	    2880 kB
RssShmem:	       0 kB
VmData:	   18400 kB
VmStk:	     132 kB
VmExe:	    1408 kB
VmLib:	    3712 kB
VmPTE:	     124 kB
VmSwap:	     644 kB
HugetlbPages:	       0 kB
CoreDumping:	0
Threads:	1
SigQ:	0/15446
SigPnd:	0000000000000000
ShdPnd:	0000000000000000
SigBlk:	7be3c0fe28014a03
SigIgn:	0000000000001000
SigCgt:	00000001800004ec
CapInh:	0000000000000000
CapPrm:	0000003fffffffff
CapEff:	0000003fffffffff
CapBnd:	0000003fffffffff
CapAmb:	0000000000000000
NoNewPrivs:	0
Seccomp:	0
Speculation_Store_Bypass:	vulnerable
Cpus_allowed:	ffffffff,ffffffff,ffffffff,ffffffff
Cpus_allowed_list:	0-127
Mems_allowed:	00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001
Mems_allowed_list:	0
voluntary_ctxt_switches:	1666
nonvoluntary_ctxt_switches:	2859
```

We focus on memory related attributes. In this implementation, we extract `Name`, `Status`,` Vmpeak `,` Vmsize `,`Vmhwm` and `Vmrss` as output.

Specifically:

* ` Name`: process name
* `Status`: the status of each process, including "R (running)," s (sleeping), "d (disk sleep)," t (stopped), "t (tracking stop)," Z (zombie), "or" x (dead) "
* `PID`: the process ID
* `PPID`: parent process ID
* `VM peak`: the peak of memory occupied by the current process
* `Vmsize`: represents the memory occupied by the process
* `Vmhwm`: is the peak value that the program gets allocated to physical memory
* `Vmrss`: the physical memory used by the program

Then we try to use Python to implement the top command to get the above information of each process.
Here we create a process class.

```python
class pro_info():
    name = ""
    status = ""
    pid = 0
    ppid = 0
    VM_peak = 0  # memory peak size
    VM_size = 0  # current memory size
    VM_HWM = 0  # physical memory peak size
    VM_RSS = 0  # current physical memory
```

Then we get the memory information of all processes by traversing all process related files in the / proc folder.
Here we filter. Some processes do not have the memory attributes mentioned above. We filter such processes.
Then all threads are stored in a list and called in the subsequent GUI phase.

Then there is the free command. For the free command, we need to view the meminfo file in the / proc directory. An example of this file is as follows.

```c
MemTotal:        4015896 kB
MemFree:          320208 kB
MemAvailable:    1438720 kB
Buffers:          146916 kB
Cached:          1144608 kB
SwapCached:        11876 kB
Active:          2187096 kB
Inactive:         883364 kB
Active(anon):    1328664 kB
Inactive(anon):   488556 kB
Active(file):     858432 kB
Inactive(file):   394808 kB
Unevictable:          32 kB
Mlocked:              32 kB
SwapTotal:       1046524 kB
SwapFree:         884732 kB
Dirty:                52 kB
Writeback:           372 kB
AnonPages:       1775172 kB
Mapped:           516288 kB
Shmem:             38276 kB
Slab:             208032 kB
SReclaimable:     139428 kB
SUnreclaim:        68604 kB
KernelStack:       12432 kB
PageTables:        38512 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     3054472 kB
Committed_AS:    5754120 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:         0 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:      216896 kB
DirectMap2M:     3977216 kB
DirectMap1G:     2097152 kB

```

Here, we focus on several important parts.

* Total: the total amount of memory
* Available: available memory
* Free: the total amount of memory that can be allocated
* Shared: shared memory between threads
* Buffers: the size of physical memory used by the buffer.
* Cached: the size of physical memory used by the cache.
* Active: the most recently used cache size
* Inactive: cache size that has not been used frequently recently

Here, we create a meminfo class to record relevant information.

```python
class mem_info():
    MemTotal = 0
    MemFree = 0
    MemAvailable = 0
    Buffers = 0
    Cached = 0
    SwapCached = 0
    Active = 0
    Inactive = 0
```

Then we use Python to open the relevant files and read the information, which is recorded in a meminfo object for subsequent GUI calls.

The last part is GUI. We use the form visualization interface provided by the grid class of wxPython to visualize. At the same time, we realize the response of mouse click event. When we click the column name, we will automatically sort the current information according to the column.

![](D:\Desktop\OS\Project2\1.png)

### Task2&3 TODO



## Future direction: 

* For this project, discuss the future directions that can be expanded. 

As mentioned in the beginning, we still have some plans for the future, but due to limited time and energy, they have not been realized at present, so we put them into the future plan.

* First of all, for the realization of more functions, we intend to imitate Linux and windows system monitor to achieve more functions, such as monitoring CPU usage, viewing application history, viewing GPU usage, recording the dynamics of each user, recording changes in network conditions, etc. We believe that the attempt of these functions will enable us to dig deeper into the kernel of the operating system and have a deeper understanding of the whole operating system.
* Secondly, we will try to further beautify the GUI, such as adding some animations, charts, and more interaction with users. In addition, we plan to integrate GUI of task 1 with GUI of task 2 and task 3, which will make our project more complete and bring users a better experience.
* TODO

## Summary: 

* Summarize the main techniques learned through the project and the experience of teamwork.

  In this project, our team division of labor is very clear. The division of labor with high cohesion and low coupling reduces the complexity of completing this project and improves our efficiency.

  * In task 1, we read a lot about the source code of Linux implementation, and we were shocked by the beauty of programming of Linux developers. This also aroused our interest in further exploring the operating system. At the same time, using Python to re implement the related functions is also a deeper understanding of Linux memory management. Finally, we make a simple GUI. In this process, we have a superficial understanding of Python GUI Library - wxPython. Visualization is also an essential part of the operating system. If we have more time, we also want to try more other orders.

  * Task2&3 TODO

## Division of labor: 

* List the main work for each team member.

| id       | name   | labor     |
| -------- | ------ | --------- |
| 11812011 | 高昊天 | Task1&GUI |
| 11812020 |        |           |
| 11811509 |        |           |

