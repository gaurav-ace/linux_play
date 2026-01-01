import threading
from queue import Queue
import ui
import collector
import time

def main():
    q = Queue()

    collector_thread = threading.Thread(
        target=collector.collector,
        args=(q,),
        daemon=True        # exits when main exits
    )

    ui_thread = threading.Thread(
        target=ui.ui,
        args=(q,),
        daemon=True
    )

    collector_thread.start()
    ui_thread.start()

    # keep main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

