import tkinter as tk
from tkinter import scrolledtext
import threading
import socket

# Configuración del Cliente
HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ---- Función para recibir mensajes ----
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                update_chat(message)
        except:
            break

# ---- Función para actualizar la interfaz con mensajes recibidos ----
def update_chat(message):
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)

# ---- Función para enviar mensajes ----
def send_message():
    message = msg_entry.get()
    if message:
        client.send(message.encode('utf-8'))
        update_chat(f"Tú: {message}")
    msg_entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("800x500")  # Tamaño amplio y ajustable
root.configure(bg="#f5f5f5")  # Fondo claro y moderno

# ---- Estilos ----
BUTTON_COLOR = "#3498db"  # Azul moderno
BUTTON_TEXT_COLOR = "white"
TEXT_COLOR = "#2c3e50"  # Gris oscuro para texto
FONT = ("Arial", 14)

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

# Hilo para recibir mensajes del servidor
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

# Iniciar la interfaz gráfica
root.mainloop()
