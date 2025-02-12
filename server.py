import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 5000
clients = []

# Función para manejar clientes
def handle_client(client_socket, address):
    print(f"[NUEVA CONEXIÓN] Cliente conectado desde {address}")  # Mensaje en consola
    update_chat(f"Cliente conectado: {address}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[MENSAJE RECIBIDO] {address}: {message}")  # Mensaje en consola
            update_chat(f"{address}: {message}")

            # Enviar mensaje a todos los clientes menos al emisor
            for client in clients:
                if client != client_socket:
                    client.send(f"{address}: {message}".encode('utf-8'))
        except:
            print(f"[ERROR] Problema con {address}, desconectando...")  # Mensaje en consola
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"[DESCONECTADO] Cliente {address} se ha desconectado")  # Mensaje en consola
    update_chat(f"Cliente {address} se ha desconectado")

# Función para iniciar el servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[INICIADO] Servidor corriendo en {HOST}:{PORT}")  # Mensaje en consola
        update_chat(f"Servidor iniciado en {HOST}:{PORT}")
    except Exception as e:
        print(f"[ERROR] No se pudo iniciar el servidor: {e}")  # Mensaje en consola
        update_chat(f"Error al iniciar el servidor: {e}")
        return

    while True:
        try:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            print(f"[CONEXIÓN ACEPTADA] Cliente {client_address} conectado")  # Mensaje en consola
            update_chat(f"Cliente {client_address} conectado")

            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
        except Exception as e:
            print(f"[ERROR] No se pudo aceptar la conexión: {e}")  # Mensaje en consola
            update_chat(f"Error al aceptar conexión: {e}")

# Función para actualizar la interfaz con nuevos mensajes
def update_chat(message):
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)

# Función para enviar mensajes desde el servidor
def send_message():
    message = msg_entry.get()
    if message:
        print(f"[MENSAJE ENVIADO] Servidor: {message}")  # Mensaje en consola
        update_chat(f"Servidor: {message}")

        # Enviar a todos los clientes
        for client in clients:
            try:
                client.send(f"Servidor: {message}".encode('utf-8'))
            except:
                print(f"[ERROR] No se pudo enviar mensaje a un cliente.")  # Mensaje en consola
    msg_entry.delete(0, tk.END)



# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Chat")
root.geometry("800x500")  # Tamaño más amplio y moderno
root.configure(bg="#f5f5f5")  # Fondo claro y limpio

# ---- Estilos ----
BUTTON_COLOR = "#3498db"  # Azul moderno
BUTTON_TEXT_COLOR = "white"
TEXT_COLOR = "#2c3e50"  # Gris oscuro para texto
FONT = ("Arial", 14)

# ----- MARCO SUPERIOR -----
top_frame = tk.Frame(root, bg="#f5f5f5")
top_frame.pack(pady=20)

# Botón para iniciar el servidor
start_button = tk.Button(top_frame, text="Iniciar Servidor", font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
                         relief="flat", borderwidth=2, width=20,
                         command=lambda: threading.Thread(target=start_server, daemon=True).start())
start_button.pack()

# ----- MARCO DEL CHAT -----
chat_frame = tk.Frame(root, bg="#f5f5f5")
chat_frame.pack(padx=20, pady=10, expand=True, fill="both")

# Área de texto para mostrar mensajes
chat_area = scrolledtext.ScrolledText(chat_frame, height=15, width=80, bg="#ffffff", fg=TEXT_COLOR, font=FONT,
                                      relief="solid", borderwidth=1)
chat_area.pack(expand=True, fill="both", padx=10, pady=10)

# ----- MARCO INFERIOR -----
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(pady=10)

# Campo de entrada de mensajes
msg_entry = tk.Entry(bottom_frame, width=50, font=FONT, bg="#eeeeee", fg="black", relief="solid", borderwidth=1)
msg_entry.grid(row=0, column=0, padx=10)

# Botón para enviar mensajes
send_button = tk.Button(bottom_frame, text="Enviar", font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
                        relief="flat", borderwidth=2, width=12, command=send_message)
send_button.grid(row=0, column=1)

# Expansión automática al maximizar
root.pack_propagate(False)

# Iniciar la interfaz gráfica
root.mainloop()

