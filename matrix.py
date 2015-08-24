from collections import deque

numchars = int(raw_input())
message = raw_input()
offset = int(raw_input())


class Alphabet(object):

    alphabet = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','y', 'z' ])
    _map = {}

    def __init__(self, message):
        for i, a in enumerate(self.alphabet):
            self._map[a] = i

    def cipher(self, message, offset):
        for char in message:
            if char.isupper():
                yield self.letter_at_index(char.lower(), offset).upper()
            else:
                yield self.letter_at_index(char, offset)

    def letter_at_index(self, letter, offset):
        try:
            if offset > 26:
                offset = offset % 26
            letter_start = self._map[letter]
            if letter_start + offset > 25:
                cipher_start = 0 + ((letter_start + offset) - 26)
            else:
                cipher_start = letter_start + offset
            return self.alphabet[cipher_start]
        except (ValueError, IndexError, KeyError):
            return letter

al = Alphabet("test")

print "".join([c for c in al.cipher(message, offset)])
