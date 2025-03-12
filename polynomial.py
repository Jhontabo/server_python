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

    def divide(self, dividend, divisor):
        if len(divisor) == 0 or (len(divisor) == 1 and divisor[0] == 0):
            raise ValueError("No se puede dividir por cero.")

        quotient = []
        remainder = dividend[:]
        
        while len(remainder) >= len(divisor):
            lead_coeff = remainder[0] / divisor[0]
            quotient.append(lead_coeff)
            
            # Generar el término multiplicado y restarlo del dividendo
            subtrahend = [lead_coeff * d for d in divisor] + [0] * (len(remainder) - len(divisor))
            remainder = [r - s for r, s in zip(remainder, subtrahend)]
            
            # Eliminar ceros iniciales
            while remainder and remainder[0] == 0:
                remainder.pop(0)

        return quotient, remainder
