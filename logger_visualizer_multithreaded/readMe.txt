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

