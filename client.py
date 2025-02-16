import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import mysql.connector

# Configuración del Cliente
SERVER_IP = "192.168.0.18"  # IP del servidor
PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# Configuración de la base de datos del Cliente
DB_CONFIG_CLIENTE = {
    "host": "localhost",
    "user": "root",
    "password": "@password27",
    "database": "chat_cliente"
}

try:
    conn_cliente = mysql.connector.connect(**DB_CONFIG_CLIENTE)
    cursor_cliente = conn_cliente.cursor()
    print("[BASE DE DATOS CLIENTE] Conectado")
except mysql.connector.Error as e:
    print(f"[ERROR] No se pudo conectar a la base de datos del cliente: {e}")

# Función para recibir mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                update_chat(message)

                # Si el mensaje es una respuesta de búsqueda, guardarlo en la BD
                if message.startswith("[SERVIDOR] Encontrado:"):
                    _, nombre, apellido = message.split(":")[1].strip().split()
                    cursor_cliente.execute("INSERT INTO usuarios (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
                    conn_cliente.commit()

        except:
            update_chat("[DESCONECTADO] Conexión perdida")
            break

# Función para actualizar la interfaz con mensajes
def update_chat(message):
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)

# Función para enviar mensajes
def send_message():
    message = msg_entry.get()
    if message:
        client.send(message.encode('utf-8'))
        update_chat(f"Tú: {message}")
    msg_entry.delete(0, tk.END)

# Función para buscar nombres y enviarlos al servidor
def buscar_nombre():
    nombre = simpledialog.askstring("Buscar Usuario", "Ingrese el nombre:")
    if nombre:
        client.send(f"BUSCAR:{nombre}".encode('utf-8'))

# Interfaz gráfica del Cliente
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("800x500")

chat_area = scrolledtext.ScrolledText(root, height=15, width=80)
chat_area.pack()

msg_entry = tk.Entry(root, width=50)
msg_entry.pack()

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack()

search_button = tk.Button(root, text="Buscar Nombre", command=buscar_nombre)
search_button.pack()

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

root.mainloop()
