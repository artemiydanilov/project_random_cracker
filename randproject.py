class RandomCracker:

    def __init__(self):
        self.state = False
        self.mt = []
        self.counter = 0

    def submit(self, num):
        if self.state:
            print("Already got enough bits")
            return
        bits = self.to_bitarray(num)

        assert(all([x == 0 or x == 1 for x in bits]))

        self.counter +=1
        self.mt.append(self.harden_inverse(bits))
        if self.counter == 624:
            self.regen()
            self.state = True
            
    def to_bitarray(self, num):
        k = [int(x) for x in bin(num)[2:]]
        return [0] * (32-len(k)) + k

    def from_bitarray(self, bits):
        digit = 0
        for i in range(len(bits)):
            digit += int(bits[i]) * (2 ** (len(bits) - 1 - i))
        return digit
    
    def or_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b
        return [x[0] | x[1] for x in zip(a, b)]

    def xor_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b
        return [x[0] ^ x[1] for x in zip(a, b)]

    def and_nums(self, a, b):
        if len(a) < 32:
            a = [0]* (32-len(a))+a
        if len(b) < 32:
            b = [0]* (32-len(b))+b
        return [x[0] & x[1] for x in zip(a, b)]
    
    def harden(self, bits):
        bits = self.xor_nums(bits, bits[:-11])
        bits = self.xor_nums(bits, self.and_nums(bits[7:] + [0] * 7 , self.to_bitarray(0x9d2c5680)))
        bits = self.xor_nums(bits, self.and_nums(bits[15:] + [0] * 15 , self.to_bitarray(0xefc60000)))
        bits = self.xor_nums(bits, bits[:-18])
        return bits
    
    def decode_harden_midop(self, enc, and_arr, shift):
        
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
    
    def harden_inverse(self, bits):
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self.xor_nums(bits, bits[:-18])
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[15:] + [0] * 15 , _to_bitarray(0xefc60000)))
        bits = self.decode_harden_midop(bits, self.to_bitarray(0xefc60000), 15)
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[7:] + [0] * 7 , _to_bitarray(0x9d2c5680)))
        bits = self.decode_harden_midop(bits, self.to_bitarray(0x9d2c5680), 7)
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self.xor_nums(bits, [0] * 11 + bits[:11]+[0] * 10)
        bits = self.xor_nums(bits, bits[11:21])
        return bits

    def regen(self):
        N = 624
        M = 397
        MATRIX_A = 0x9908b0df
        LOWER_MASK = 0x7fffffff
        UPPER_MASK = 0x80000000
        mag01 = [self.to_bitarray(0), self.to_bitarray(MATRIX_A)]

        l_bits = self.to_bitarray(LOWER_MASK)
        u_bits = self.to_bitarray(UPPER_MASK)

        for i in range(0, N - M):
            y = self.or_nums(self.and_nums(self.mt[i], u_bits), self.and_nums(self.mt[i + 1], l_bits))
            self.mt[i] = self.xor_nums(self.xor_nums(self.mt[i + M], y[:-1]), mag01[y[-1] & 1])

        for i in range(N - M - 1, N - 1):
            y = self.or_nums(self.and_nums(self.mt[i], u_bits), self.and_nums(self.mt[i + 1], l_bits))
            self.mt[i] = self.xor_nums(self.xor_nums(self.mt[i + (M - N)], y[:-1]), mag01[y[-1] & 1])

        y = self.or_nums(self.and_nums(self.mt[N - 1], u_bits), self.and_nums(self.mt[0], l_bits))
        self.mt[N - 1] = self.xor_nums(self.xor_nums(self.mt[M - 1], y[:-1]), mag01[y[-1] & 1])

        self.counter = 0

    def predict(self):
        if not self.state:
            print("Didn't recieve enough bits to predict")
            return 0
        if self.counter >= 624:
            self.regen()
        self.counter += 1
        return self.from_bitarray(self.harden(self.mt[self.counter - 1]))


if __name__ == '__main__':

    import random, time
    rc = RandomCracker()
    random.seed(time.time())
    for i in range(624):
        rc.submit(random.randint(0, 4294967294))
    print(random.randint(0, 4294967294), rc.predict())
    print([(random.randint(0, 4294967294), rc.predict()) for i in range(5)])