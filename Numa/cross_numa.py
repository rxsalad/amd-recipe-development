import subprocess
import time
from collections import defaultdict

# -------- CONFIG --------
PIDS = [1, 616, 617, 767, 768, 769, 770, 771, 772, 773, 774]
INTERVAL = 1      # seconds
ITERATIONS = 3600

# NUMA boundary for MI350, 192 cores total
NODE0_MAX = 95
NODE1_MIN = 96

# NUMA boundary for MI325, 160 cores total
# NODE0_MAX = 79
# NODE1_MIN = 80


def get_numa_node(psr):
    if psr <= NODE0_MAX:
        return 0
    else:
        return 1


def get_ps_data(pids):
    pid_str = ",".join(str(p) for p in pids)

    cmd = ["ps", "-o", "pid,psr,comm", "-p", pid_str]

    print(f"\nRunning command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    lines = result.stdout.strip().split("\n")[1:]  # skip header

    data = {}

    for line in lines:
        parts = line.split(None, 2)
        pid = int(parts[0])
        psr = int(parts[1])
        comm = parts[2]

        data[pid] = {
            "psr": psr,
            "node": get_numa_node(psr),
            "comm": comm
        }

    return data


# -------- TRACKING STRUCTURES --------

prev = {}
psr_changes = defaultdict(int)
node_changes = defaultdict(int)


# -------- MAIN LOOP --------

for i in range(ITERATIONS):

    current = get_ps_data(PIDS)

    if i > 0:
        for pid in current:

            if pid not in prev:
                continue

            # PSR change
            if current[pid]["psr"] != prev[pid]["psr"]:
                psr_changes[pid] += 1

            # NUMA node change
            if current[pid]["node"] != prev[pid]["node"]:
                node_changes[pid] += 1

    prev = current

    if i < ITERATIONS - 1:
        time.sleep(INTERVAL)


    # -------- PRINT RESULTS --------

    print(f"\nRESULTS ({(i+1)*INTERVAL} seconds, sampling at the interval of {INTERVAL} second):\n")
    print(f"{'PID':>6} {'COMMAND':>25} {'Current_CPU_Core':>15} {'Current_NUMA_Node':>15} {'CPU_Core_changes':>15} {'NUMA_changes':>15}")

    for pid in sorted(PIDS):
 
        comm = prev.get(pid, {}).get("comm", "N/A")
        current_psr = prev.get(pid, {}).get("psr", "N/A")
        current_node = prev.get(pid, {}).get("node", "N/A")

        print(f"{pid:>6} {comm:>20} {current_psr:>15} {current_node:>15} {psr_changes[pid]:>15} {node_changes[pid]:>15}")

