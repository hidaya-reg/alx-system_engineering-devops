# 0x05. Processes and signals
## Resources
- [Linux PID](https://www.linfo.org/pid.html)
- [Linux process](https://www.thegeekstuff.com/2012/03/linux-processes-environment/)
- [Linux signal](https://www.educative.io/answers/what-are-linux-signals)
- [Process management in linux](https://www.digitalocean.com/community/tutorials/process-management-in-linux)
- [All about signals](https://www.computerhope.com/unix/signals.htm)

## Learning Objectives
<details>
<summary>What is a PID</summary>

### PID
A PID (Process ID) is a unique numerical identifier assigned to each process running on a computer. In operating systems like Linux, Unix, and Windows, every active process has its own PID, which is used by the operating system to keep track of and manage processes.

Here's what makes a PID useful:
- **Process Management:** The PID allows system administrators and users to monitor, control, and manage specific processes. For instance, you can use the PID to terminate a process with commands like kill in Linux.
- **System Stability:** PIDs help prevent conflicts between processes by ensuring that each process has a unique identifier.
- **Debugging and Profiling:** Tools can target specific PIDs to diagnose or profile a program's behavior.

PIDs are generally assigned incrementally, but when the limit is reached, they wrap around to the lowest available PID.
</details>
<details>
<summary>What is a process</summary>

### What is a process
A **process** is an instance of a program that is running on a computer. When you execute a program, the operating system creates a process to manage the program's execution, including the code, resources, and memory space required.

Here’s a breakdown of what a process involves:
1. Executable Code: This is the code of the program that is currently being executed.
2. Memory Space: Each process has its own isolated memory space, which includes:
    + Text Segment: Contains the compiled program code.
    + Data Segment: Stores global and static variables.
    + Heap: Used for dynamic memory allocation.
    + Stack: Manages function calls and local variables.
3. Process Control Block (PCB): The OS uses this data structure to track information about the process, such as its state, PID, CPU registers, memory allocation, and file descriptors.
4. State: Processes go through different states during their lifecycle, such as:
- New: Being created.
- Ready: Waiting to be assigned to the CPU.
- Running: Actively executing on the CPU.
- Waiting: Paused, waiting for an event (like input/output).
- Terminated: Finished execution or has been killed.
5. Resource Management: The process may require various system resources, like CPU time, memory, files, and network connections.

#### Process vs. Program
A program is just a static set of instructions stored on disk, while a process is a dynamic instance of that program in action, with its own resources and state. Multiple processes can run the same program simultaneously, each in its own isolated memory space.

In summary, a process is the running form of a program, managed by the operating system to ensure stability, resource allocation, and execution control.
</details>
<details>
<summary>Process Management in Linux</summary>

### Process Management in Linux
#### Types of Processes in Linux
**1. Foreground Processes:**
    + Depend on user input.
    + Also known as interactive processes.
**2. Background Processes:**
    + Run independently of the user.
    + Known as non-interactive or automatic processes.
#### Process States in Linux
- **Running:** Actively executing or ready to execute.
- **Sleeping:**
    + **Interruptible sleep:** Process can wake up to handle signals.
    + **Uninterruptible sleep:** Process will not respond to signals.
- **Stopped:** Process is halted, usually due to a stop signal.
- **Zombie:** Process has completed, but its entry remains in the process table.

#### Commands for Process Management in Linux
**1. ``top`` Command:** Displays real-time information about processes, including:
- **PID**: Process ID
- **User**: Process owner
- **PR**: Scheduling priority
- **NI**: Nice value
- **VIRT**, **RES**, **SHR**: Memory usage stats
- **S**: Process state (D for uninterruptible sleep, R for running, etc.)
    + ``R``: Running or runnable (ready to run)
    + ``S``: Sleeping (waiting for an event to complete)
    + ``D``: Uninterruptible sleep (usually waiting for I/O)
    + ``T``: Stopped (by a signal or via job control)
    + ``Z``: Zombie (terminated but not reaped by its parent)
- **%CPU** and **%MEM**: Resource usage

Use arrow keys to navigate and ``q`` to quit. Press ``k`` to kill a selected process.
**2. ``ps`` Command:** Displays a snapshot of running processes.
Common options:
- ``a``: Shows processes for all users, not just your own.
- ``u``: Displays user-oriented format with more details, like the user name, CPU, and memory usage.
- ``x``: Includes processes that are not associated with a terminal, such as background processes.
```bash
ps -aux
```
Note: In ``ps -aux``, the ``-`` is optional. You can write it as either ``ps aux`` or ``ps -aux``.
**3. Stopping a Process:** ``kill`` Command: Sends a signal to terminate a process.
- ``kill -9 [PID]``: Sends SIGKILL (force kill).
- ``kill -L``: Lists all signals.
- ``kill [PID]``: Sends SIGTERM (gentle kill by default).

**4. Changing Process Priority (Niceness):**
- **Nice values** range from ``-20`` (highest priority) to ``19`` (lowest priority).
- Start a process with a specific nice value:
    ```bash
    nice -n [value] [process name]
    ```
- Change priority of an existing process:
    ```bash
    renice [value] -p [PID]
    ```
</details>
<details>
<summary>How to find a process’ PID</summary>

### How to find a process’ PID
To find a process's PID (Process ID) in Linux, you can use various commands depending on what you know about the process.

#### 1. Using the ``ps`` Command
The ps command can be used to filter for a specific process by name: ``ps -aux | grep [process_name]``

Replace ``[process_name]`` with the actual name of the process. This will list all processes with that name, along with their PIDs.

Example:
``ps -aux | grep nginx``
This command searches for any running ``nginx`` processes and shows their PIDs.

#### 2. Using the ``pgrep`` Command
- **Basic Usage** ``pgrep [options] pattern``
- **How It Works**
    1. Pattern Matching: 
        + ``pgrep`` takes a pattern (usually the name of a process) as an argument and searches for processes whose names match the specified pattern.
        + It uses regular expressions, which means you can perform complex matching.
    2. Output:
        + If a match is found, ``pgrep`` outputs the PIDs of the matching processes, one per line.
        + If no matches are found, ``pgrep`` returns nothing and exits with a status code of 1.
    3. Options: ``pgrep`` supports various options to refine your search. Here are a few commonly used options:
        + ``-u``: Search for processes owned by a specific user.
        + ``-l``: List the matching processes along with their names.
        + ``-f``: Match against the full command line instead of just the process name.
- **Example Commands**
    + Find Processes by Name: `pgrep bash`
    This command will return the PIDs of all running Bash processes.
    + Find Processes by User: `pgrep -u username`
    This command will return the PIDs of processes owned by username.
    + List Matching Processes with Names: `pgrep -l ssh`
    This command returns the PIDs and names of processes matching "ssh".
    + Match Against Full Command Line: `pgrep -f "python script.py"`
    This searches for processes that include "python script.py" in their full command line.

#### 3. Using the ``pidof`` Command
``pidof`` is similar to ``pgrep`` but is specifically designed to find the PID of a single process. `pidof [process_name]`
Example:
``pidof sshd``
This command will return the PID of the ``sshd`` process if it’s running.

#### 4. Checking ``/proc`` Directory
If you know the exact name of the command that started the process, you can search the ``/proc`` directory:
```bash
ls -l /proc | grep [process_name]
```
#### 5. Using the ``top`` or ``htop`` Command
Run ``top`` or ``htop`` to view a list of all processes along with their PIDs in real-time.
Use the arrow keys to navigate to your process.
</details>
<details>
<summary>How to kill a process</summary>

### How to kill a process
#### 1. Using the ``kill`` Command with the PID
The ``kill`` command allows you to send a signal to a process, typically to terminate it.

**Basic Syntax:** `kill [signal] [PID]`
- **SIGTERM** (default): Sends a termination signal that can be caught by the process, allowing it to clean up before exiting.
- **SIGKILL**(``-9``): Forces the process to terminate immediately without cleanup.
Examples:
- To gently terminate a process (replace ``[PID]`` with the actual Process ID): `kill [PID]`
- To forcefully terminate a process: `kill -9 [PID]`

#### 2. Using the ``pkill`` Command by Process Name
``pkill`` allows you to kill processes by name instead of PID. `pkill [process_name]`

Example:
- To force kill a process by name: `pkill -9 [process_name]`

#### 3. Using ``killall`` Command by Process Name
``killall`` is similar to ``pkill`` but is used to terminate all instances of a process with a specific name. `killall [process_name]`

Example:
- To forcefully terminate all instances of a process:`killall -9 [process_name]`

#### 4. Using ``htop`` or ``top`` to Kill a Process
In ``htop`` or ``top``, you can view a list of processes and kill one interactively.

1. Run ``htop`` or ``top``:
2. Navigate to the process you want to kill (use arrow keys in ``htop``).
3. Press ``F9`` (in ``htop``) or ``k`` (in ``top``), then select the kill signal.

**Note:** Killing a process with ``-9`` (SIGKILL) should be used only when necessary, as it doesn’t allow the process to perform any cleanup.
</details>
<details>
<summary>What is a signal</summary>

### Signa
ln Linux and Unix-like operating systems, a signal is a form of inter-process communication used to notify a process that a specific event has occurred. Signals are used by the operating system and other programs to interrupt, control, or terminate processes. They are essentially messages sent to a process by the kernel, another process, or the user.

Each signal has a unique number and a symbolic name.
#### Common Signals in Linux

| Signal Name | Signal Number | Description                        | Example Command                          |
|-------------|---------------|------------------------------------|------------------------------------------|
| **SIGHUP**  | 1             | Hang Up Signal (terminal closed)  | `kill -HUP [PID]`                        |
| **SIGINT**  | 2             | Interrupt Signal (Ctrl+C)         | `kill -INT [PID]` or `kill -2 [PID]`   |
| **SIGQUIT** | 3             | Quit Signal (Ctrl+\)              | `kill -QUIT [PID]` or `kill -3 [PID]`  |
| **SIGILL**  | 4             | Illegal Instruction                | `kill -ILL [PID]` or `kill -4 [PID]`   |
| **SIGABRT** | 6             | Abort Signal                       | `kill -ABRT [PID]` or `kill -6 [PID]`  |
| **SIGFPE**  | 8             | Floating Point Exception           | `kill -FPE [PID]` or `kill -8 [PID]`   |
| **SIGKILL** | 9             | Kill Signal (forcefully terminate) | `kill -KILL [PID]` or `kill -9 [PID]`  |
| **SIGSEGV** | 11            | Segmentation Fault                 | `kill -SEGV [PID]` or `kill -11 [PID]` |
| **SIGTERM** | 15            | Termination Signal (default kill) | `kill [PID]` or `kill -TERM [PID]`     |
| **SIGSTOP** | 19            | Stop Signal (pause process)       | `kill -STOP [PID]`                      |
| **SIGCONT** | 18            | Continue Signal (resume process)   | `kill -CONT [PID]`                      |
| **SIGUSR1** | 10            | User-defined Signal 1              | `kill -USR1 [PID]`                      |
| **SIGUSR2** | 12            | User-defined Signal 2              | `kill -USR2 [PID]`                      |
| **SIGALRM** | 14            | Alarm Signal                       | `kill -ALRM [PID]` or `kill -14 [PID]` |
| **SIGCHLD** | 17            | Child Status Signal                | `kill -CHLD [PID]` or `kill -17 [PID]` |


#### How to Send Signals
To send a signal to a process, you can use:
- ``kill`` **command** with the process ID (PID), like this:
```bash
kill -9 1234   # Send SIGKILL to process with PID 1234
kill -15 1234  # Send SIGTERM to process with PID 1234
```
- ``pkill`` or ``killall`` commands by specifying the process name:
```bash
pkill -SIGINT myprogram   # Send SIGINT to all processes named "myprogram"
```
#### Signal Handling in Programs
Programs can handle specific signals to perform custom actions when they receive those signals. For instance, a web server might reload its configuration when it receives ``SIGHUP``. However, some signals, like ``SIGKILL`` and ``SIGSTOP``, cannot be caught or ignored by a process.
#### Summary
Signals are quick notifications that help control what programs do. By sending a signal, you can interrupt, pause, or terminate a program, or even tell it to perform a custom action.
</details>
<details>
<summary>What are the 2 signals that cannot be ignored</summary>

### Two signals that cannot be ignored

#### 1. SIGKILL (Signal Number 9):
This signal is used to forcefully terminate a process immediately. When a process receives SIGKILL, it is terminated without any chance to clean up or perform any shutdown tasks. It cannot be caught, blocked, or ignored, making it a very effective way to stop a stubborn process.

#### 2. SIGSTOP (Signal Number 19):
This signal stops a process, pausing its execution. Like SIGKILL, SIGSTOP cannot be caught or ignored by the process. When a process receives this signal, it will stop running until it receives a SIGCONT signal to resume.
These two signals are essential for process control in Unix-like operating systems because they ensure that critical control operations can be performed regardless of the state of the process.
</details>
<details>
<summary>Signal Handling</summary>

### Signal Handling `trap`
In the context of Unix-like operating systems, a `trap` is a mechanism that allows a process to handle signals or specific events within its code. It enables a program to define custom behavior when it receives certain signals, rather than terminating or ignoring them.

#### Key Points About ``trap``:
1. Signal Handling: The ``trap`` command is often used in shell scripts to specify commands that should be executed when the shell receives certain signals. This allows the script to perform cleanup operations or handle errors gracefully.

2. Syntax: In shell scripts, the syntax for using ``trap`` is: `trap 'commands' SIGNAL`
Here, ``commands`` is the command or sequence of commands to execute when the specified ``SIGNAL`` is received.

3. Multiple Signals: You can set traps for multiple signals at once by separating them with spaces: `trap 'commands' SIGNAL1 SIGNAL2`

4. Removing Traps: To remove a trap for a signal, you can use an empty command string: `trap '' SIGNAL`

#### Example Usage: 
Here’s an example of a shell script that uses trap to handle the SIGINT signal (generated by pressing ``Ctrl+C``):
```bash
#!/bin/bash

cleanup() {
    echo "Cleaning up before exit..."
    exit 0
}

trap cleanup SIGINT

while true; do
    echo "Running..."
    sleep 1
done
```
In this example, when the user interrupts the script with Ctrl+C, the cleanup function is called, which prints a message and exits the script cleanly.

</details>
<details>
<summary>he ampersand (``&``)</summary>

### he ampersand (``&``)

In the command line, the ampersand (``&``) has a special function: it is used to run commands in the background. When you append & to the end of a command, the shell executes the command as a background process, allowing you to continue using the terminal without waiting for that command to finish.

#### Basic Usage of ``&``
- **Foreground Execution (Default):** When you run a command normally, it runs in the foreground, blocking your terminal until it completes.
```bash
sleep 5  # Terminal will be blocked for 5 seconds
```
- **Background Execution:** When you add ``&`` at the end of a command, the command runs in the background.
```bash
sleep 5 &  # Runs in the background immediately, terminal is free for other commands
```
The shell will typically output a job ID and a process ID (PID) when you start a background process: `[1] 12345`
- ``1`` is the job ID.
- ``12345`` is the process ID.
**Example**
```bash
$ sleep 10 &
[1] 12345
```
- ``sleep 10`` runs in the background for 10 seconds.
- You can continue using the terminal to run other commands immediately.
#### Bringing a Background Process to the Foreground
You can bring a background process back to the foreground using the ``fg`` command along with the job ID:
```bash
fg %1  # Brings job 1 to the foreground
```

#### Job Control Commands
**Jobs are shell-specific:** The ``jobs`` command only displays background tasks in the current shell session.
- ``jobs``: Lists all jobs started in the current shell session, showing their status (running, stopped, etc.) and job IDs.
```bash
$ jobs
[1]+  Running                 sleep 5 &
```
- ``fg``: Brings a background job to the foreground. You can specify the job ID if there are multiple jobs.
```bash
$ fg %1  # Brings job 1 to the foreground
```
- ``bg``: Resumes a stopped job in the background. Useful if you paused a job (e.g., with ``Ctrl+Z``).
```bash
$ bg %1  # Resumes job 1 in the background
```
- ``kill``: Terminates a job by sending it a signal. You can specify a job ID or a PID.
```bash
$ kill %1  # Kills job 1
```
**Job IDs**
When a job is started, it is assigned a unique job ID within the current shell session. This ID is prefixed by a ``%`` when referencing the job (e.g., ``%1`` for job 1). Each job can also have a corresponding process ID (PID) that is used for lower-level process management.
#### Summary
- ``&``: Runs a command in the background.
- ``jobs``: Lists background jobs.
- ``fg``: Brings a background job to the foreground.
- ``bg``: Resumes a stopped job in the background.
- ``kill``: Terminates a job by sending it a signal.

</details>
<details>
<summary>Double Ampersand (&&)</summary>

### Double Ampersand (``&&``)
In shell scripting and command-line interfaces, the double ampersand (&&) is used as a logical operator that allows you to execute multiple commands conditionally based on the success (exit status) of the preceding command.

#### How ``&&`` Works
- When you use ``command1 && command2``, ``command2`` will only execute if ``command1`` completes successfully (i.e., returns an exit status of ``0``).
- If ``command1`` fails (i.e., returns a non-zero exit status), ``command2`` will not be executed.
#### Example
```bash
mkdir new_directory && cd new_directory
```
In this case:
- ``mkdir new_directory`` creates a new directory called ``new_directory``.
- If the directory creation is successful, ``cd new_directory`` will change into that directory.
- If mkdir fails (for example, if the directory already exists), ``cd new_directory`` will not be executed.
#### Chaining Multiple Commands
You can chain multiple commands using ``&&``:
```bash
command1 && command2 && command3
```
Here, ``command3`` will execute only if both ``command1`` and ``command2`` succeed.

#### Summary
- ``&&`` is used to execute commands conditionally based on the success of the previous command.
- It helps in creating scripts that depend on the successful completion of previous steps, ensuring that subsequent commands only run if prior ones are successful.
</details>
<details>
<summary>What is Daemon</summary>

### Daemons
In computing, a daemon (pronounced "dee-muhn") is a background process that runs continuously and handles requests for services or performs tasks without direct user intervention. Daemons are essential for performing various system functions and providing services to applications or users.

#### Characteristics of Daemons
**1. Background Operation:** Daemons run in the background, allowing them to operate independently of user sessions. This means they can start when the system boots and continue running without needing user input.
**2. Service Providers:** Daemons typically provide services such as:
- Web servers (e.g., Apache, Nginx)
- Database servers (e.g., MySQL, PostgreSQL)
- Print servers (e.g., CUPS)
- Email servers (e.g., Postfix, Sendmail)

**3. No User Interface:** Daemons do not interact with users directly. Instead, they may communicate with other programs or system components through inter-process communication (IPC) mechanisms, such as sockets or message queues.
**4. Managed by System:** Daemons are often managed by the system's init system (e.g., ``init``, ``systemd``) during startup and shutdown processes. They can be started, stopped, or restarted based on system needs.
**5. Logging:** Daemons typically log their activity to system logs or dedicated log files to help with monitoring and troubleshooting.

#### Common Types of Daemons
Here are some common examples of daemons and their functions:

- **Web Server Daemons:** Handle HTTP requests (e.g., ``httpd`` for Apache, ``nginx`` for Nginx).
- **Database Daemons:** Manage database operations (e.g., ``mysqld`` for MySQL, ``postgres`` for PostgreSQL).
- **Cron Daemon:** Manages scheduled tasks (e.g., ``cron`` or ``crond``), executing jobs at specified times.
- **SSH Daemon:** Provides secure shell access to the system (e.g., ``sshd``).
- **Print Daemon:** Manages print jobs and queues (e.g., ``cupsd`` for CUPS).
- **Mail Transfer Agents (MTAs):** Handle email delivery (e.g., ``postfix``, ``sendmail``).
#### Creating a Daemon
To create a daemon, a process typically follows these steps:
**1. Forking:** The process forks itself, creating a child process that runs in the background. The parent process can exit, allowing the child to run independently.
**2. Changing Directory:** The daemon may change its working directory to a non-volatile location (e.g., ``/``).
**3. File Mode Creation Mask:** It sets the file mode creation mask to ensure it has the necessary permissions for any files it creates.
**4. Closing Standard File Descriptors:** The daemon usually closes standard input, output, and error file descriptors to detach itself from the terminal.
**5. Running in the Background:** The daemon enters an infinite loop to perform its tasks or wait for events.

#### Summary
- A daemon is a background process that performs tasks or provides services without direct user interaction.
- Daemons are crucial for system functionality, enabling various services like web serving, database management, and scheduled tasks.
- They operate independently and are managed by the system's init system or service manager.
</details>
<details>
<summary>What's in /etc/init.d/ directory</summary>

### The ``/etc/init.d/`` directory
In Unix-like operating systems, especially those derived from or similar to Linux, the /etc/init.d/ directory plays a crucial role in the management of system services (also known as daemons). 
#### What is ``/etc/init.d/``?
- **Directory Location:** The ``/etc/init.d/`` directory contains initialization scripts that manage system services. These scripts are executed during the boot process and can also be used to start, stop, restart, or check the status of services.
- **Script Types:** Each script in this directory corresponds to a specific service (such as a web server, database, or other daemon) and is typically named after that service.
#### Functions of init.d Scripts
- **Service Management:** The primary purpose of scripts in ``init.d`` is to control the services running on the system. Common actions performed by these scripts include:
    + Start: Initiates the service.
    + Stop: Terminates the service.
    + Restart: Stops and then starts the service.
    + Status: Displays the current state of the service.
#### Typical Structure of an Init Script
An init script generally includes the following components:
1. **Shebang Line:** Indicates the script interpreter, usually ``#!/bin/sh``.
2. **Description:** A comment at the top describing the service.
3. **Control Functions:** Functions for starting, stopping, and managing the service.
4. **Case Statement:** A conditional structure that checks for arguments (like ``start``, ``stop``, etc.) and calls the appropriate function.

#### Example Init Script
```bash
#!/bin/sh
### BEGIN INIT INFO
# Provides:          my_service
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: My custom service
### END INIT INFO

start() {
    echo "Starting my_service"
    # Command to start the service
}

stop() {
    echo "Stopping my_service"
    # Command to stop the service
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        # Command to check service status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
```
#### Service Management on Modern Systems
- **Systemd:** Many modern Linux distributions have shifted from using ``init.d`` scripts to a newer system called **systemd**. Systemd uses **unit files** located in ``/etc/systemd/system/`` and ``/lib/systemd/system/`` to manage services. While ``init.d`` scripts are still supported for backward compatibility, ``systemd`` provides a more robust and efficient way to handle services.
#### Summary
- The ``/etc/init.d/`` directory contains initialization scripts for managing system services in Unix-like operating systems.
- These scripts provide a standardized way to start, stop, and check the status of services during system boot and runtime.
- While ``init.d`` scripts are still in use, many modern distributions now prefer systemd for service management.
</details>
<details>
<summary>`nohup` command</summary>

### `nohup` command
``nohup`` (short for "no hang-up") is a command that allows a process to keep running in the background, even if you log out or close the terminal. Normally, when you close the terminal, processes started from that terminal receive a ``SIGHUP`` (hang-up) signal, which usually terminates them. ``nohup`` prevents this by ignoring the ``SIGHUP`` signal.

#### Basic ``nohup`` Example
```bash
nohup ./my_script.sh &
```
- ``nohup`` tells the shell to ignore the ``SIGHUP`` signal, allowing the script to keep running.
- ``./my_script.sh`` is the script or command you want to run.
- ``&`` at the end places the process in the background, allowing you to continue using the terminal without waiting for the command to finish.
#### Example Behavior
**1. Without ``nohup``:**
```bash
./my_script.sh &
```
The script runs in the background, but if you close the terminal, it will receive a ``SIGHUP`` signal and likely terminate.
**2. With ``nohup``:**
```bash
nohup ./my_script.sh &`
```
The script will keep running in the background even if you close the terminal, because ``nohup`` ignores the ``SIGHUP`` signal.
#### Default Output with nohup
If you don’t specify any output redirection, ``nohup`` automatically sends the output (both ``stdout`` and ``stderr``) to a file called ``nohup.out`` in the current directory.
```bash
nohup ./my_script.sh &
# Output goes to nohup.out
```
#### Redirecting Output to a Custom File
If you want to avoid ``nohup.out`` and specify your own output file, you can redirect the output like this:
```bash
nohup ./my_script.sh > my_output.log 2>&1 &
```
- ``> my_output.log`` redirects ``stdout`` to ``my_output.log``.
- ``2>&1`` redirects ``stderr`` to the same location as stdout, so both ``stdout`` and ``stderr`` end up in ``my_output.log``.
#### Example Scenario
Imagine you have a script ``my_script.sh`` that performs some long-running task, like logging system status every minute. You want it to keep running, even if you log out. Here’s how you might use nohup:
```bash
#!/bin/bash
while true; do
    echo "Logging system status at $(date)" >> /tmp/system_status.log
    sleep 60
done
```
Running the Script with nohup:
```bash
nohup ./my_script.sh > /tmp/my_script_output.log 2>&1 &
```
**What Happens:**
- The script runs in the background, keeps logging system status every minute to ``/tmp/system_status.log``.
- The message Logging system status at... is redirected to ``/tmp/my_script_output.log``.
- The process continues to run, even if you close the terminal.
#### Checking the Running nohup Process
To check if the script is still running, you can use:
```bash
ps aux | grep my_script.sh
```
Or, if you saved the ``PID`` to a file when running ``nohup`` (like in an init script), you can use ``cat`` to read the ``PID`` file and ``kill -0`` to check if it’s running:
```bash
cat /var/run/my_script.pid
kill -0 $(cat /var/run/my_script.pid) && echo "Script is running"
```

</details>
<details>
<summary>what a zombie process is</summary>

### Zombie Processes
- **Definition:** **zombie process** is a process that has completed its execution but still has an entry in the process table. This situation happens when a process has finished running, but its **parent process** has not yet acknowledged its termination.
- **State:** When a child process terminates, it sends a signal (specifically, ``SIGCHLD``) to its parent process. The child process remains in a **defunct** state until the parent reads its exit status. This ensures that the system can keep track of the process's termination status and resource usage.
- **Representation:** In the output of commands like ``ps``, zombie processes are shown with the status ``Z`` and the ``<defunct>`` tag. For example:
```bash
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user     13527  0.0  0.0      0     0 ?        Z      01:19   0:00 [zombie] <defunct>
```
In this output:
- ``PID``: The process ID of the zombie.
- ``STAT``: The process status (``Z`` indicates it is a zombie).
- ``<defunct>``: Indicates that this process is no longer running but still exists in the process table as a zombie.
#### How Zombie Processes are Created
- When a child process finishes execution, it sends a **SIGCHLD** signal to the parent process.
- The **parent process** is supposed to read the child's **exit status** using the ``wait()`` or ``waitpid()`` system calls.
- If the parent process does not call ``wait()``, the child process cannot be fully removed from the process table, leaving it as a zombie.
#### Characteristics of a Zombie Process
- **Process ID (PID)** is still in the process table.
- The process does **not use any system resources** (like memory or CPU time) since it has already terminated.
- It appears in ``ps`` output with a status of **"Z"** (for "zombie").
#### Why Zombie Processes Matter
- One or two zombies are usually harmless because they don’t consume system resources.
- **Accumulation** of zombie processes can lead to exhaustion of available PIDs, which can impact system stability and the ability to start new processes.
#### Identifying a Zombie Process
You can find zombie processes using the ``ps`` command:
```bash
ps aux | grep 'Z'
```
Or by looking specifically for the status field "Z":
```bash
ps -eo pid,ppid,stat,cmd | grep 'Z'
```
#### Example of a Zombie Process
Here's a simple scenario:
```bash
#!/bin/bash

# Parent script spawns a child process
( sleep 5 ) &

# Parent does not call wait on the child
# Child completes, becomes a zombie
```
The child process in this script will finish after 5 seconds, but if the parent script doesn't call wait, the child becomes a zombie until the parent terminates.
#### Handling Zombies: To prevent zombie processes:
- Ensure that the parent process uses ``wait()`` or ``waitpid()`` to read the exit status of its child processes.
- Use signal handlers to properly handle ``SIGCHLD`` signals.
#### Cleaning Up Zombie Processes
To remove zombies:
1. **Restart the parent process:** Often, terminating or restarting the parent will force it to collect the child’s exit status, clearing the zombie.
2. **Kill the parent process:** This turns the zombie’s parent into ``init`` (PID 1), which will automatically clean up zombie children.
In more complex systems, parent processes should handle ``SIGCHLD`` signals properly to ``wait()`` for any terminated child processes and prevent zombies from forming.
</details>
<details>
<summary>What is fork() and how to use it</summary>

### System call `fork()`
``fork()`` is a system call in Unix-like operating systems that creates a new process by duplicating the calling process. The new process is called the **child process**, while the original process is referred to as the **parent process**. Both processes will continue execution from the point where the ``fork()`` call was made.

#### How ``fork()`` Works
**1. Process Creation:** When a process calls ``fork()``, the operating system creates a new process. This new process is an exact copy of the parent process, with its own unique Process ID (PID).
2. Return Value:
    + In the **parent process**, ``fork()`` returns the child's PID.
    + In the **child process**, ``fork()`` returns ``0``.
    + If an error occurs, ``fork()`` returns ``-1`` in the parent process, and no child process is created.
**3. Separate Memory Space:** After the fork, both processes execute independently and have separate memory spaces. Changes made by one process do not affect the other.
#### Using ``fork()``
Here's a simple example demonstrating how to use ``fork()`` in a C program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid;
    int status;

    // Create a new process
    pid = fork();

    // Error handling
    if (pid < 0) {
        perror("fork failed");
        return 1; // Exit with an error code
    }

    // This block is executed by the parent process
    if (pid > 0) {
        printf("Parent process, PID: %d\n", getpid());
        printf("Child process created with PID: %d\n", pid);
        
        // Wait for the child process to finish
        wait(&status);
        printf("Child process (PID: %d) exited with status: %d\n", pid, WEXITSTATUS(status));
    }

    // This block is executed by the child process
    else {
        printf("Child process, PID: %d, Parent PID: %d\n", getpid(), getppid());
        // Simulate some work in the child process
        sleep(2); // The child will sleep for 2 seconds
        exit(0);  // The child exits successfully
    }

    return 0; // Both parent and child will reach this point
}
```
#### Key Points
- **Process Isolation:** Each process has its own memory space, and they can run concurrently.
- **Use Cases:** Commonly used to create new processes for handling tasks such as executing different programs or handling client requests in server applications.
- **Zombie Processes:** If the parent process does not call ``wait()`` or ``waitpid()`` after a child process exits, the child can become a zombie process.

</details>
<details>
<summary></summary>
</details>
<details>
<summary></summary>
</details>

## Tasks
### 0. What is my PID
Write a Bash script that displays its own PID.
```bash
$ ./0-what-is-my-pid
4120
```
### 1. List your processes
Write a Bash script that displays a list of currently running processes.
Requirements:
- Must show all processes, for all users, including those which might not have a TTY
- Display in a user-oriented format
- Show process hierarchy
```bash
$ ./1-list_your_processes | head -50
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         2  0.0  0.0      0     0 ?        S    Feb13   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [ksoftirqd/0]
root         4  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kworker/0:0]
root         5  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    Feb13   0:02  \_ [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    Feb13   0:03  \_ [rcuos/0]
root         9  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [rcu_bh]
root        10  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [rcuob/0]
root        11  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [migration/0]
root        12  0.0  0.0      0     0 ?        S    Feb13   0:02  \_ [watchdog/0]
root        13  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [khelper]
root        14  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kdevtmpfs]
root        15  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [netns]
root        16  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [writeback]
root        17  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kintegrityd]
root        18  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [bioset]
root        19  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kworker/u3:0]
root        20  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kblockd]
root        21  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [ata_sff]
root        22  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [khubd]
root        23  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [md]
root        24  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [devfreq_wq]
root        25  0.0  0.0      0     0 ?        S    Feb13   0:41  \_ [kworker/0:1]
root        27  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [khungtaskd]
root        28  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [vmstat]
root        30  0.0  0.0      0     0 ?        SN   Feb13   0:00  \_ [ksmd]
root        31  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [fsnotify_mark]
root        32  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [ecryptfs-kthrea]
root        33  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [crypto]
root        45  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kthrotld]
root        46  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kworker/u2:1]
root        65  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [deferwq]
root        66  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [charger_manager]
root       108  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kpsmoused]
root       125  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [scsi_eh_0]
root       126  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kworker/u2:2]
root       172  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [jbd2/sda1-8]
root       173  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [ext4-rsv-conver]
root       409  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [iprt]
root       549  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [kworker/u3:1]
root       808  0.0  0.0      0     0 ?        S    Feb13   0:00  \_ [kauditd]
root       834  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [rpciod]
root       846  0.0  0.0      0     0 ?        S<   Feb13   0:00  \_ [nfsiod]
root         1  0.0  0.4  33608  2168 ?        Ss   Feb13   0:00 /sbin/init
root       373  0.0  0.0  19472   408 ?        S    Feb13   0:00 upstart-udev-bridge --daemon
root       378  0.0  0.2  49904  1088 ?        Ss   Feb13   0:00 /lib/systemd/systemd-udevd --daemon
root       518  0.0  0.1  23416   644 ?        Ss   Feb13   0:00 rpcbind
statd      547  0.0  0.1  21536   852 ?        Ss   Feb13   0:00 rpc.statd -L
```
### 2. Show your Bash PID
Using your previous exercise command, write a Bash script that displays lines containing the ``bash`` word, thus allowing you to easily get the PID of your Bash process.
Requirements:
- You cannot use ``pgrep``
- The third line of your script must be ``# shellcheck disable=SC2009`` (for more info about ignoring ``shellcheck`` error [here](https://github.com/koalaman/shellcheck/wiki/Ignore))
```bash
$ ./2-show_your_bash_pid
sylvain   4404  0.0  0.7  21432  4000 pts/0    Ss   03:32   0:00          \_ -bash
sylvain   4477  0.0  0.2  11120  1352 pts/0    S+   03:40   0:00              \_ bash ./2-show_your_bash_PID
sylvain   4479  0.0  0.1  10460   912 pts/0    S+   03:40   0:00                  \_ grep bash
```
Here we can see that my Bash PID is ``4404``.

### 3. Show your Bash PID made easy
Write a Bash script that displays the PID, along with the process name, of processes whose name contain the word ``bash``.
Requirements:
- You cannot use ``ps``
```bash
$ ./3-show_your_bash_pid_made_easy
4404 bash
4555 bash
$ ./3-show_your_bash_pid_made_easy
4404 bash
4557 bash
```
Here we can see that:
- For the first iteration: ``bash`` PID is ``4404`` and that the ``3-show_your_bash_pid_made_easy`` script PID is ``4555``
- For the second iteration: ``bash`` PID is ``4404`` and that the ``3-show_your_bash_pid_made_easy`` script PID is ``4557``

### 4. To infinity and beyond
Write a Bash script that displays ``To infinity and beyond`` indefinitely.
Requirements:
- In between each iteration of the loop, add a ``sleep 2``
```bash
$ ./4-to_infinity_and_beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
^C
```
Note that I ``ctrl+c`` (killed) the Bash script in the example.

### 5. Don't stop me now!
We stopped our ``4-to_infinity_and_beyond`` process using ``ctrl+c`` in the previous task, there is actually another way to do this.
Write a Bash script that stops ``4-to_infinity_and_beyond`` process.
Rquirements:
- You must use kill

Terminal #0
```bash
$ ./4-to_infinity_and_beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
Terminated
``` 
Terminal #1
```bash
$ ./5-dont_stop_me_now 
```
I opened 2 terminals in this example, started by running my ``4-to_infinity_and_beyond`` Bash script in terminal #0 and then moved on terminal #1 to run ``5-dont_stop_me_now``. We can then see in terminal #0 that my process has been terminated.

### 6. Stop me if you can
Write a Bash script that stops ``4-to_infinity_and_beyond`` process.
Requirements:
- You cannot use ``kill`` or ``killall``

Terminal #0
```bash
$ ./4-to_infinity_and_beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
Terminated
```
Terminal #1
```bash
$ ./6-stop_me_if_you_can
```
I opened 2 terminals in this example, started by running my ``4-to_infinity_and_beyond`` Bash script in terminal #0 and then moved on terminal #1 to run ``6-stop_me_if_you_can``. We can then see in terminal #0 that my process has been terminated.

### 7. Highlander
Write a Bash script that displays:
- ``To infinity and beyond`` indefinitely
- With a ``sleep 2`` in between each iteration
- ``I am invincible!!!`` when receiving a ``SIGTERM`` signal

Make a copy of your ``6-stop_me_if_you_can`` script, name it ``67-stop_me_if_you_can``, that kills the ``7-highlander`` process instead of the ``4-to_infinity_and_beyond`` one.

Terminal #0
```bash
$ ./7-highlander
To infinity and beyond
To infinity and beyond
I am invincible!!!
To infinity and beyond
I am invincible!!!
To infinity and beyond
To infinity and beyond
To infinity and beyond
I am invincible!!!
To infinity and beyond
^C
```
Terminal #1
```bash
$ ./67-stop_me_if_you_can 
$ ./67-stop_me_if_you_can
$ ./67-stop_me_if_you_can
```
I started ``7-highlander`` in Terminal #0 and then run ``67-stop_me_if_you_can`` in terminal #1, for every iteration we can see ``I am invincible!!!`` appearing in terminal #0.
 
### 8. Beheaded process
Write a Bash script that kills the process ``7-highlander``.

Terminal #0
```bash
$ ./7-highlander 
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
Killed
```
Terminal #1
```bash
$ ./8-beheaded_process
```
I started ``7-highlander`` in Terminal #0 and then run ``8-beheaded_process`` in terminal #1 and we can see that the ``7-highlander`` has been killed.

### 9. Process and PID file
Write a Bash script that:
- Creates the file ``/var/run/myscript.pid`` containing its PID
- Displays ``To infinity and beyond`` indefinitely
- Displays ``I hate the kill command`` when receiving a SIGTERM signal
- Displays ``Y U no love me?!`` when receiving a SIGINT signal
- Deletes the file ``/var/run/myscript.pid`` and terminates itself when receiving a SIGQUIT or SIGTERM signal
```bash
$ sudo ./100-process_and_pid_file
To infinity and beyond
To infinity and beyond
^CY U no love me?!
```
Executing the ``100-process_and_pid_file`` script and killing it with ``ctrl+c``.

Terminal #0
```bash
$ sudo ./100-process_and_pid_file
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
To infinity and beyond
I hate the kill command
```
Terminal #1
```bash
$ sudo pkill -f 100-process_and_pid_file
```
Starting ``100-process_and_pid_file`` in the terminal #0 and then killing it in the terminal #1.

### 10. Manage my process
Read:
- [&](https://bashitout.com/2013/05/18/Ampersands-on-the-command-line.html)
- [init.d](https://www.ghacks.net/2009/04/04/get-to-know-linux-the-etcinitd-directory/)
- [Daemon](https://en.wikipedia.org/wiki/Daemon_%28computing%29)
- [Positional parameters](https://www.gnu.org/software/bash/manual/html_node/Positional-Parameters.html)

man: `sudo`

Programs that are detached from the terminal and running in the background are called daemons or processes, need to be managed. The general minimum set of instructions is: ``start``, ``restart`` and ``stop``. The most popular way of doing so on Unix system is to use the init scripts.
Write a ``manage_my_process`` Bash script that:
- Indefinitely writes ``I am alive!`` to the file ``/tmp/my_process``
- In between every ``I am alive!`` message, the program should pause for 2 seconds

Write Bash (init) script ``101-manage_my_process`` that manages ``manage_my_process``. (both files need to be pushed to git)
Requirements:
- When passing the argument ``start``:
    + Starts ``manage_my_process``
    + Creates a file containing its PID in ``/var/run/my_process.pid``
    + Displays ``manage_my_process started``
- When passing the argument ``stop``:
    + Stops ``manage_my_process``
    + Deletes the file ``/var/run/my_process.pid``
    + Displays ``manage_my_process stopped``
- When passing the argument ``restart``
    + Stops ``manage_my_process``
    + Deletes the file ``/var/run/my_process.pid``
    + Starts ``manage_my_process``
    + Creates a file containing its PID in ``/var/run/my_process.pid``
    + Displays ``manage_my_process restarted``
- Displays ``Usage: manage_my_process {start|stop|restart}`` if any other argument or no argument is passed

Note that this init script is far from being perfect (but good enough for the sake of manipulating process and PID file), for example we do not handle the case where we check if a process is already running when doing ``./101-manage_my_process start``, in our case it will simply create a new process instead of saying that it is already started.
```bash
$ sudo ./101-manage_my_process
Usage: manage_my_process {start|stop|restart}
$ sudo ./101-manage_my_process start
manage_my_process started
$ tail -f -n0 /tmp/my_process 
I am alive!
I am alive!
I am alive!
I am alive!
^C
$ sudo ./101-manage_my_process stop
manage_my_process stopped
$ cat /var/run/my_process.pid 
cat: /var/run/my_process.pid: No such file or directory
$ tail -f -n0 /tmp/my_process 
^C
$ sudo ./101-manage_my_process start
manage_my_process started
$ cat /var/run/my_process.pid 
11864
$ sudo ./101-manage_my_process restart
manage_my_process restarted
$ cat /var/run/my_process.pid 
11918
$ tail -f -n0 /tmp/my_process 
I am alive!
I am alive!
I am alive!
^C
```
### 11. Zombie
Read [what a zombie process is](https://zombieprocess.wordpress.com/what-is-a-zombie-process/).

Write a C program that creates 5 zombie processes.
Requirements:
- For every zombie process created, it displays ``Zombie process created, PID: ZOMBIE_PID``
- Your code should use the Betty style. It will be checked using ``betty-style.pl`` and ``betty-doc.pl``
- When your code is done creating the parent process and the zombies, use the function bellow
```c
int infinite_while(void)
{
    while (1)
    {
        sleep(1);
    }
    return (0);
}
```
Example:
Terminal #0
```bash
$ gcc 102-zombie.c -o zombie
$ ./zombie 
Zombie process created, PID: 13527
Zombie process created, PID: 13528
Zombie process created, PID: 13529
Zombie process created, PID: 13530
Zombie process created, PID: 13531
^C
```
Terminal #1
```bash
$ ps aux | grep -e 'Z+.*<defunct>'
sylvain  13527  0.0  0.0      0     0 pts/0    Z+   01:19   0:00 [zombie] <defunct>
sylvain  13528  0.0  0.0      0     0 pts/0    Z+   01:19   0:00 [zombie] <defunct>
sylvain  13529  0.0  0.0      0     0 pts/0    Z+   01:19   0:00 [zombie] <defunct>
sylvain  13530  0.0  0.0      0     0 pts/0    Z+   01:19   0:00 [zombie] <defunct>
sylvain  13531  0.0  0.0      0     0 pts/0    Z+   01:19   0:00 [zombie] <defunct>
sylvain  13533  0.0  0.1  10460   964 pts/2    S+   01:19   0:00 grep --color=auto -e Z+.*<defunct>
```
In Terminal #0, I start by compiling ``102-zombie.c`` and executing ``zombie`` which creates 5 zombie processes. In Terminal #1, I display the list of processes and look for lines containing ``Z+.*<defunct>`` which catches zombie process.