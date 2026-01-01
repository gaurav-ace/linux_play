from queue import Queue
import time

def read_cpu_stats():
    """
    Reads the first 'cpu' line from /proc/stat.

    Returns:
        total_time: sum of all CPU time fields
        idle_time: idle CPU time
    """    

    with open("/proc/stat", "r") as f:
        line = f.readline()          # read first line only
        parts = line.split()         # split by whitespace

        values = list(map(int, parts[1:]))
        idle_time = values[3]
        total_time = sum(values)

        return total_time, idle_time


def read_mem_info():
    """
    Reads memory info from /proc/meminfo.

    Returns:
        used_mb: used memory in MB
        free_mb: available memory in MB
    """
    meminfo = {}

    with open("/proc/meminfo", "r") as f:
        for line in f:
            key,val = line.split(":")
            meminfo[key] = int(val.strip().split()[0])
            
    mem_total = meminfo["MemTotal"]          # in kb
    mem_available = meminfo["MemAvailable"]  # in kb
    
    mem_used  = mem_total - mem_available

    return mem_used / 1024, mem_available / 1024     # convert to MB


def collector(queue):
    """
    Runs in a separate thread.
    Periodically reads CPU and memory stats
    and puts them into the queue.
    """

    prev_total, prev_idle = read_cpu_stats()

    while True:
        time.sleep(1)

        cur_total, cur_idle = read_cpu_stats()

        total_diff = cur_total - prev_total
        idle_diff = cur_idle - prev_idle

        cpu_usage = (total_diff - idle_diff)/ total_diff * 100

        prev_total = cur_total
        prev_idle = cur_idle

        # mem usage
        mem_used, mem_free = read_mem_info()
        
        # put a tuple into queue (thread-safe)
        queue.put((cpu_usage, mem_used, mem_free))



