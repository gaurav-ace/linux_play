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

