from tkinter import *
import socket
from threading import Thread

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
BUFSIZ = 1024
client_socket = socket.socket()


# Connect to Remote
def Connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (ip, int(host_port.get()))
    client_socket.connect(ADDR)
    print(ADDR)

def Listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(type(host_port.get()))
    ADDR = (ip, int(host_port.get()))
    server_socket.bind(ADDR)
    print(ADDR)

# Receive Function
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break

# Send Function
def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        socket.close()
    #     mainWindow.quit()


# GUI
mainWindow = Tk()
mainWindow.title('Chat Application - Server')

configFrame = Frame(mainWindow)

# Show Hostname
Label(configFrame, text="My Hostname: ").grid(row=0,column = 0)
Label(configFrame, text=hostname).grid(row=0,column = 1)
# Show IP
Label(configFrame, text="My IP: ").grid(row=1,column = 0)
Label(configFrame, text=ip).grid(row=1,column = 1)
# Set Port
Label(configFrame, text='Port').grid(row=2,column=0)
host_port = Entry(configFrame)
host_port.grid(row=2, column=1)

ListenButton = Button(configFrame, text='Listen', width=25, command=Listen).grid(row=2,column=3)

configFrame.grid(row=0)





# Message Receive Box
messagesFrame = Frame(mainWindow)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messagesFrame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messagesFrame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messagesFrame.grid(row=4)

# Label(mainWindow, text="Your Message: ").grid(row=3,column=0)
SendFrame = Frame(mainWindow)
message = Text(SendFrame,height=4).grid(row=6,column=0)
sendButton = Button(SendFrame, text='Send Message', width=20, command=mainWindow.destroy).grid(row=6,column=1)
SendFrame.grid(row=5)



receive_thread = Thread(target=receive)
receive_thread.start()

mainWindow.mainloop()