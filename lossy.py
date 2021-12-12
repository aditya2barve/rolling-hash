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

    @staticmethod
    def FromString(str):
        h = LossyTenHash()
        for c in str:
            h = h.add_right(c)
        return h

    def __init__(self):
        self.str = ""
        self.value = 0

    def slide_right(self, new_char):
        self.add_right(new_char)
        self.drop_left()
        return self

    def slide_left(self, new_char):
        self.add_left(new_char)
        self.drop_right()
        return self

    def add_right(self, new_char):
        self.value = 10 * self.value + int(new_char)
        self.value = self.value % self.PRIME
        self.str = self.str + new_char
        return self

    def add_left(self, new_char):
        self.value = 10 ** len(self.str) * int(new_char) + self.value
        self.value = self.value % self.PRIME
        self.str = new_char + self.str
        return self

    def drop_right(self):
        char_to_drop = self.str[-1]
        value_to_drop = int(char_to_drop)
        self.value = (self.value - value_to_drop) % self.PRIME
        # the following two lines fail because we don't have the 2340 anymore. we have 2340 % 251 = 81.
        # nine_tenths = 9 * self.value // 10
        # self.value = (self.value - nine_tenths) % self.PRIME
        # since we can't divide by 10, multiply by the multiplicative inverse of 10 in mod 251.
        self.value = (self.value * modInverse(10, self.PRIME)) % self.PRIME
        self.value = (self.value + self.PRIME) % self.PRIME
        self.str = self.str[:-1]
        return self

    def drop_left(self):
        char_to_drop = self.str[0]
        value_to_drop = int(char_to_drop) * (10 ** (len(self.str) - 1))
        self.value = (self.value - value_to_drop) % self.PRIME
        self.value = (self.value + self.PRIME) % self.PRIME
        self.str = self.str[1:]
        return self


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
