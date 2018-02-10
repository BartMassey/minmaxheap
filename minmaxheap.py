# Copyright (c) 2018 Bart Massey

# Min-Max Heap
#
# Min-Max Heaps and Generalized Priority Queues
# M.D. Atkinson, J.-R. Sack, N. Santoro, T. Strothotte
# Comms ACM 29(10) p. 996, October 1986
# http://cglab.ca/~morin/teaching/5408/refs/minmax.pdf

import random

def even_level(index):
    "Tree level of index."
    index += 1
    return (index.bit_length() & 1) == 1

def downheap(a, start=0, end=None, lt=None):
    "Downheap minmax heap a starting at position i."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y
    if even_level(start):
        cf = lt
    else:
        cf = lambda x, y: lt(y, x)
    while True:
        children = [2 * start + 1, 2 * start + 2]
        nexti = children[0]
        if nexti >= end:
            return
        grandchildren = list(range(4 * start + 3, 4 * start + 7))
        for i in children + grandchildren:
            if i >= end:
                break
            if cf(a[i], a[nexti]):
                nexti = i
        if nexti in children:
            if cf(a[nexti], a[start]):
                a[nexti], a[start] = a[start], a[nexti]
            return
        else:
            if cf(a[nexti], a[start]):
                a[nexti], a[start] = a[start], a[nexti]
                pnexti = (nexti - 1) // 2
                if cf(a[pnexti], a[nexti]):
                    a[nexti], a[pnexti] = a[pnexti], a[nexti]
            else:
                return
        start = nexti


def check_heap(a, start=0, end=None, lt=None):
    "Highly inefficient check of heap invariant."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y

    def children(i):
        if i >= end:
            return []
        return children(2 * i + 1) + [(i, a[i])] + children(2 * i + 2)

    def check_posn(p):
        if even_level(p):
            cf = lambda x, y: x == y or lt(x, y)
            cfs = "<="
        else:
            cf = lambda x, y: x == y or lt(y, x)
            cfs = ">="
        for i, ai in children(p):
            if not cf(a[p], ai):
                print("failed a[{}]={} {} a[{}]={}".format(
                    p, a[p], cfs, i, ai))

    for p in range(start, end):
        check_posn(p)


def heapify(a, lt=None):
    "Make a into a heap."
    end = len(a)
    for i in reversed(range((end-2) // 2 + 1)):
        downheap(a, start=i, lt=lt)
        # check_heap(a, start=i)

def store_min(a, end=None, lt=None):
    "Extract min element and place it after the end of the heap."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y
    assert end > 0
    if end == 1:
        return
    a[0], a[end-1] = a[end-1], a[0]
    downheap(a, end=end-1, lt=lt)

def store_max(a, end=None, lt=None):
    "Extract max element and place it after the end of the heap."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y
    assert end > 0
    if end == 1:
        return
    imax = 1
    if end > 2 and lt(a[1], a[2]):
        imax = 2
    a[imax], a[end-1] = a[end-1], a[imax]
    downheap(a, start=imax, end=end-1, lt=lt)

def peek_min(a, end=None, lt=None):
    "Return min element."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y
    assert end > 0
    return a[0]

def peek_max(a, end=None, lt=None):
    "Return max element."
    if end == None:
        end = len(a)
    if lt == None:
        lt = lambda x, y: x < y
    assert end > 0
    if end == 1:
        return a[0]
    imax = 1
    if end > 2 and lt(a[1], a[2]):
        imax = 2
    return a[imax]

if __name__ == "__main__":

    a = [chr(ord('a') + i) for i in range(15)]
    random.shuffle(a)
    print(''.join(a))
    heapify(a)
    print(''.join(a))
    check_heap(a)
    n = len(a)
    small_half =  n // 2
    for end in reversed(range(small_half+1, n+1)):
        store_max(a, end=end)
    for end in reversed(range(1, small_half+1)):
        store_min(a, end=end)
    print(''.join(a))
