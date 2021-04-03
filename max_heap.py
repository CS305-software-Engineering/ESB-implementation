# this is an implementation of maxheap which will be imported in priority_queue.py

# from heapq import heappush, heappop, heapify
import heapq


class max_heap:
    def __init__(self):
        self._heap = []
        pass

    def push(self, x):

        pass

    def pop(self):

        pass

    def top(self):
        return self._heap[0]

    def empty(self):
        return (len(self._heap) == 0)

    def size(self):
        return len(self._heap)


ls = [1, 2, 3]
print(len(ls))