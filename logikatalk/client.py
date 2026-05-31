from customtkinter import *
import socket
import threading
import os
#import login

#env = login.get_data()
class Window(CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry("500x500")
        self.title("LogikaTalk")

        self.name = os.environ.get("USERNAME", "User")# env.get("name")
        self.text = CTkTextbox(self, width=400, height=250, text_color="black", fg_color="white")
        self.text.configure(state="disabled")
        self.text.pack(pady=20)

        self.sent_text = CTkEntry(self, width=280, placeholder_text="Введіть повідомлення")
        self.sent_text.place(x=20, y=300)

        self.sent = CTkButton(self, text="Відправити", width=80,command=self.send_message)
        self.sent.place(x=310, y=300)

        self.img_btn = CTkButton(self, text="📷", width=40, fg_color="gray")
        self.img_btn.place(x=400, y=300)
        
        self.host = "localhost"
        self.port = 8080
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.sock.send(f"Text@{self.name}@підключився до чату \n".encode())
            threading.Thread(target=self.recv_msg, daemon=True).start()
        except:
            self.add_message("Помилка підключення до сервера")
        
    def recv_msg(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode(errors='ignore')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                print("server error")
                break
        self.sock.close()
    def handle_line(self, line):
        print(f"Received line: {line}")
        if not line:
            return
        parts = line.split('@', 3)
        print(parts)
        msg_type = parts[0]
        if msg_type == "Text":
            if len(parts) >= 3:
                author = parts[1]
                message = "@".join(parts[2:])  # Об'єднати елементи в рядок
                self.add_message(f"{author}: {message}")
        if msg_type == "Image":
            pass
    def add_message(self, text):
        self.text.configure(state="normal")
        self.text.insert("end", text + "\n")
        self.text.configure(state="disabled")

    def send_message(self):
        msg = self.sent_text.get()
        if msg:
            self.add_message(f"{self.name}: {msg}")
            data = f"Text@{self.name}@{msg}\n"
            try:
                self.sock.send(data.encode())
            except:
                print("Помилка відправки повідомлення")
            self.sent_text.delete(0, 'end')   


        
    
Window().mainloop()