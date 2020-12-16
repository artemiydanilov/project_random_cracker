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
    
    def _decode_harden_midop(self, enc, and_arr, shift):
        
        NEW = 0
        XOR = 1
        OK =  2
        work = []
        for i in range(32):
            work.append((NEW,enc[i]))
        changed = True
        while changed:
            changed = False
            for i in range(32):
                status = work[i][0]
                data = work[i][1]
                if i >= 32-shift and status == NEW:
                    work[i] = (OK,data)
                    changed = True
                elif i < 32-shift and status == NEW:
                    if and_arr[i] == 0:
                        work[i] = (OK, data)
                        changed = True
                    else:
                        work[i] = (XOR, data)
                        changed = True
                elif status == XOR:
                    i_other = i+shift
                    if work[i_other][0] == OK:
                        work[i] = (OK, data ^ work[i_other][1])
                        changed = True

        return [x[1] for x in work]
    
    def _harden_inverse(self, bits):
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, bits[:-18])
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[15:] + [0] * 15 , _to_bitarray(0xefc60000)))
        bits = self._decode_harden_midop(bits, self._to_bitarray(0xefc60000), 15)
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[7:] + [0] * 7 , _to_bitarray(0x9d2c5680)))
        bits = self._decode_harden_midop(bits, self._to_bitarray(0x9d2c5680), 7)
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, [0] * 11 + bits[:11]+[0] * 10)
        bits = self._xor_nums(bits, bits[11:21])

        return bits
    
