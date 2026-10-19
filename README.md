# schoolabe-python-checks

Code from the Schoolabe dev articles. Each folder holds the script behind one article and the output the script printed when it was run.

Schoolabe ([schoolabe.com](https://www.schoolabe.com)) is a free coding practice site. This repository belongs to its team.

All outputs below came from Python 3.13.5. The C program was built with gcc 14.2 (`gcc -O2`). The scripts use only the standard library.

## belady

Article: [Belady's Anomaly: FIFO vs LRU vs Optimal, Checked in Python](https://dev.to/realdev9868/beladys-anomaly-fifo-vs-lru-vs-optimal-checked-in-python-5f3m)

`belady/belady.py` implements FIFO, LRU and optimal page replacement. It runs them on two reference strings, then on 1,000,000 random strings (12 references over pages 1 to 5, random seed 2026) and counts how often 4 frames fault more than 3.

```
python3 belady/belady.py
```

Output:

```
Lesson string with 3 frames: [1, 2, 3, 4, 1, 2, 5, 1, 2]
  FIFO: 7 faults   F F F F F F F hit hit
  LRU: 7 faults   F F F F F F F hit hit
  OPT: 5 faults   F F F F hit hit F hit hit
FIFO on the same string with 4 frames: 7 faults
Classic string: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
  FIFO, 3 frames: 9 faults
  FIFO, 4 frames: 10 faults
  LRU, 3 frames: 10 faults
  LRU, 4 frames: 8 faults
1,000,000 random strings, 12 refs over pages 1-5, 3 frames vs 4:
  FIFO faulted more with 4 frames: 1
  LRU faulted more with 4 frames:  0
```

The run took about 8 seconds. The random part is repeatable with the fixed seed, but the count is for Python 3.13.5 only. Other versions were not checked.

`belady/exhaustive.c` checks every possible string instead of sampling. There are 5^12 of them.

```
gcc -O2 -o exhaustive belady/exhaustive.c
./exhaustive
```

Output:

```
strings: 244140625
FIFO worse with 4 frames than 3: 120
1 in 2034505
```

The run took about 30 seconds. So 120 of the 244,140,625 strings make FIFO fault more with 4 frames, which is the anomaly. The sample above found 1 in a million, which is the same order of magnitude as the exact rate of about 0.5 per million.

## python-copy-bug

Article: [The Python Copy Bug That Looks Fine in Code Review](https://dev.to/realdev9868/the-python-copy-bug-that-looks-fine-in-code-review-9k)

`python-copy-bug/copy_bug.py` shows a shallow copy sharing an inner list, the same thing with `list(x)`, `x[:]` and `x.copy()`, the `deepcopy` fix, a shallow copy that is safe because it rebinds instead of mutating, the grid-of-zeros bug, and a rough timing of `deepcopy`.

```
python3 python-copy-bug/copy_bug.py
```

Output:

```
1. shallow copy, then append
   defaults: {'theme': 'dark', 'tags': ['new', 'beta']}
   user_a  : {'theme': 'dark', 'tags': ['new', 'beta']}
   same inner list? True
inner lists shared with the original: [True, True, True]
2. deepcopy, then append
   defaults: {'theme': 'dark', 'tags': ['new']}
   user_b  : {'theme': 'dark', 'tags': ['new', 'beta']}
3. shallow copy, but rebind instead of mutate
   defaults: {'theme': 'dark', 'tags': ['new']}
   user_c  : {'theme': 'light', 'tags': ['new', 'beta']}
repeated rows -> [[9, 0, 0], [9, 0, 0], [9, 0, 0]]
comprehension   -> [[9, 0, 0], [0, 0, 0], [0, 0, 0]]
deepcopy of 2,000 lists of 100 ints: 25 to 29 ms over 10 runs
self-referencing list deep-copied fine: True
```

The timing line changes from run to run. Earlier runs gave 26 to 35 ms. Every other line is the same each time.

The script only tests lists, dicts and ints. Classes with their own `__copy__` or `__deepcopy__` methods, and objects that hold file handles or locks, are not covered.

## Files

```
belady/belady.py
belady/exhaustive.c
belady/output.txt
belady/exhaustive-output.txt
python-copy-bug/copy_bug.py
python-copy-bug/output.txt
```

`output.txt` files are the raw output of the matching script.
