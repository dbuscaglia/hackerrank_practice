import string


class Alphabet(object):

    def __init__(self):
        self._char_value_map = {string.ascii_lowercase[i]: i+1 for i in xrange(26)}
        self._char_set = set([c for c in string.ascii_lowercase])

    def char_value(self, c):
        return self._char_value_map[c]

    def is_funny(self, str_input):
        str_length = len(str_input)
        for i, c in enumerate(xrange(0, str_length / 2 + 1, 1)):
            leftabs = abs( self.char_value(str_input[i]) -
                self.char_value(str_input[i +1]))
            rightabs = abs(self.char_value(str_input[str_length - 1 - i]) -
                self.char_value(str_input[str_length - 2 - i]))
            if leftabs != rightabs:
                return "Not Funny"
        return "Funny"

    def is_panagram(self, str_input):
        letters = set([c.lower() for c in str_input if c != ' '])
        return "pangram" if self._char_set == letters else "not pangram"

    def required_delta_anagram(self, str_a, str_b):
        if len(str_a) % len(str_b) != 0 or len(str_a) == 0 or len(str_b) == 0:
            return "-1"
        required = 0
        left_counts = {string.ascii_lowercase[i]: 0 for i in xrange(26)}
        right_counts = {string.ascii_lowercase[i]: 0 for i in xrange(26)}
        unique_letters = set()
        for c in str_a:
            left_counts[c] = left_counts[c] + 1
        for c in str_b:
            unique_letters.add(c)
            right_counts[c] = right_counts[c] + 1

        for c in unique_letters:
            delta =  right_counts[c] - left_counts[c]
            if delta > 0:
                required += delta
        return str(required)

    def first_lexigraphicaly_larger_string(self, input_str):
        from itertools import permutations
        current_score = sum([self.char_value(c) for c in input_str])
        perms = permutations(input_str)
        contender = "no answer"
        m = 0
        for p in perms:
            pscore = sum([self.char_value(c) for c in p])
            print pscore
            if pscore > current_score and p != input_str:
                if pscore < m or m == 0:
                    contender = p
        return contender

    def can_grid_be_rearranged_in_lexigraphical_order(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        for i in xrange(rows):
            grid[i].sort()

        for row in xrange(rows):
            c = []
            for col in xrange(cols):
                c.append(grid[col][row])
            if not sorted(c) == c:
                return "NO"
        return "YES"

a = Alphabet()
output = []
grid = []
test_cases = int(raw_input())
for case in xrange(test_cases):
    grid = []
    rows = int(raw_input())
    for r in xrange(rows):
        grid.append(r)
        s = raw_input().strip()
        grid[r] = [c for c in s]  # Cols

    output.append(a.can_grid_be_rearranged_in_lexigraphical_order(grid))

print "\n".join(output)
