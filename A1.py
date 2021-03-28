from tkinter import *
import socket


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
BUFSIZ = 1024
# ADDR = (e1, 33000)
# client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(socket.ADDR)

# Receive Function
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break


mainWindow = Tk()
mainWindow.title('Chat Application')
Label(mainWindow, text='IP Address').grid(row=0)
Label(mainWindow, text='Port').grid(row=1)
Label(mainWindow, text="IP: "+ip).grid(row=2,column = 0)
Label(mainWindow, text="Hostname: "+hostname).grid(row=2,column = 1)
e1 = Entry(mainWindow)
e2 = Entry(mainWindow)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
b1 = Button(mainWindow, text='Stop', width=25, command=mainWindow.destroy)
b1.grid(row=3)
# button.pack()


# Message Receive Box
messages_frame = Frame(mainWindow)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.grid(row=5)

mainWindow.mainloop()