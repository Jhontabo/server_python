import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import mysql.connector

# Configuración del servidor
HOST = "0.0.0.0"  
PORT = 5000
clients = []

# Configuración de la base de datos del Servidor
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "277353",
    "database": "chat_servidor"
}

# Conectar con MySQL
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("[BASE DE DATOS] Conectado al Servidor")
except mysql.connector.Error as e:
    print(f"[ERROR] No se pudo conectar a la base de datos: {e}")

# Manejo de clientes
def handle_client(client_socket, address):
    print(f"[NUEVA CONEXIÓN] Cliente conectado desde {address}")
    update_chat(f"Cliente conectado: {address}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"[MENSAJE RECIBIDO] {address}: {message}")
            update_chat(f"{address}: {message}")

            # Si el cliente busca un nombre en la BD del servidor
            if message.startswith("BUSCAR:"):
                nombre_buscado = message.replace("BUSCAR:", "").strip()
                cursor.execute("SELECT nombre, apellido FROM usuarios WHERE nombre = %s", (nombre_buscado,))
                resultado = cursor.fetchone()
                if resultado:
                    respuesta = f"[SERVIDOR] Encontrado: {resultado[0]} {resultado[1]}"
                else:
                    respuesta = f"[SERVIDOR] No encontrado"

                client_socket.send(respuesta.encode('utf-8'))

            # Reenviar mensaje a todos los clientes
            for client in clients:
                if client != client_socket:
                    client.send(f"{address}: {message}".encode('utf-8'))

        except:
            print(f"[DESCONECTADO] Cliente {address} desconectado")
            break

    clients.remove(client_socket)
    client_socket.close()

# Función para iniciar el servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    update_chat(f"Servidor iniciado en {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        update_chat(f"Cliente {client_address} conectado")

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# Interfaz gráfica
def update_chat(message):
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)

def send_message():
    message = msg_entry.get()
    if message:
        update_chat(f"Servidor: {message}")
        for client in clients:
            try:
                client.send(f"Servidor: {message}".encode('utf-8'))
            except:
                print("[ERROR] No se pudo enviar el mensaje")
    msg_entry.delete(0, tk.END)

def buscar_nombre():
    nombre = simpledialog.askstring("Buscar Usuario", "Ingrese el nombre:")
    if nombre:
        cursor.execute("SELECT nombre, apellido FROM usuarios WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        if resultado:
            encontrado = f"{resultado[0]} {resultado[1]}"
            update_chat(f"[SERVIDOR] Encontrado: {encontrado}")
            msg_entry.delete(0, tk.END)  # Rellena el campo de texto con el nombre encontrado
            msg_entry.insert(0, encontrado)
        else:
            update_chat("[SERVIDOR] No encontrado")

# Interfaz del Servidor
root = tk.Tk()
root.title("Servidor de Chat")
root.geometry("800x500")

start_button = tk.Button(root, text="Iniciar Servidor", command=lambda: threading.Thread(target=start_server, daemon=True).start())
start_button.pack()

chat_area = scrolledtext.ScrolledText(root, height=15, width=80)
chat_area.pack()

msg_entry = tk.Entry(root, width=50)
msg_entry.pack()

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack()

search_button = tk.Button(root, text="Buscar Nombre", command=buscar_nombre)
search_button.pack()

root.mainloop()
