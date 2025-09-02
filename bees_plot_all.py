import numpy as np
import matplotlib.pyplot as plt

_version = "1.0.9"
# Parameters
N0 = 250              # initial botnet size
weeks = 10            # simulation horizon in weeks
days_per_week = 7
days = weeks * days_per_week
n = 1                 # scouting cycles per week
mu_weekly = 0.01      # weekly attrition
simulations = 12      # number of simulation runs

# Growth parameters
mean_r_weekly = 0.25  # mean weekly growth rate
std_r_weekly = 0.05   # weekly growth randomness

# Convert weekly rates to daily rates assuming compounding
mu_daily = 1 - (1 - mu_weekly)**(1/days_per_week)
mean_r_daily = (1 + mean_r_weekly)**(1/days_per_week) - 1
std_r_daily = std_r_weekly / days_per_week  # rough approximation

def simulate_botnet_daily(N, n, mu_daily, days, mean_r_daily, std_r_daily, seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    sizes = [N]
    for t in range(1, days):
        # Daily random growth
        r = np.random.normal(mean_r_daily, std_r_daily)
        r = max(r, 0.001)  # floor to prevent negative growth
        new_size = sizes[-1] * (1 + r)**n - mu_daily * sizes[-1]
        sizes.append(new_size)
    return np.array(sizes)

# Run simulations
all_runs = np.array([simulate_botnet_daily(N0, n, mu_daily, days, mean_r_daily, std_r_daily, seed=i) for i in range(simulations)])
avg_run = all_runs.mean(axis=0)

# Plot
plt.figure(figsize=(12,6))
i = 0;
for run in all_runs:
    if i == len(all_runs) - 1:
        plt.plot(run, color="#6c757d", linewidth=1, alpha=0.3, label="Simulations")
    else:
        plt.plot(run, color="#6c757d", linewidth=1, alpha=0.3)
    i = i + 1
plt.plot(avg_run, color="red", linewidth=2, label="Scouts (Average simulated)")
akamai = np.loadtxt('akamai.csv', delimiter=',')
isp = np.loadtxt('isp1.csv', delimiter=',')

plt.plot(akamai, color="orange", linewidth=2, label="Akamai (measured)", linestyle='dotted')
plt.plot(isp, color="blue", linewidth=2, label="ISP (measured)", linestyle='dashed')
#plt.title("Botnet Growth Simulations (Daily Steps, Smooth Curves)")
plt.xlabel("Time Period (days)")
plt.ylabel("Botnet size")
plt.legend()
plt.grid(True)
plt.show()

print("Average growth (rounded):", np.round(avg_run,0))
