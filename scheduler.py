# CPU Scheduling Simulator (Simple Version)

# Input
def gantt_fcfs(p):
    p.sort(key=lambda x: x[1])
    t = 0
    chart = ""

    for x in p:
        if t < x[1]:
            t = x[1]

        start = t
        t += x[2]
        end = t

        chart += f"| {x[0]} "

    chart += "|"

    print("\nGantt Chart (FCFS):")
    print(chart)

    # time line
    t = 0
    times = "0"
    for x in p:
        t += x[2]
        times += f"   {t}"
    print(times)
n = int(input("Enter number of processes: "))

proc = []

for i in range(n):
    at = int(input(f"P{i+1} Arrival Time: "))
    bt = int(input(f"P{i+1} Burst Time: "))
    pr = int(input(f"P{i+1} Priority: "))

    proc.append([f"P{i+1}", at, bt, pr])


# FCFS
def fcfs(p):
    p.sort(key=lambda x: x[1])
    t = 0
    print("\nFCFS:")

    for x in p:
        if t < x[1]:
            t = x[1]

        t += x[2]
        ct = t
        tat = ct - x[1]
        wt = tat - x[2]

        print(x[0], "CT:", ct, "TAT:", tat, "WT:", wt)


# SJF
def sjf(p):
    p2 = p.copy()
    t = 0
    done = []
    print("\nSJF:")

    while len(done) < len(p2):
        ready = [x for x in p2 if x[1] <= t and x not in done]

        if not ready:
            t += 1
            continue

        x = min(ready, key=lambda x: x[2])

        t += x[2]
        ct = t
        tat = ct - x[1]
        wt = tat - x[2]

        print(x[0], "CT:", ct, "TAT:", tat, "WT:", wt)
        done.append(x)


# Priority
def priority(p):
    p2 = p.copy()
    t = 0
    done = []
    print("\nPriority:")

    while len(done) < len(p2):
        ready = [x for x in p2 if x[1] <= t and x not in done]

        if not ready:
            t += 1
            continue

        x = min(ready, key=lambda x: x[3])

        t += x[2]
        ct = t
        tat = ct - x[1]
        wt = tat - x[2]

        print(x[0], "CT:", ct, "TAT:", tat, "WT:", wt)
        done.append(x)


# Round Robin
def rr(p, q):
    queue = sorted(p, key=lambda x: x[1])
    t = 0
    rem = {x[0]: x[2] for x in p}
    done = {}

    print("\nRound Robin:")

    while queue:
        x = queue.pop(0)

        if t < x[1]:
            t = x[1]

        run = min(q, rem[x[0]])
        t += run
        rem[x[0]] -= run

        if rem[x[0]] > 0:
            queue.append(x)
        else:
            done[x[0]] = t

    for x in p:
        ct = done[x[0]]
        tat = ct - x[1]
        wt = tat - x[2]

        print(x[0], "CT:", ct, "TAT:", tat, "WT:", wt)


# Run all
fcfs(proc.copy())
sjf(proc.copy())
priority(proc.copy())
rr(proc.copy(), 2)
gantt_fcfs(proc.copy())
