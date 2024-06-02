from tkinter import *
import socket

def SendMessage():
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.connect((host, port))
    message = chooseRB.get()+":"+ entryMessage.get()+":"+entryMessage2.get()
    s.send(message.encode())
    received = s.recv(1024).decode()
    listMessages.insert(END, received)
    s.close()

def on_buttonMain_click():
    SendMessage()

root = Tk()
root.title("Client")

chooseRB = StringVar()
rbJSON = Radiobutton(root,text="JSON",value="JSON",variable=chooseRB )
rbJSON.select()
rbJSON.pack()

rbSQL = Radiobutton(root,text="SQL",value="SQL",variable=chooseRB )
rbSQL.deselect()
rbSQL.pack()

rbDictionary = Radiobutton(root,text="DICTIONARY",value="DICTIONARY",variable=chooseRB )
rbDictionary.deselect()
rbDictionary.pack()

rbListFilter = Radiobutton(root,text="LIST FILTER  - TEXT",value="LISTFILTER",variable=chooseRB )
rbListFilter.deselect()
rbListFilter.pack()

rbListReduce = Radiobutton(root,text="LIST REDUCE",value="LISTREDUCE",variable=chooseRB )
rbListReduce.deselect()
rbListReduce.pack()


labelAction1 = Label(root, width=100, height=1, text="Message 1")
labelAction1.pack()

entryMessage = Entry(root, width=100)
entryMessage.pack()

labelAction2 = Label(root, width=100, height=1, text="Message 2")
labelAction2.pack()

entryMessage2 = Entry(root, width=100)
entryMessage2.pack()


buttonSend = Button(root, width=30, height=3, text="Send", command=lambda: on_buttonMain_click())
buttonSend.pack()

listMessages = Listbox(root, width=100, height=4)
listMessages.pack()

root.mainloop()
