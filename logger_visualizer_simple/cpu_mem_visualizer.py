import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("syslog.csv")

plt.plot(df["timestamp"], df["cpu_usage"], label="CPU %")
plt.plot(df["timestamp"], df["mem_used_mb"], label="Memory Used (MB)")
plt.plot(df["timestamp"], df["mem_free_mb"], label="Memory Free (MB)")
plt.legend()
plt.show()

