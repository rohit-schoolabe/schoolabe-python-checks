import random
from collections import OrderedDict, deque

def fifo(refs, frames):
    q, mem, faults, trace = deque(), set(), 0, []
    for p in refs:
        if p in mem:
            trace.append("hit")
        else:
            faults += 1
            if len(mem) == frames:
                mem.remove(q.popleft())
            q.append(p)
            mem.add(p)
            trace.append("F")
    return faults, trace

def lru(refs, frames):
    mem, faults, trace = OrderedDict(), 0, []
    for p in refs:
        if p in mem:
            mem.move_to_end(p)
            trace.append("hit")
        else:
            faults += 1
            if len(mem) == frames:
                mem.popitem(last=False)
            mem[p] = True
            trace.append("F")
    return faults, trace

def opt(refs, frames):
    mem, faults, trace = [], 0, []
    for i, p in enumerate(refs):
        if p in mem:
            trace.append("hit")
            continue
        faults += 1
        trace.append("F")
        if len(mem) < frames:
            mem.append(p)
            continue
        rest = refs[i + 1:]
        # evict the page whose next use is furthest away (or never)
        victim = max(mem, key=lambda x: rest.index(x) if x in rest else float("inf"))
        mem.remove(victim)
        mem.append(p)
    return faults, trace

lesson = [1, 2, 3, 4, 1, 2, 5, 1, 2]
print("Lesson string with 3 frames:", lesson)
for name, policy in (("FIFO", fifo), ("LRU", lru), ("OPT", opt)):
    n, t = policy(lesson, 3)
    print(f"  {name}: {n} faults   {' '.join(t)}")
print("FIFO on the same string with 4 frames:", fifo(lesson, 4)[0], "faults")

belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
print("Classic string:", belady)
for name, policy in (("FIFO", fifo), ("LRU", lru)):
    for frames in (3, 4):
        print(f"  {name}, {frames} frames: {policy(belady, frames)[0]} faults")

random.seed(2026)
trials, bad_fifo, bad_lru = 1_000_000, 0, 0
for _ in range(trials):
    refs = [random.randint(1, 5) for _ in range(12)]
    if fifo(refs, 4)[0] > fifo(refs, 3)[0]:
        bad_fifo += 1
    if lru(refs, 4)[0] > lru(refs, 3)[0]:
        bad_lru += 1
print(f"{trials:,} random strings, 12 refs over pages 1-5, 3 frames vs 4:")
print(f"  FIFO faulted more with 4 frames: {bad_fifo}")
print(f"  LRU faulted more with 4 frames:  {bad_lru}")
