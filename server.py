import Pyro4
from polynomial import Polynomial

def start_server():
    # 📌 Servidor funcionando **solo en local**
    host_ip = "127.0.0.1"  # Cambia esto cuando quieras usar en otra computadora
    daemon = Pyro4.Daemon(host=host_ip)  # Servidor Pyro4 en localhost
    ns = Pyro4.locateNS()  # Localizar el servidor de nombres de Pyro4

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
