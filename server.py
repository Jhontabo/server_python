import Pyro4
from polynomial import Polynomial

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Polynomial)
    ns.register("polynomial.service", uri)
    print("Server is running and waiting for connections...")
    daemon.requestLoop()

if __name__ == "__main__":
    start_server()
