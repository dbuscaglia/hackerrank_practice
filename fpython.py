a = [1, 2 ,3 ,4, 6]

f = lambda x : x + 100

b = map(f, a)

c = filter(lambda x: x >100, b)
print c

d = reduce(lambda x, y: x + y, c)
print d
