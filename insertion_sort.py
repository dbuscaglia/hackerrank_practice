
def sort_numbers(s):
    count = 0
    for i in range(1, len(s)):
        val = s[i]
        j = i - 1
        while (j >= 0) and (s[j] > val):
            count += 1
            s[j+1] = s[j]
            j = j - 1
        s[j+1] = val
    return count

n = input()
for iterate in range( n ):
    x = input()
    a = [ int( i ) for i in raw_input().strip().split() ]
    # Write code to compute answer using x, a and answer
    print sort_numbers(a)
