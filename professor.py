num = int(raw_input())

for i in xrange(num):
    total_students, required_students = raw_input().split(" ")
    input_string = raw_input()
    on_time_students = len(filter(lambda x: int(x) <= 0, input_string.split(' ')))
    if int(required_students) <= on_time_students:
        print "NO"  # DONT CANCEL CLASS
    else:
        print "YES"  # CANCEL CLASS
