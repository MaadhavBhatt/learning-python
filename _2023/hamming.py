import operator as op
from functools import reduce
from math import log2

import numpy as np


class HammingCodeBlock:
    """
    Class to represent a block of bits with Hamming code error correction.
    """

    def __init__(self, data) -> None:
        self.data = data
        self.bits = self._construct_bits_block()

        self.active_indices = [i for i, bit in enumerate(self.bits) if bit]

        self.set_parity_bits()

    def __str__(self) -> str:
        return str(self.bits)

    def _safe_log2(self, x: int):
        return log2(x) if x > 0 else 0

    def _no_prefix_bin(self, x: int):
        return bin(x).replace("0b", "")

    def _xor_active_indices(self) -> int:
        # TODO: Maybe use 0 as third argument
        return reduce(op.xor, self.active_indices)

    def _get_parity_indices(self) -> list:
        parity_indices = []

        for i in range(len(self.data)):
            if self._safe_log2(i) % 1 == 0:
                parity_indices.append(i)

        return parity_indices

    def _construct_bits_block(self):
        bits_block = []
        data_index = 0

        for i in range(16):
            if i in self._get_parity_indices():
                bits_block.append(0)
            else:
                bits_block.append(self.data[data_index])
                data_index += 1

        return bits_block

    def set_parity_bits(self) -> None:
        for i in self._no_prefix_bin(self._xor_active_indices())[::-1]:
            if i == 1:
                self.bits[2**i] = not self.bits[2**i]

    def detect_error_bit(self) -> int:
        return self._xor_active_indices()
