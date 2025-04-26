import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

class PortScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Port Scanner")
        master.geometry("400x600")
        master.configure(bg="#2E2E2E")

        # Title Label
        self.title_label = tk.Label(master, text="Port Scanner", font=("Helvetica", 16), bg="#2E2E2E", fg="#FFFFFF")
        self.title_label.pack(pady=10)

        # Host Entry
        self.label = tk.Label(master, text="Enter Host:", bg="#2E2E2E", fg="#FFFFFF")
        self.label.pack(pady=5)

        self.host_entry = tk.Entry(master, width=30, font=("Helvetica", 12))
        self.host_entry.pack(pady=5)

        # Start Port Entry
        self.start_label = tk.Label(master, text="Start Port:", bg="#2E2E2E", fg="#FFFFFF")
        self.start_label.pack(pady=5)

        self.start_port_entry = tk.Entry(master, width=30, font=("Helvetica", 12))
        self.start_port_entry.pack(pady=5)

        # End Port Entry
        self.end_label = tk.Label(master, text="End Port:", bg="#2E2E2E", fg="#FFFFFF")
        self.end_label.pack(pady=5)

        self.end_port_entry = tk.Entry(master, width=30, font=("Helvetica", 12))
        self.end_port_entry.pack(pady=5)

        # Scan Button
        self.scan_button = tk.Button(master, text="Scan", command=self.start_scan, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12))
        self.scan_button.pack(pady=20)

        # Results Area
        self.results_area = scrolledtext.ScrolledText(master, width=45, height=10, font=("Helvetica", 12), bg="#FFFFFF", fg="#000000")
        self.results_area.pack(pady=10)

        # Open Ports Area
        self.open_ports_label = tk.Label(master, text="Open Ports Only:", bg="#2E2E2E", fg="#FFFFFF")
        self.open_ports_label.pack(pady=5)

        self.open_ports_area = scrolledtext.ScrolledText(master, width=45, height=5, font=("Helvetica", 12), bg="#FFFFFF", fg="#000000")
        self.open_ports_area.pack(pady=10)

        # Footer Label
        self.footer_label = tk.Label(master, text="© Devoloped by HexViper", bg="#2E2E2E", fg="#FFFFFF")
        self.footer_label.pack(pady=10)

    def scan_port(self, host, port):
        """Scan a single port on the host."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                self.results_area.insert(tk.END, f"Port {port} is open\n")
                self.open_ports_area.insert(tk.END, f"{port}\n")
            else:
                self.results_area.insert(tk.END, f"Port {port} is closed\n")

    def start_scan(self):
        """Start scanning ports in a separate thread."""
        host = self.host_entry.get()
        start_port = self.start_port_entry.get()
        end_port = self.end_port_entry.get()

        # Validate input
        if not host or not start_port.isdigit() or not end_port.isdigit():
            messagebox.showerror("Input Error", "Please enter valid host and port numbers.")
            return

        start_port = int(start_port)
        end_port = int(end_port)

        self.results_area.delete(1.0, tk.END)  # Clear previous results
        self.open_ports_area.delete(1.0, tk.END)  # Clear previous open ports

        threading.Thread(target=self.scan_ports, args=(host, start_port, end_port)).start()

    def scan_ports(self, host, start_port, end_port):
        """Scan a range of ports on the host."""
        for port in range(start_port, end_port + 1):
            self.scan_port(host, port)

if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()
