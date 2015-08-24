"""
Pizza queue problem
"""
import heapq
class Heap(object):
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """

    def __init__(self):
        """ create a new min-heap. """
        self._heap = []

    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        assert priority >= 0
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap)  # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        """ Get all elements ordered by asc. priority. """
        return self

    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration


def get_next_valid_order(t, q):
    restoreitems = []
    pizza_cook_time, start_time = q.next()
    while start_time > t:
        restoreitems.append((pizza_cook_time, start_time))
        pizza_cook_time, start_time = q.next()
    if restoreitems:
        for item in restoreitems:
            q.push(item[0], item[1])
    return pizza_cook_time, start_time


pizzaqueue = Heap()

total_orders = int(raw_input())
start_times = []
for _ in xrange(total_orders):
    st, cooking_time = raw_input().split(" ")
    pizzaqueue.push(int(cooking_time), int(st))
    start_times.append(int(st))
"""
total_orders = 5
pizzaqueue.push(961148050, 385599125)
pizzaqueue.push(951133776, 376367013)
pizzaqueue.push(283280121, 782916802)
pizzaqueue.push(317664929, 898415172)
pizzaqueue.push(980913391, 847912645)
"""
start_times = sorted(start_times)
last_start = start_times[0]
total_time = 0
cooking_time = 0
waittimes = []
for t in start_times:
    pizza_cook_time, st = get_next_valid_order(last_start, pizzaqueue)
    last_start += pizza_cook_time
    waittimes.append(last_start - st)


print int(sum(waittimes) / total_orders)
#print sum(waittimes)


#print total_time, total_orders
#print int(waittimes / total_orders)
