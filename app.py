from flask import Flask
import math
import mmh3
from bitarray import bitarray


app = Flask(__name__)


@app.route('/')
def index():
    return "Hi!"


class BloomFilter(object):

    """
    Bloom filter class, murmur3 hash function based on geeksforgeeks tutorial
    """

    def __init__(self, items_count, fp_prob):

        """
        :param items_count: Number of items expected to be stored
        :param fp_prob: False positive probability
        """

        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item):
        """
        :param item: Item to add to the filter
        """
        digests = []
        for i in range(self.hash_count):
            digest = mm3.hash(item, i) % self.size
            digests.append(digest)
            self.bit_array[digest] = True

    def check(self, item):
        """
        :param item: Item to check existence of in the filter
        :return: True or False
        """
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        k = (m/n) * math.log(2)
        return int(k)
