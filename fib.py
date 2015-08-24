class fib(object):

    previous_results = {
        1: 0,
        2: 1,
    }

    @classmethod
    def set_initials(cls, first, second):
        cls.previous_results[1] = first
        cls.previous_results[2] = second

    @classmethod
    def modified(cls, number):
        if number == 1:
            return cls.previous_results[1]
        if number == 2:
            return cls.previous_results[2]
        r = cls.modified(number - 1)*cls.modified(number - 1) + cls.modified(number-2)
        cls.previous_results[number] = r
        return r

first, second, goal = (int(i) for i in raw_input().strip().split())
fib.set_initials(first, second)
print fib.modified(goal)
