import time
import csv
from rich.console import Console
from rich.live import Live
from rich.table import Table

CSV_PATH = "syslog.csv"

console = Console()

def read_latest_row():
    with open(CSV_PATH, "r") as f:
        rows = list(csv.reader(f))
        if len(rows) < 2:
            return None
        return rows[-1]

def bar(percent, width=20):
    filled = int((percent / 100) * width)
    return "█" * filled + "░" * (width - filled)


def render_table(cpu, mem_used, mem_free):
    table = Table(title="System Monitor")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    #table.add_row("CPU Usage (%)", f"{cpu:.2f}")
    #table.add_row("Memory Used (MB)", f"{mem_used:.2f}")
    #table.add_row("Memory Free (MB)", f"{mem_free:.2f}")

    cpu_style = "green" if cpu < 50 else "yellow" if cpu < 80 else "red"
    table.add_row("CPU", f"[{cpu_style}]{bar(cpu)} {cpu:.1f}%[/{cpu_style}]")

    # crude normalization for memory bar
    mem_percent = (mem_used / (mem_used + mem_free)) * 100
    table.add_row("MEM", f"[{cpu_style}]{bar(mem_percent)} {mem_percent:.1f}%[/{cpu_style}]")
       
    return table

with Live(console=console, refresh_per_second=1) as live:
    while True:
        row = read_latest_row()
        if row:
            _, cpu, mem_used, mem_free = map(float, row)
            live.update(render_table(cpu, mem_used, mem_free))
        time.sleep(1)

