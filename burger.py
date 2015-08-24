test_cases = int(raw_input())
orders = []
for case in xrange(test_cases):
     order_start, order_finish =  (int( i ) for i in raw_input().strip().split())
     orders.append((order_start + order_finish, case + 1))

sorted_orders = sorted(orders, key=lambda x: x[0])
print " ".join([str(x[1]) for x in sorted_orders])
