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
            
    def _to_bitarray(self, num):
        k = [int(x) for x in bin(num)[2:]]
        return [0] * (32-len(k)) + k

    def _predict(self):
        if not self.state:
            print("Didn't recieve enough bits to predict")
            return 0
        if self.counter >= 624:
            self._regen()
        self.counter += 1

        return self._harden(self.mt[self.counter-1])
    
    
     def _or_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b

        return [x[0] | x[1] for x in zip(a, b)]

    def _xor_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b

        return [x[0] ^ x[1] for x in zip(a, b)]

    def _and_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b

        return [x[0] & x[1] for x in zip(a, b)]
    
    
    #закалка
    def _harden(self, bits):
        bits = self._xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, self._and_nums(bits[7:] + [0] * 7 , self._to_bitarray(0x9d2c5680)))
        bits = self._xor_nums(bits, self._and_nums(bits[15:] + [0] * 15 , self._to_bitarray(0xefc60000)))
        bits = self._xor_nums(bits, bits[:-18])
        return bits
    
    
