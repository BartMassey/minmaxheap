# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


"""
Min-Max Heap

A min-max heap (double-ended priority heap) allows
efficient extraction of either min or max elements.

Implementation of pseudocode from

  Min-Max Heaps and Generalized Priority Queues
  M.D. Atkinson, J.-R. Sack, N. Santoro, T. Strothotte
  Comms ACM 29(10) p. 996, October 1986
  http://cglab.ca/~morin/teaching/5408/refs/minmax.pdf

See also

  Diamond deque: a simple data structure for priority deques
  S.C. Chang, M.W. Du
  Info Proc Letters 46(5) p. 231, July 1993

for what would probably be a cleaner and easier data structure.
"""

import random

class MinMaxHeap(object):
    def __init__(self, a, start=0, end=None, lt=None):
        """Create a new heap with the given start and end
           elements (end is actually size, i.e. last element
           plus one) and comparison function."""
        self.a = a
        self.start = start
        if end == None:
            end = len(a) - start
        self.end = end
        assert self.end >= self.start
        if lt == None:
            lt = lambda x, y: x < y
        self.lt = lt
        self.gt = lambda x, y: lt(y, x)
        if self.end > self.start + 1:
            self.heapify()

    def swap(self, i, j):
        "Exchange a[i] with a[j]."
        self.a[i], self.a[j] = self.a[j], self.a[i] 

    def is_min_level(self, index):
        "Tree level of index is some min level."
        index = index - self.start + 1
        return (index.bit_length() & 1) == 1

    def downheap(self, i=None):
        "Downheap minmax heap a starting at position i."
        if i == None:
            i = self.start
        assert i >= self.start and i < self.end
        i0 = i
        if self.is_min_level(i):
            cf = self.lt
        else:
            cf = self.gt
        left = 2 * i + 1
        while left < self.end:
            right = left + 1
            nexti = left
            for c in [right, 2*left+1, 2*left+2, 2*right+1, 2*right+2]:
                if c >= self.end:
                    break
                if cf(self.a[c], self.a[nexti]):
                    nexti = c
            if nexti <= right:
                if cf(self.a[nexti], self.a[i]):
                    self.swap(nexti, i)
                return
            else:
                if cf(self.a[nexti], self.a[i]):
                    self.swap(nexti, i)
                    parent = (nexti - 1) // 2
                    if cf(self.a[parent], self.a[nexti]):
                        self.swap(nexti, parent)
                else:
                    return
            i = nexti
            left = 2 * i + 1

    def upheap(self, i=None):
        "Upheap minmax heap starting at position i."
        if i == None:
            i = self.end - 1
        assert i >= self.start and i < self.end
        if i == self.start:
            return
        parent = (i - 1) // 2
        if self.is_min_level(i):
            if self.gt(self.a[i], self.a[parent]):
                self.swap(i, parent)
                i = parent
                cf = self.gt
            else:
                cf = self.lt
        else:
            if self.lt(self.a[i], self.a[parent]):
                self.swap(i, parent)
                i = parent
                cf = self.lt
            else:
                cf = self.gt
        parent = (i - 1) // 2
        grandparent = (parent - 1) // 2
        while i >= 3 and cf(self.a[i], self.a[grandparent]):
            self.swap(i, grandparent)
            i = grandparent
            parent = (i - 1) // 2
            grandparent = (parent - 1) // 2
        
    def increment_end(self):
        "Bump the end pointer toward end-of-heap."
        assert self.end < len(self.a)
        self.end += 1

    def decrement_end(self):
        "Bump the end pointer toward end-of-heap."
        assert self.end > self.start
        self.end -= 1

    def reset(self, start=0, end=None, lt=None):
        """Reset start, end and possibly lt and rebuild
           relevant portion of heap."""
        if end == None:
            end = len(self.a)
        self.start = start
        self.end = end
        assert self.end >= self.start
        if lt != None:
            self.lt = lt
        self.heapify()

    def check_heap(self):
        "Highly inefficient check of heap invariant."

        def children(i):
            if i >= self.end:
                return []
            return children(2 * i + 1) + [(i, self.a[i])] + children(2 * i + 2)

        def check_posn(p):
            if self.is_min_level(p):
                cf = lambda x, y: x == y or self.lt(x, y)
                cfs = "<="
            else:
                cf = lambda x, y: x == y or self.gt(x, y)
                cfs = ">="
            result = True
            for i, ai in children(p):
                if not cf(self.a[p], ai):
                    print("failed a[{}]={} {} a[{}]={}".format(
                        p, self.a[p], cfs, i, ai))
                    result = False
            return result

        ok = True
        for p in range(self.start, self.end):
            ok = ok and check_posn(p)
        assert ok

    def heapify(self):
        "Enforce the heap property on our a."
        for i in reversed(range(self.start, (self.end - 1) // 2 + 1)):
            self.downheap(i)

    def store_min(self):
        "Extract min element and place it after the new end of the heap."
        assert self.end >= self.start
        self.end -= 1
        if self.end <= self.start:
            return
        self.swap(self.start, self.end)
        self.downheap()

    def store_max(self):
        "Extract max element and place it after the new end of the heap."
        assert self.end >= self.start
        if self.end <= self.start + 1:
            return
        imax = self.start + 1
        if self.end > imax + 1 and self.lt(self.a[imax], self.a[imax + 1]):
            imax += 1
        self.end -= 1
        self.swap(imax, self.end)
        if imax < self.end:
            self.downheap(imax)

    def peek_min(self):
        "Return min element."
        assert self.start < self.end
        return self.a[self.start]

    def peek_max(self):
        "Return max element."
        assert self.start < self.end
        if self.start + 1 == self.end:
            return self.a[self.start]
        if self.start + 2 == self.end:
            return self.a[self.start + 1]
        return max(self.a[self.start + 1], self.a[self.start + 2])

    def extract_min(self, shrink=True):
        "Extract and return min element."
        self.store_min()
        if shrink and self.end == len(self.a) - 1:
            return self.a.pop()
        return self.a[self.end]

    def extract_max(self, shrink=True):
        "Extract and return max element."
        self.store_max()
        if shrink and self.end == len(self.a) - 1:
            return self.a.pop()
        return self.a[self.end]

    def insert(self, e, grow=True):
        "Insert element e, maybe overwriting element beyond end."
        if grow and self.end == len(self.a):
            self.a.append(e)
        else:
            assert self.end == len(self.a) - 1
            self.a[self.end] = e
        self.end += 1
        self.upheap(self.end - 1)

    def sort(self, start=0, end=None):
        """Sort the underlying array fragment in-place and return it.
           Returns the whole array if fully sorted, else None.
           Resets start and end if needed."""
        if end == None:
            end = self.end
        if start != self.start or end != self.end:
            self.reset(start=start, end=end)
        if self.start == 0 and self.end == len(self.a):
            result = self.a
        else:
            result = None
        for i in reversed(range(self.start + 1, self.end)):
            self.store_max()
        return result

if __name__ == "__main__":

    s = [chr(ord('a') + i) for i in range(15)]
    random.shuffle(s)
    h = MinMaxHeap(s)
    h.check_heap()
    n = len(s)
    small_half =  n // 2
    for _ in range(small_half, n):
        h.store_max()
    for _ in range(0, small_half):
        h.store_min()
    assert ''.join(s) == "gfedcbahijklmno"

    random.shuffle(s)
    h = MinMaxHeap([])
    for i in range(n):
        h.insert(s[i])
    h.check_heap()
    assert sorted(s) == h.sort()
