defaults = {"theme": "dark", "tags": ["new"]}
user_a = defaults.copy()
user_a["tags"].append("beta")

print("1. shallow copy, then append")
print("   defaults:", defaults)
print("   user_a  :", user_a)
print("   same inner list?", user_a["tags"] is defaults["tags"])

nested = [["a"], ["b"]]
clones = [list(nested), nested[:], nested.copy()]
print("inner lists shared with the original:", [c[0] is nested[0] for c in clones])

import copy

defaults = {"theme": "dark", "tags": ["new"]}
user_b = copy.deepcopy(defaults)
user_b["tags"].append("beta")

print("2. deepcopy, then append")
print("   defaults:", defaults)
print("   user_b  :", user_b)

defaults = {"theme": "dark", "tags": ["new"]}
user_c = defaults.copy()
user_c["theme"] = "light"
user_c["tags"] = user_c["tags"] + ["beta"]

print("3. shallow copy, but rebind instead of mutate")
print("   defaults:", defaults)
print("   user_c  :", user_c)

grid = [[0] * 3] * 3
grid[0][0] = 9
print("repeated rows ->", grid)

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print("comprehension   ->", grid)

import copy
import time

rows = [list(range(100)) for _ in range(2000)]
times = []
for _ in range(10):
    start = time.perf_counter()
    copy.deepcopy(rows)
    times.append((time.perf_counter() - start) * 1000)
print(f"deepcopy of 2,000 lists of 100 ints: {min(times):.0f} to {max(times):.0f} ms over 10 runs")

loop = [1]
loop.append(loop)
clone = copy.deepcopy(loop)
print("self-referencing list deep-copied fine:", clone[1] is clone and clone is not loop)

