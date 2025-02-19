import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import mysql.connector

# Configuración del Cliente
SERVER_IP = "172.16.36.24"  # IP del servidor
PORT = 5000

conectado = False  # Estado inicial de la conexión
client = None  # Variable del socket

# Configuración de la base de datos del Cliente
DB_CONFIG_CLIENTE = {
    "host": "localhost",
    "user": "root",
    "password": "277353",
    "database": "chat_client"
}

try:
    conn_cliente = mysql.connector.connect(**DB_CONFIG_CLIENTE)
    cursor_cliente = conn_cliente.cursor()
    print("[BASE DE DATOS CLIENTE] Conectado")
except mysql.connector.Error as e:
    print(f"[ERROR] No se pudo conectar a la base de datos del cliente: {e}")

# Intentar conectar con el servidor
def conectar_servidor():
    """Intenta conectar al servidor y actualiza el estado."""
    global conectado, client

    if conectado:
        return  # Si ya está conectado, no hace nada

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_IP, PORT))
        conectado = True
        print("[INFO] Conectado al servidor correctamente.")

        if root.winfo_exists():
            messagebox.showinfo("Conexión Exitosa", "Conectado al servidor correctamente.")

        send_button.config(state=tk.NORMAL)  # Habilitar el botón de enviar
        connect_button.config(state=tk.DISABLED)  # Deshabilitar el botón de conexión

        # Iniciar hilo de recepción de mensajes
        thread = threading.Thread(target=receive_messages, daemon=True)
        thread.start()

    except Exception as e:
        conectado = False
        print(f"[ERROR] No se pudo conectar al servidor: {e}")

        if root.winfo_exists():
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que esté en línea.")

        connect_button.config(state=tk.NORMAL)  # Habilitar el botón de conexión manual

# Recibir mensajes del servidor
def receive_messages():
    """Escucha los mensajes entrantes del servidor."""
    global conectado
    while conectado:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                update_chat(message)
                
                # Si el mensaje viene del servidor con un nombre encontrado, insertarlo en msg_entry
                if message.startswith("[SERVIDOR] Encontrado:"):
                    nombre_encontrado = message.replace("[SERVIDOR] Encontrado:", "").strip()
                    msg_entry.delete(0, tk.END)
                    msg_entry.insert(0, nombre_encontrado)

        except:
            update_chat("[DESCONECTADO] Conexión perdida")
            conectado = False
            connect_button.config(state=tk.NORMAL)  # Habilitar botón de conexión
            break

def update_chat(message):
    """Actualiza el área de chat con un nuevo mensaje."""
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)

def send_message():
    """Envía un mensaje al servidor."""
    message = msg_entry.get()
    if message and conectado:
        try:
            client.send(message.encode('utf-8'))
            update_chat(f"Tú: {message}")
        except:
            update_chat("[ERROR] No se pudo enviar el mensaje")
    msg_entry.delete(0, tk.END)

def buscar_nombre():
    """Busca un usuario en la base de datos local y en el servidor."""
    nombre = simpledialog.askstring("Buscar Usuario", "Ingrese el nombre:")
    
    if nombre:
        # Buscar en la base de datos local
        cursor_cliente.execute("SELECT nombre, apellido FROM usuarios WHERE nombre = %s", (nombre,))
        resultado_local = cursor_cliente.fetchone()
        
        if resultado_local:
            encontrado_local = f"{resultado_local[0]} {resultado_local[1]}"
            update_chat(f"[CLIENTE] Encontrado en la BD Local: {encontrado_local}")
            msg_entry.delete(0, tk.END)  # Limpiar la caja de texto
            msg_entry.insert(0, encontrado_local)  # Insertar el nombre en el campo de entrada
        else:
            update_chat("[CLIENTE] No encontrado en la BD Local")

        # Enviar consulta al servidor
        if conectado:
            try:
                client.send(f"BUSCAR:{nombre}".encode('utf-8'))
            except:
                update_chat("[ERROR] No se pudo enviar la consulta al servidor.")

# Interfaz del Cliente
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("800x500")

# Área de chat
chat_area = scrolledtext.ScrolledText(root, height=15, width=80)
chat_area.pack()

# Entrada de mensaje
msg_entry = tk.Entry(root, width=50)
msg_entry.pack()

# Botón para enviar mensajes (deshabilitado hasta que se conecte)
send_button = tk.Button(root, text="Enviar", command=send_message, state=tk.DISABLED)
send_button.pack()

# Botón para buscar nombres en la base de datos local y en el servidor
search_button = tk.Button(root, text="Buscar Nombre", command=buscar_nombre)
search_button.pack()

# Botón para conectar manualmente al servidor
connect_button = tk.Button(root, text="Conectar al Servidor", command=conectar_servidor)
connect_button.pack()

# Intentar conectar automáticamente después de iniciar la interfaz
root.after(100, conectar_servidor)

root.mainloop()
