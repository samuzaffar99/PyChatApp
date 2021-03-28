from tkinter import *
import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
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

mainWindow.mainloop()