"""quick sort."""

# own thought


def quick_sort(source_list):
    """Quick Sorted."""
    if not source_list:
        return source_list
    length = len(source_list)
    a = source_list
    key = a[0]
    jack = length - 1
    for i in range(length):
        if a[i] > key:
            a[i], a[jack] = a[jack], a[i]
            jack -= 1
        else:
            continue
        for j in range(jack, -1, -1):
            if a[i] < key:
                a[i], a[j] = a[j], a[i]
                break


def heap_sort()
