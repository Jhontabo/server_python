import tkinter as tk
from tkinter import messagebox
import Pyro4

class PolynomialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Polynomial Operations")
        self.root.geometry("400x350")
        
        # 📌 Cliente conectándose **solo en local**
        self.server_ip = "127.0.0.1"  # Cambia esto cuando quieras conectar a otro PC

        try:
            self.polynomial = Pyro4.Proxy(f"PYRONAME:polynomial.service@{self.server_ip}")
        except Pyro4.errors.CommunicationError:
            messagebox.showerror("Connection Error", "Cannot connect to the server. Make sure it is running and try again.")
            self.root.destroy()
            return
        
        # UI Elements
        self.label1 = tk.Label(root, text="Enter first polynomial (coefficients):")
        self.label1.pack()
        self.entry1 = tk.Entry(root, width=40)
        self.entry1.pack()
        
        self.label2 = tk.Label(root, text="Enter second polynomial (coefficients):")
        self.label2.pack()
        self.entry2 = tk.Entry(root, width=40)
        self.entry2.pack()
        
        self.operation_var = tk.StringVar()
        self.operation_var.set("add")
        
        self.operations_frame = tk.Frame(root)
        self.operations_frame.pack()
        
        tk.Radiobutton(self.operations_frame, text="Add", variable=self.operation_var, value="add").pack(side=tk.LEFT)
        tk.Radiobutton(self.operations_frame, text="Subtract", variable=self.operation_var, value="subtract").pack(side=tk.LEFT)
        tk.Radiobutton(self.operations_frame, text="Multiply", variable=self.operation_var, value="multiply").pack(side=tk.LEFT)
        tk.Radiobutton(self.operations_frame, text="Divide", variable=self.operation_var, value="divide").pack(side=tk.LEFT)
        
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="Result:", font=("Arial", 12, "bold"))
        self.result_label.pack()
        
        self.result_text = tk.Text(root, height=5, width=50)
        self.result_text.pack()
        
    def calculate(self):
        polyA = self.parse_input(self.entry1.get())
        polyB = self.parse_input(self.entry2.get())
        
        if polyA is None or polyB is None:
            messagebox.showerror("Input Error", "Invalid input. Please enter coefficients separated by spaces.")
            return
        
        operation = self.operation_var.get()
        
        try:
            if operation == "add":
                result = self.polynomial.add(polyA, polyB)
            elif operation == "subtract":
                result = self.polynomial.subtract(polyA, polyB)
            elif operation == "multiply":
                result = self.polynomial.multiply(polyA, polyB)
            elif operation == "divide":
                if len(polyB) == 0 or (len(polyB) == 1 and polyB[0] == 0):
                    messagebox.showerror("Math Error", "Cannot divide by zero.")
                    return
                quotient, remainder = self.polynomial.divide(polyA, polyB)
                result = f"Quotient: {quotient}\\nRemainder: {remainder}"
            else:
                result = "Unknown operation"
        except Pyro4.errors.CommunicationError:
            messagebox.showerror("Server Error", "Server connection lost. Please restart it and try again.")
            return
        
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, str(result))
        
    def parse_input(self, text):
        try:
            return [int(x) for x in text.split()]
        except ValueError:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = PolynomialGUI(root)
    root.mainloop()
