# import random

# random_items = [random.randint(-50, 100) for c in range(32)]

# print 'Before: ', random_items
# insertion_sort(random_items)
# print 'After: ', random_items

"""Insertion Sort.

Insertion sort is a simple sorting algorithm that builds the final sorted array (or list) one item at a time.
It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.
Howerver, insertion sort provides several advantages.
"""

# ```python
def insertion_sort(a):
    if not a:
        return []
    for i in range(1, len(a)):
        cur = a[i]
        for j in range(i - 1, -1, -1):
            if a[j] <= cur:
                continue
            a[j + 1] = a[j]
            if j == 0:
                a[j] = cur
            if a[j - 1] <= cur:
                a[j] = cur
        print i, a

# insertion_sort([6, 5, 3, 1, 8, 7, 2, 4])

## output
# 1 [5, 6, 3, 1, 8, 7, 2, 4]
# 2 [3, 5, 6, 1, 8, 7, 2, 4]
# 3 [1, 3, 5, 6, 8, 7, 2, 4]
# 4 [1, 3, 5, 6, 8, 7, 2, 4]
# 5 [1, 3, 5, 6, 7, 8, 2, 4]
# 6 [1, 2, 3, 5, 6, 7, 8, 4]
# 7 [1, 2, 3, 4, 5, 6, 7, 8]


def bubble_sort(a):
    if not a:
        return []
    for i in range(len(a) - 1, -1, -1):
        for j in range(i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
        print i, a

# bubble_sort([6, 5, 3, 1, 8, 7, 2, 4])

# output
# 7 [5, 3, 1, 6, 7, 2, 4, 8]
# 6 [3, 1, 5, 6, 2, 4, 7, 8]
# 5 [1, 3, 5, 2, 4, 6, 7, 8]
# 4 [1, 3, 2, 4, 5, 6, 7, 8]
# 3 [1, 2, 3, 4, 5, 6, 7, 8]
# 2 [1, 2, 3, 4, 5, 6, 7, 8]
# 1 [1, 2, 3, 4, 5, 6, 7, 8]
# 0 [1, 2, 3, 4, 5, 6, 7, 8]


def merge_sort(items):
    # print len(items), items
    if len(items) <= 1:
        return
    mid = len(items) / 2
    left = items[0:mid]
    right = items[mid:]

    merge_sort(left)
    merge_sort(right)

    # print len(items), 'sort'

    l, r = 0, 0
    for i in range(len(items)):
        lval = left[l] if l < len(left) else None
        rval = right[r] if r < len(right) else None
        if (lval and rval and lval < rval) or rval is None:
            items[i] = lval
            l += 1
        elif(lval and rval and lval > rval) or lval is None:
            items[i] = rval
            r += 1
        # else:
        #     raise Exception('Could not merge')
    print len(items), items

# merge_sort([6, 5, 3, 1, 8, 7, 2, 4, 4])
# output
# 2 [5, 6]
# 2 [1, 3]
# 4 [1, 3, 5, 6]
# 2 [7, 8]
# 2 [2, 4]
# 4 [2, 4, 7, 8]
# 8 [1, 2, 3, 4, 5, 6, 7, 8]

def merge_sort_own(items):
    """write by myself."""
    


def quick_sort(items):
    if len(items) <= 1:
        return
    pivot_index = len(items) / 2
    smaller_items = []
    larger_items = []

    for i, val in enumerate(items):
        if i == pivot_index:
            continue
        if val < items[pivot_index]:
            smaller_items.append(val)
        else:
            larger_items.append(val)
    quick_sort(smaller_items)
    quick_sort(larger_items)
    items[:] = smaller_items + [items[pivot_index]] + larger_items
    print len(items), pivot_index, items

# quick_sort([6, 5, 3, 1, 8, 7, 2, 4])

# output
# 3 1 [4, 5, 6]
# 5 2 [2, 3, 4, 5, 6]
# 6 3 [2, 3, 4, 5, 6, 7]
# 7 3 [1, 2, 3, 4, 5, 6, 7]
# 8 4 [1, 2, 3, 4, 5, 6, 7, 8]


import heapq

def heap_sort(items):
    heapq.heapify(items)
    items[:] = [heapq.heappop(items) for i in range(len(items))]
    print items

# heap_sort([6, 5, 3, 1, 8, 7, 2, 4])

# output
# [1, 2, 3, 4, 5, 6, 7, 8]


def selection_sort(items):
    for i in range(len(items)):
        minn = items[i]
        for j in range(i + 1, len(items)):
            if minn > items[j]:
                minn, items[j] = items[j], minn
        items[i] = minn
    print items

# selection_sort([6, 5, 3, 1, 8, 7, 2, 4])

def shell_sort(items):
    length = len(items)
    height = 1
    while height < length:
        height = height * 3 + 1

    while height >= 1:
        for i in range(height, length):
            while i - height >= 0 and items[i] < items[i - height]:
                items[i], items[i - height] = items[i - height], items[i]
                i -= height
        height /= 3
        print height, items

## shell_sort([6, 5, 3, 1, 8, 7, 2, 4, 1, 2, 9, 10, 20, 21])
## output
# 13 [6, 5, 3, 1, 8, 7, 2, 4, 1, 2, 9, 10, 20, 21]
# 4 [6, 5, 3, 1, 8, 7, 2, 4, 1, 2, 9, 10, 20, 21]
# 1 [1, 2, 2, 1, 6, 5, 3, 4, 8, 7, 9, 10, 20, 21]
# 0 [1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21]

## functional

import random

names = ['Mary', 'Isla', 'Sam']
code_names = ['Mr. Pink', 'Mr. Orange', 'Mr. Black']

name = map(lambda x: random.choice(code_names), names)

# print name

name2 = map(hash, names)

print name2

