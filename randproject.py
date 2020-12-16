class RandomCracker:

    def __init__(self):
        self.mt = []
        self.counter = 0

    def submit(self, num):
        bits = self._to_bitarray(num)
        self.counter += 1
        self.mt.append(self._harden_inverse(bits))
        if self.counter == 624:
            self._regen()

    def _predict(self):
        if self.counter >= 624:
            self._regen()
