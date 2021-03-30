from tkinter import *
import socket
from threading import Thread

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
BUFSIZ = 1024
client_socket = None

receive_thread = None

# Connect to Remote
def Connect():
    global client_socket
    global receive_thread
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (remote_ip.get(), int(remote_port.get()))
    print(ADDR)
    client_socket.connect(ADDR)
    receive_thread = Thread(target=RecvMessage)
    receive_thread.start()

# Receive Function
def RecvMessage():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break

# Send Function
def SendMessage():
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        socket.close()
    #     mainWindow.quit()

mainWindow = Tk()
mainWindow.title('Chat Application - Client')

configFrame = Frame(mainWindow)
# Set IP and Port
Label(configFrame, text='IP Address').grid(row=0)
Label(configFrame, text='Port').grid(row=1)
remote_ip = Entry(configFrame)
remote_ip.insert(END, '127.0.0.1')
remote_ip.grid(row=0, column=1)
remote_port = Entry(configFrame)
remote_port.insert(END, '8008')
remote_port.grid(row=1, column=1)

ConnectButton = Button(configFrame, text='Connect', width=25, command=Connect).grid(row=1,column=2)

# Show Current IP and Hostname
Label(configFrame, text="My IP: ").grid(row=2,column = 0)
Label(configFrame, text=ip).grid(row=2,column = 1)
Label(configFrame, text="My Hostname: ").grid(row=3,column = 0)
Label(configFrame, text=hostname).grid(row=3,column = 1)

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
sendButton = Button(SendFrame, text='Send Message', width=20, command=SendMessage).grid(row=6,column=1)
SendFrame.grid(row=5)

mainWindow.mainloop()