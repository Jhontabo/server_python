import Pyro4
from polynomial import Polynomial

def start_server():
    daemon = Pyro4.Daemon()  # Servidor Pyro4
    ns = Pyro4.locateNS()  # Localizar el servidor de nombres
    uri = daemon.register(Polynomial)  # Registrar la clase

    try:
        ns.register("polynomial.service", uri)
    except Pyro4.errors.NamingError:
        ns.remove("polynomial.service")
        ns.register("polynomial.service", uri)

    print(f"Server is running at {uri} and waiting for connections...")
    daemon.requestLoop()  # Mantener el servidor en espera de conexiones

if __name__ == "__main__":
    start_server()
