"""
This script inputs numbers from standard input, one per line.
After each number, the mean, standard deviation, and median are
calculated and output to the screen.

The mean and standard deviation are calculated using
Welford's online algorithm described here:
https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

The median is calculated by creating a heap data structure. After adding
the new input value at each iteration, the median is calculated.

To run code
> python3 stream_stats.py < INPUTFILE

INPUTFILE has format of single number for each line.

"""

import sys      # used to read input from standard input
import heapq    # used in add_num function to create heaps


def add_num(num, max_heap, min_heap):
    """
    This function adds a number to the two heap data structures
    that track the sorted input data.
    Uses built in python library: heapq.
    :param num: input data
    :param max_heap: heap containing values above the halfway point
    :param min_heap: heap containing values below the halfway point
    """

    if not max_heap and not min_heap:  # if both heaps empty
        heapq.heappush(min_heap, num)
        return
    if not max_heap:  # if max heap empty
        if num > min_heap[0]:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
            heapq.heappush(min_heap, num)
        else:
            heapq.heappush(max_heap, -num)
        return
    # if heaps not empty, figure out where new number should go.
    if len(max_heap) == len(min_heap):
        if num < -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
    elif len(max_heap) > len(min_heap):
        if num < -max_heap[0]:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
    else:
        if num > min_heap[0]:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
            heapq.heappush(min_heap, num)
        else:
            heapq.heappush(max_heap, -num)
    return


def findmedian(max_heap, min_heap):
    """
    Using the input heaps, the median value is found at either of
    the ends of the data structures.
    """
    if len(max_heap) == len(min_heap):
        return (-max_heap[0] + min_heap[0])/2
    elif len(max_heap) > len(min_heap):
        return -max_heap[0]
    else:
        return min_heap[0]


def main():
    # set up variables
    mean = 0
    count = 0
    var = 0
    max_heap = []
    min_heap = []

    # loop through input strings, calculating mean, variance/stddev, median
    # output to screen
    for str_num in sys.stdin:
        num = (float(str_num))
        count += 1
        old_mean = mean
        mean = old_mean + (1 / count) * (num - old_mean)
        var = ((count - 1) * var + (num - old_mean) * (num - mean)) / count
        stddev = var**0.5
        add_num(num, max_heap, min_heap)
        median = findmedian(max_heap, min_heap)

        print(f'mean={mean:10.4}, stddev={stddev:10.4}, median={median:10.4}')


if __name__ == "__main__":
    main()
