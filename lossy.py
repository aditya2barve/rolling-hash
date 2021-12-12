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
        # this line fails. we don't have the "2340 anymore. we have 2340 % 251 = 81"
        # so we can't divide by 10. find out the multiplicative inverse of 10 in mod 251 space
        # and multiply by it
        # nine_tenths = 9 * self.value // 10
        # self.value = (self.value - nine_tenths) % self.PRIME
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


assert LossyTenHash().value == 0 % LossyTenHash.PRIME
assert LossyTenHash.FromString("345").value == 345 % LossyTenHash.PRIME
assert LossyTenHash.FromValue(345).value == 345 % LossyTenHash.PRIME
assert (
    LossyTenHash.FromValue(345).slide_right("6", "3").value == 456 % LossyTenHash.PRIME
)
assert (
    LossyTenHash.FromValue(345).slide_right("6", "3").add_right("7").value
    == 4567 % LossyTenHash.PRIME
)
assert (
    LossyTenHash.FromValue(345).slide_left("2", "5").value == 234 % LossyTenHash.PRIME
)
assert (
    LossyTenHash.FromValue(345).slide_left("2", "5").add_left("1").value
    == 1234 % LossyTenHash.PRIME
)
