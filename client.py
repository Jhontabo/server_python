import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import mysql.connector

# Configuración del Cliente
SERVER_IP = "192.168.0.18"  # IP del servidor (ajusta según tu red)
PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# Configuración de la base de datos del Cliente
DB_CONFIG_CLIENTE = {
    "host": "localhost",
    "user": "root",
    "password": "277353",
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

# Función para buscar un nombre en la base de datos del Cliente
def buscar_nombre():
    nombre = simpledialog.askstring("Buscar Usuario", "Ingrese el nombre:")
    if nombre:
        cursor_cliente.execute("SELECT nombre, apellido FROM usuarios WHERE nombre = %s", (nombre,))
        resultado = cursor_cliente.fetchone()
        if resultado:
            respuesta = f"[CLIENTE] Encontrado en la BD Local: {resultado[0]} {resultado[1]}"
            update_chat(respuesta)

            # Preguntar si se desea enviar al Servidor
            enviar_al_servidor = tk.messagebox.askyesno("Enviar al Servidor", "¿Deseas enviar este resultado al servidor?")
            if enviar_al_servidor:
                client.send(f"BUSCAR:{nombre}".encode('utf-8'))  # Envía la consulta al servidor
        else:
            update_chat("[CLIENTE] No encontrado en la BD Local")

# Interfaz del Cliente
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
