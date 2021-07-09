import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

#real scenario (server online): HOST = public IP address
HOST = '127.0.0.1'

PORT = 9090

class Client:
    #costruttore della classe client
    def __init__(self, host, port):
        #definisco il socket del client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #faccio connettere il socket alla tupla Host e port
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        #mi faccio dare il nickname dal client (user)
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        #GUI non ancora costruita
        self.gui_done = False
        #la connessione sta già eseguendo
        self.running = True

        #thread che crea la GUI e la mantiene
        gui_thread = threading.Thread(target=self.gui_loop)
        #thread che interafisce con la connessione al server del client
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

        #funzione che crea l'interfaccia grafica

    def gui_loop(self):

        #gui & background
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Python Chat Room", bg="lightgray")
        self.chat_label.config(font=("Arial Black", 12))
        self.chat_label.pack(padx=20, pady=5)

        #chat history box
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        #message label
        self.msg_label = tkinter.Label(self.win, text="Message Box", bg="lightgray")
        self.msg_label.config(font=("Hp simplified", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Hp simplified",12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        #alla chiusura forzata della finestra viene invocata la funzione stop
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        #prendo il messaggio nell'area di input NB: '1.0', 'end' -> indica l'intero messaggio.
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"

        self.sock.send(message.encode('utf-8'))

        #una volta inviato il messaggio ripulisco l'area di input
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)