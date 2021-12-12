needle = "456"
haystack = "1234567890"


def modInverse(a, prime):
    a = a % prime
    for x in range(1, prime):
        if (a * x) % prime == 1:
            return x

    return None


# 251 is largest prime < 256
# using mod 251 arithmetic, we can keep our hash values in 8 bits
class LossyTenHash:
    PRIME = 251
    MULTIPLICATIVE_INVERSE_OF_10 = modInverse(10, PRIME)

    @staticmethod
    def FromString(str):
        h = LossyTenHash()
        for c in str:
            h = h.add_right(c)
        return h

    def __init__(self):
        self.str = ""
        self.value = 0

    def copy(self):
        h = LossyTenHash()
        h.str = self.str
        h.value = self.value
        return h

    def slide_right(self, new_char):
        return self.add_right(new_char).drop_left()

    def slide_left(self, new_char):
        return self.add_left(new_char).drop_right()

    def add_right(self, new_char):
        h = self.copy()
        h.value = 10 * h.value + int(new_char)
        h.value = h.value % h.PRIME
        h.str = h.str + new_char
        return h

    def add_left(self, new_char):
        h = self.copy()
        h.value = 10 ** len(h.str) * int(new_char) + h.value
        h.value = h.value % h.PRIME
        h.str = new_char + h.str
        return h

    def drop_right(self):
        h = self.copy()
        char_to_drop = h.str[-1]
        value_to_drop = int(char_to_drop)
        h.value = (h.value - value_to_drop) % h.PRIME
        # the following two lines fail because we don't have the 2340 anymore. we have 2340 % 251 = 81.
        # nine_tenths = 9 * h.value // 10
        # h.value = (h.value - nine_tenths) % h.PRIME
        # since we can't divide by 10, multiply by the multiplicative inverse of 10 in mod 251.
        h.value = (h.value * h.MULTIPLICATIVE_INVERSE_OF_10) % h.PRIME
        h.value = (h.value + h.PRIME) % h.PRIME
        h.str = h.str[:-1]
        return h

    def drop_left(self):
        h = self.copy()
        char_to_drop = h.str[0]
        value_to_drop = int(char_to_drop) * (10 ** (len(h.str) - 1))
        h.value = (h.value - value_to_drop) % h.PRIME
        h.value = (h.value + h.PRIME) % h.PRIME
        h.str = h.str[1:]
        return h


h345 = LossyTenHash.FromString("345")

test_cases = [
    (LossyTenHash(), 0),
    (h345, 345),
    (h345.slide_right("6"), 456),
    (h345.slide_right("6").add_right("7"), 4567),
    (h345.slide_left("2"), 234),
    (h345.slide_left("2").add_left("1"), 1234),
]

for t in test_cases:
    assert t[0].value == t[1] % LossyTenHash.PRIME
