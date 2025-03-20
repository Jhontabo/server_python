import Pyro4

@Pyro4.expose  # Expone la clase para que Pyro4 pueda acceder a sus métodos
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

def start_server():
    # 📌 Servidor funcionando en una IP accesible para otras máquinas
    host_ip = "192.168.60.178"  # Cambia esto por la IP de la máquina donde ejecutas el servidor
    daemon = Pyro4.Daemon(host=host_ip)  # Servidor Pyro4 en la IP configurada
    ns = Pyro4.locateNS(host=host_ip)  # Localizar el servidor de nombres de Pyro4

    # Registrar la clase Polynomial
    uri = daemon.register(Polynomial)

    try:
        ns.register("polynomial.service", uri)
    except Pyro4.errors.NamingError:
        ns.remove("polynomial.service")
        ns.register("polynomial.service", uri)

    print(f"Server is running at {uri} and waiting for connections...")
    daemon.requestLoop()  # Mantener el servidor en espera de conexiones

if __name__ == "__main__":
    start_server()
