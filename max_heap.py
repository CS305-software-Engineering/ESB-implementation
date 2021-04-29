# this is an implementation of maxheap which will be imported in priority_queue.py

from heapq_max import heappush_max, heappop_max, heapify_max


class SizeError(Exception):  # custsom exception for popping empty queue
    pass


class max_heap:
    def __init__(self):
        self._heap = []

    def push(self, x):
        heappush_max(self._heap, x)

    def pop(self):
        if (self.size() == 0):
            raise SizeError
        return heappop_max(self._heap)

    def top(self):
        return self._heap[0]

    def empty(self):
        return (len(self._heap) == 0)

    def size(self):
        return len(self._heap)