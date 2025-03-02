import Pyro4

@Pyro4.expose
class Polynomial:
    def add(self, pA, pB):
        return [a + b for a, b in zip(pA, pB)]

    def subtract(self, pA, pB):
        return [a - b for a, b in zip(pA, pB)]

    def multiply(self, pA, pB):
        result = [0] * (len(pA) + len(pB) - 1)
        for i in range(len(pA)):
            for j in range(len(pB)):
                result[i + j] += pA[i] * pB[j]
        return result
