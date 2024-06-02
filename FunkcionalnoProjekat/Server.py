import tkinter as tk
from tkinter import *
import socket
import time
from threading import Thread
import json
import User
import  Connections
import sqlite3
import functools

dictionary = {}
lisrFilter = []
listReduce = []
def ReduceF(a, b):
    return a.lower() + " " + b.upper()
def FilterF(x):
    if len(x)<2:
        return False

    if x[0].isupper():
        return True
    else:
        return False
def init_file():
    fileName = Connections.connection[0]
    try:
        with open(fileName, 'r') as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(fileName, 'w') as file:
            json.dump([], file)

def LoadFromFile():
    fileName = Connections.connection[0]
    with open(fileName, 'r') as fp:
        return json.load(fp)

def WriteInFile(user):
    fileName = "file.txt"
    data = LoadFromFile()
    data.append(json.loads(user.to_json()))
    with open(fileName, 'w') as fd:
        json.dump(data, fd)
def InsertIntoSql(val1, val2):
    with sqlite3.connect(Connections.connection[1]) as conn:
        # Bezbedniji način za unos podataka u bazu
        conn.execute("INSERT INTO THINGS (One, Two) VALUES (?, ?)", (val1, val2))
        conn.commit()

def ReadFromSql():
    with sqlite3.connect(Connections.connection[1]) as conn:
        cursor = conn.execute("SELECT ID, One, Two FROM THINGS")
        response = ""
        for row in cursor:
            response += "ID = " + str(row[0])
            response += "One = " + str(row[1])
            response += "Two = " + str(row[2])
    print(response)
    return response


def ServerRequest():
    print("Server started")
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.bind((host, port))
    s.listen(5)
    while True:
        listBox.insert(END, "Server  --- waiting")
        conn, addr = s.accept()
        message = conn.recv(1024).decode()
        array = message.split(':')
        response = ""
        if array[0] == 'JSON':
            user = User.User(array[1])
            WriteInFile(user)
            response = json.dumps(LoadFromFile())
        elif array[0] == 'DICTIONARY':
            global  dictionary
            dictionary[array[1]] = array[2]
            response = str(dictionary)
        elif array[0] == "SQL":
            InsertIntoSql(array[1],array[2])
            response += ReadFromSql()
        elif array[0] == "LISTFILTER":
            lisrFilter.append(array[1])
            lisrFilter.append(array[2])
            filteredTemp = filter(FilterF, lisrFilter)
            filtered_list = list(filteredTemp)
            response = str(filtered_list)
        elif array[0] == "LISTREDUCE":
            listReduce.append(array[1])
            listReduce.append(array[2])
            response = functools.reduce(ReduceF, listReduce, "")

        print(message)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        listBox.insert(END, f"{current_time} received message: {message}")
        conn.send(response.encode())
        conn.close()

root = tk.Tk()
root.title("Server")
listBox = Listbox(root, width=100, height=20)
listBox.pack()

init_file()

server_thread = Thread(target=ServerRequest)
server_thread.daemon = True
server_thread.start()

root.mainloop()
