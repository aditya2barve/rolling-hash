needle = "456"
haystack = "1234567890"

# 251 is largest prime < 256
# using mod 251 arithmetic, we can keep our hash values in 8 bits
class Lossy:
    @staticmethod
    def FromString(str):
        h = Lossy()
        for c in str:
            h = h.add_right(c)
        return h

    @staticmethod
    def FromValue(value):
        return Lossy(value)

    def __init__(self, value=0):
        self.value = value

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
        return self

    def add_left(self, new_char):
        number_of_chars = len(str(self.value))
        self.value = 10 ** number_of_chars * int(new_char) + self.value
        return self

    def drop_right(self):
        self.value = self.value // 10
        return self

    def drop_left(self):
        number_of_chars = len(str(self.value)) - 1
        self.value = self.value % (10 ** number_of_chars)
        return self


assert Lossy().value == 0
assert Lossy.FromString("345").value == 345
assert Lossy.FromValue(345).value == 345
assert Lossy.FromValue(345).slide_right("6").value == 456
assert Lossy.FromValue(345).slide_right("6").add_right("7").value == 4567
assert Lossy.FromValue(345).slide_left("2").value == 234
assert Lossy.FromValue(345).slide_left("2").add_left("1").value == 1234
