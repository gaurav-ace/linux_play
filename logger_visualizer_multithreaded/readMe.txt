There is one lighter version of same project in this repo : logger_visualiser_simple (using top and logging in .csv file)


However, using top and CSV had high overhead and poor real-time behavior—

1) top requires spawning a process and parsing unstable text output,
2) CSV introduces disk I/O, latency, and race conditions between writer and reader.

By switching to /proc :
1) we read stable, kernel-provided metrics directly with minimal overhead.
2) And by using multithreading with an in-memory queue, we removed disk I/O from the hot path and enabled true real-time updates with clean separation between data collection and UI.


A multithreaded Linux system monitor using /proc, where a producer thread collects kernel stats and a consumer thread renders a live terminal UI using a thread-safe queue.

┌──────────────┐
│ Collector    │  reads /proc
│ Thread       │
└──────┬───────┘
       │   puts data
       ▼
   ┌────────┐
   │ Queue  │   (thread-safe)
   └────────┘
       ▲
       │ gets data
┌──────┴───────┐
│ UI Thread    │  displays live
└──────────────┘

