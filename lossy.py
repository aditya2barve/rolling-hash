needle = "456"
haystack = "1234567890"


def modInverse(a, prime):
    a = a % prime
    for x in range(1, prime):
        if (a * x) % prime == 1:
            return x

    return -1


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

    @staticmethod
    def FromValue(value):
        return LossyTenHash(value)

    def __init__(self, value=0):
        self.value = value % self.PRIME
        self.number_of_chars = len(str(value))

    def slide_right(self, new_char, char_to_drop):
        self.add_right(new_char)
        self.drop_left(char_to_drop)
        return self

    def slide_left(self, new_char, char_to_drop):
        self.add_left(new_char)
        self.drop_right(char_to_drop)
        return self

    def add_right(self, new_char):
        self.value = 10 * self.value + int(new_char)
        self.value = self.value % self.PRIME
        self.number_of_chars += 1
        return self

    def add_left(self, new_char):
        self.value = 10 ** self.number_of_chars * int(new_char) + self.value
        self.value = self.value % self.PRIME
        self.number_of_chars += 1
        return self

    def drop_right(self, char_to_drop):
        value_to_drop = int(char_to_drop)
        self.value = (self.value - value_to_drop) % self.PRIME
        # the following two lines fail because we don't have the 2340 anymore. we have 2340 % 251 = 81.
        # nine_tenths = 9 * self.value // 10
        # self.value = (self.value - nine_tenths) % self.PRIME
        # since we can't divide by 10, multiply by the multiplicative inverse of 10 in mod 251.
        self.value = (self.value * modInverse(10, self.PRIME)) % self.PRIME
        self.value = (self.value + self.PRIME) % self.PRIME
        self.number_of_chars -= 1
        return self

    def drop_left(self, char_to_drop):
        value_to_drop = int(char_to_drop) * (10 ** (self.number_of_chars - 1))
        self.value = (self.value - value_to_drop) % self.PRIME
        self.value = (self.value + self.PRIME) % self.PRIME
        self.number_of_chars -= 1
        return self


test_cases = [
    (LossyTenHash(), 0),
    (LossyTenHash.FromString("345"), 345),
    (LossyTenHash.FromValue(345), 345),
    (LossyTenHash.FromValue(345).slide_right("6", "3"), 456),
    (LossyTenHash.FromValue(345).slide_right("6", "3").add_right("7"), 4567),
    (LossyTenHash.FromValue(345).slide_left("2", "5"), 234),
    (LossyTenHash.FromValue(345).slide_left("2", "5").add_left("1"), 1234),
]

for t in test_cases:
    assert t[0].value == t[1] % LossyTenHash.PRIME
