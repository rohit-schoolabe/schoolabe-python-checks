/* Count strings of 12 references over pages 1..5 where FIFO with 4 frames
   faults MORE than FIFO with 3 frames. Exhaustive: 5^12 strings. */
#include <stdio.h>
static int fifo(const int *r, int n, int frames) {
    int mem[8], head = 0, used = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int hit = 0;
        for (int j = 0; j < used; j++) if (mem[j] == r[i]) { hit = 1; break; }
        if (hit) continue;
        faults++;
        if (used < frames) mem[used++] = r[i];
        else { mem[head] = r[i]; head = (head + 1) % frames; }
    }
    return faults;
}
int main(void) {
    long total = 1, bad = 0;
    for (int i = 0; i < 12; i++) total *= 5;
    int r[12];
    for (long x = 0; x < total; x++) {
        long y = x;
        for (int i = 0; i < 12; i++) { r[i] = (int)(y % 5) + 1; y /= 5; }
        if (fifo(r, 12, 4) > fifo(r, 12, 3)) bad++;
    }
    printf("strings: %ld\nFIFO worse with 4 frames than 3: %ld\n1 in %.0f\n", total, bad, (double)total / bad);
    return 0;
}
