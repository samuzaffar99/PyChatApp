from tkinter import *
import socket
from threading import Thread

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
BUFSIZ = 1024
client_socket = socket.socket()
server_socket = None
accept_thread = None
clientlist= []

# Connect to Remote
def Connect():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (ip, int(host_port.get()))
    print(ADDR)
    client_socket.connect(ADDR)

def Listen():
    global server_socket
    global accept_thread
    if(accept_thread and accept_thread.is_alive()):
        accept_thread.join()
    local_ip = '127.0.0.1'
    # Create Server Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow immediate restart of server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(type(host_port.get()))
    ADDR = (local_ip, int(host_port.get()))
    print(ADDR)
    # Bind Socket to address
    server_socket.bind(ADDR)
    # Listen for incoming upto n = 5 clients
    server_socket.listen(5)
    # Thread to handle Incoming Connections
    accept_thread = Thread(target=AcceptConn)
    accept_thread.start()

def AcceptConn():
    while True:
        try:
            if(server_socket):
                client = so, (ip, port) = server_socket.accept()
                print('Connected to ', ip, ':', str(port))
                clientlist.append(client)
        except OSError:  # Possibly client has left the chat.
            print("Accept Error")
            break

# Receive Function
def RecvMessage():
    """Handles receiving of messages."""
    while True:
        try:
            if(client_socket):
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                msg_list.insert(END, msg)
                Broadcast(msg)
        except OSError:  # Possibly client has left the chat.
            print("Receive Error")
            break

# Send Function
def SendMessage():
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        socket.close()
    #     mainWindow.quit()

def Broadcast(msg):
    for client in clientlist:
            client.connection.send(msg)
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
host_port.insert(END, '8008')
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

SendFrame = Frame(mainWindow)
message = Text(SendFrame,height=4).grid(row=6,column=0)
sendButton = Button(SendFrame, text='Send Message', width=20, command=SendMessage).grid(row=6,column=1)
SendFrame.grid(row=5)


receive_thread = Thread(target=RecvMessage)
receive_thread.start()
mainWindow.mainloop()