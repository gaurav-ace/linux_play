import subprocess
import re
import os
import csv
import time

# this is to get the output from top command
def get_top_output():
    result = subprocess.run(
        ["top", "-b", "-n", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
    return result.stdout




#  our focus is on these lines ( data is for example) :
#    %Cpu(s):  7.2 us,  1.3 sy,  0.0 ni, 91.0 id
#    MiB Mem :  15947.0 total,  10234.1 free,  3456.2 used


# this is to extract the cpu and mem info
def parse_cpu_mem_usage(top_output):

    cpu_usage = None
    mem_used = None
    mem_free = None

    #split the top output in lines and parse
    for line in top_output.splitlines():
        
        if "%Cpu(s)" in line:
            # extract the id(idle time) and calculate cpu usage
            idle = float(re.search(r"(\d+\.\d+)\s*id", line).group(1))
            cpu_usage = 100.0 - idle


        if "MiB Mem" in line:
            numbers = re.findall(r"(\d+\.\d+)", line)
            total, free, used  = map(float, numbers[:3])
            mem_used = used
            mem_free = free
    
    return cpu_usage, mem_used, mem_free

# this is to log the data in a csv file
def log_stats(cpu_usage, mem_used, mem_free):
    with open("syslog.csv", "a", newline="") as f:
        writer = csv.writer(f);
        writer.writerow([time.time(), cpu_usage, mem_used, mem_free])


def init_csv():
    if not os.path.exists("syslog.csv"):
        with open("syslog.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "cpu_usage", "mem_used_mb", "mem_free_mb"])


init_csv() # called once

while True:
    output = get_top_output()
    cpu, used, free = parse_cpu_mem_usage(output)
    print("DEBUG:", cpu, used, free)
    log_stats(cpu, used, free)
    time.sleep(1)



