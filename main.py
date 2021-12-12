needle = "456"
haystack = "1234567890"


class TenHash:
    def __init__(self, str=""):
        self.value = 0
        for c in str:
            self.add_right(c)

    def slide_right(self, new_char):
        self.add_right(new_char)
        self.drop_left()
        return self.value

    def slide_left(self, new_char):
        self.add_left(new_char)
        self.drop_right()
        return self.value

    def add_right(self, new_char):
        self.value = 10 * self.value + int(new_char)
        return self.value

    def add_left(self, new_char):
        number_of_chars = len(str(self.value))
        self.value = 10 ** number_of_chars * int(new_char) + self.value
        return self.value

    def drop_right(self):
        self.value = self.value // 10
        return self.value

    def drop_left(self):
        number_of_chars = len(str(self.value)) - 1
        self.value = self.value % (10 ** number_of_chars)
        return self.value
