from rich.console import Console
from rich.live import Live
from rich.table  import Table

from queue import Queue

def bar(percent, width=20):
    """
    Creates a text progress bar.
    """
    filled = int((percent / 100) * width)   # calcluate the filled percentage
    return "\u2588" * filled + "\u2591" * (width - filled)

    # \u2588 → █ (FULL BLOCK)
    # \u2591 → ░ (LIGHT SHADE)
    

def render(cpu, mem_used, mem_free):

    """
    Builds the UI table.
    """
    table = Table(title="System Monitor")

    table.add_column("Metric")
    table.add_column("Usage")

    table.add_row("CPU", f"{bar(cpu)} {cpu:.1f}%")
    
    mem_percent = (mem_used / (mem_used + mem_free)) * 100
    table.add_row("MEM", f"{bar(mem_percent)} {mem_percent:.1f}%")

    return table


def ui(queue):
   """
   UI thread: consumes data from queue and renders it.
   """
   console = Console()

   with Live(console=console, refresh_per_second=4) as live:
       while True:
           cpu, mem_used, mem_free = queue.get()  # blocks until data available
           live.update(render(cpu, mem_used, mem_free))


