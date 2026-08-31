from typing import List
import math

__all__ = ['ObjectiveFunction']

class ObjectiveFunction:
    @staticmethod
    def Entropy(freq: List[int]) -> float:
        sub, n = 0.0, 0
        for f in freq:
            sub += f * math.log2(f)
            n += f

        return (sum(freq) * math.log2(n) - sub) / n

    @staticmethod
    def Gini(freq: List[int]) -> float:
        n = sum(freq)
        return 1 - sum((f/n)**2 for f in freq)

    @staticmethod
    def ClassificationError(freq: List[int]) -> float:
        n, m = 0, -math.inf
        for f in freq:
            if f > m:
                m = f
            n += f
        return (n - m) / n
