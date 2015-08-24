"""
A Decent Number has the following properties:

3, 5, or both as its digits. No other digit is allowed.
Number of times 3 appears is divisible by 5.
Number of times 5 appears is divisible by 3.
"""
y=int(raw_input())
z=y while(z%3!=0): z-=5 if(z<0): print '-1' else:
    print z*'5'+(y-z)*'3'
