from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
BUFSIZ = 1024
server_socket = None
accept_thread = None
recv_thread_list = []
clientlist= []
ListenButton = None
sendButton = None

#AF stands for Address Family and PF stands for Protocol Family.
#INET stands for INTERNET
#AF_INET is for IPV4

#SOCK_STREAM means it's for streaming and it uses TCP

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
    try:
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
        # Change Button text and command to stop listening
        ListenButton.configure(text = "Stop Listening!", command=StopListen)
        # Enable Sending Messages
        sendButton.configure(state='normal')
    except OverflowError:
        print("Port number too large")
    except ValueError:
        print("Invalid Port number")

# Stop Server from listening
def StopListen():
    global server_socket
    global client_list
    server_socket.close()
    # Revert Button text and command to listen
    ListenButton.configure(text = "Listen", command=Listen)
    # Disable Sending Messages
    sendButton.configure(state='disabled')
    uname.configure(state="normal")
    for client in clientlist:
        client_socket, (ip, port) = client
        client_socket.close()
    if(accept_thread and accept_thread.is_alive()):
        accept_thread.join()
    for thread in recv_thread_list:
        thread.join()
 
    client_list = []

def AcceptConn():
    while True:
        try:
            if(server_socket):
                client = so, (ip, port) = server_socket.accept()
                print('Connected to ', ip, ':', str(port))
                clientlist.append(client)
                receive_thread = Thread(target=RecvMessage,args=(so,))
                recv_thread_list.append(receive_thread)
                receive_thread.start()
        except OSError:  # Client has left the chat.
            print("Accept Error")
            break

# Receive Function
def RecvMessage(client_socket):
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
            Broadcast(msg)
        except OSError:  # Client has left the chat.
            client_socket.close()
            # try:
            #     client_socket.close()
            # except OSError:
            #     print("Not a socket")
            # clientlist.remove(client_socket)
            print("Receive Error/Client Disconnected")
            break

# Send Function
def SendMessage():
    msg = uname.get() + ": " + message.get("1.0",END) # Retrives data from input field.
    message.delete("1.0",END)  # Clears input field.
    msg_list.insert(END, msg)
    Broadcast(msg)

# Broadcast to all clients
def Broadcast(msg):
    for client in clientlist:
            client_socket, (ip, port) = client
            try:
                client_socket.sendall(bytes(msg, "utf8"))
            except ConnectionResetError:
                clientlist.remove(client)




# Function called on exit to terminate running threads and close sockets
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if(server_socket):
            server_socket.close()
        if(accept_thread and accept_thread.is_alive()):
            accept_thread.join()
        for client in clientlist:
            client_socket, (ip, port) = client
            client_socket.close()
        for thread in recv_thread_list:
            thread.join()
        mainWindow.destroy()
# GUI
mainWindow = Tk()
mainWindow.title('Chat Application - Server')

configFrame = Frame(mainWindow)

# Show Hostname
Label(configFrame, text="My Hostname: ").grid(row=0,column = 0)
Label(configFrame, text=hostname).grid(row=0,column = 1)
# Set Username
Label(configFrame, text='Name').grid(row=0,column=2)
uname = Entry(configFrame,state="normal")
uname.grid(row=0,column=3)
uname.insert(END,"Host")
# Show IP
Label(configFrame, text="My IP: ").grid(row=1,column = 0)
Label(configFrame, text=ip).grid(row=1,column = 1)
# Set Port
Label(configFrame, text='Port').grid(row=2,column=0)
host_port = Entry(configFrame)
host_port.insert(END, '8008')
host_port.grid(row=2, column=1)

ListenButton = Button(configFrame, text='Listen', width=25, command=Listen)
ListenButton.grid(row=2,column=3)

configFrame.grid(row=0)

# Message Receive Box
messagesFrame = Frame(mainWindow)
scrollbar = Scrollbar(messagesFrame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messagesFrame, height=15, width=80, bg="silver",yscrollcommand=scrollbar.set)
msg_list.insert(0, "- - - - - - Beginning of Chat - - - - - - -")
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messagesFrame.grid(row=4)

SendFrame = Frame(mainWindow)
message = Text(SendFrame,height=4)
message.grid(row=6,column=0)
sendButton = Button(SendFrame, text='Send Message', width=12, command=SendMessage,state='disabled')
sendButton.grid(row=6,column=1)
SendFrame.grid(row=5)

mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
mainWindow.mainloop()
