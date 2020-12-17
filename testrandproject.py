import unittest
from randproject import RandomCracker
import random, time


class TestRandomCracker(unittest.TestCase):
    def setUp(self):
        self.randomCracker = RandomCracker()

    def testToBitarray(self):
        self.assertEqual(self.randomCracker.to_bitarray(15),
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1])

    def testFromBitarray(self):
        self.assertEqual(self.randomCracker.from_bitarray(
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]), 15)

    def testFirstHundred(self):
        random.seed(time.time())
        for i in range(624):
            self.randomCracker.submit(random.randint(0, 4294967294))
        self.assertTrue(sum([random.randint(0, 4294967294) == self.randomCracker.predict()
                                 for i in range(100)]) > 90)

    def test10000(self):
        random.seed(time.time() + 1)
        for i in range(624):
            self.randomCracker.submit(random.randint(0, 4294967294))
        self.assertTrue(sum([random.randint(0, 4294967294) == self.randomCracker.predict()
                                 for i in range(10000)]) / 100.0 >= 94)

    def test1000(self):
        random.seed(time.time() + 3)
        for i in range(624):
            self.randomCracker.submit(random.randint(0, 4294967294))
        self.assertTrue(sum([random.randint(0, 4294967294) == self.randomCracker.predict()
                                 for i in range(1000)]) / 10.0 >= 99)

    def test100000(self):
        random.seed(time.time() + 2)
        for i in range(624):
            self.randomCracker.submit(random.randint(0, 4294967294))
        self.assertTrue(sum([random.randint(0, 4294967294) == self.randomCracker.predict()
                                 for i in range(100000)]) / 1000.0 <= 50)

    def testXOR(self):
        self.assertEqual(self.randomCracker.xor_nums([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1], 
                                                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1]),
                                                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0])

    def testOR(self):
        self.assertEqual(self.randomCracker.or_nums([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
                                                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0]),
                                                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1])
        
    def testAND(self):
        self.assertEqual(self.randomCracker.and_nums([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
                                                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0]),
                                                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0])
        

if __name__ == '__main__':
    unittest.main()
