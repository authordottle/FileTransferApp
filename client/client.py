#!/usr/bin/env python

import select, socket, sys
import socket
import time
from tkinter import *
import os
import fnmatch
from tkinter import filedialog
import random

## Get the Local IP through the google server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("8.8.8.8", 443))
machineIP = s.getsockname()[0]
print(machineIP)
s.close()

window = Tk()
window.title("FileTransferApp")
window.geometry('350x500')

f0 = Frame(window)
f1 = Frame(window)
f2 = Frame(window)
f3 = Frame(window)
f5 = Frame(window)

## Input command lines and received by server
userID = ''
path = ("./")
inputs = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TCP_PORT = 5001
TCP_PORT2 = random.randint(1000,4000)


## All Frame  Shared #####################################################################################################
## Change the frame
def raise_frame(frame):
    frame.tkraise()


## Frame #####################################################################################################
def redirectToRegisterPage():
    f0.grid_remove()
    f1.grid(row=0, column=0)
    raise_frame(f1)

## Build socket
def input():
    global TCP_IP
    TCP_IP = e.get()
    
    ## Server
    s.connect((TCP_IP, TCP_PORT))
    print("** Client is connected to server with {}." .format (s))
    
    ## Client socket
    s2.bind((machineIP, TCP_PORT2))
    s2.listen(5)
    print("** Client socket2 for receiving is built with {}.".format(s2))
    
    s3.connect((machineIP, TCP_PORT2))
    print("** Client socket3 for receiving is built with {}.".format(s3))
    
    global inputs
    inputs = [s2, sys.stdin]
    redirectToRegisterPage()


# Frame for input server ip
Label(f0, text="Please input the server ip: ").pack(side = TOP)
e = Entry(f0)
e.pack()
Button(f0, text='Submit', width=15, height=2, command=input).pack()

## Frame 1 #####################################################################################################
## Upload local files to server
## Load local file path
def loadFilePath():
    global files
    files = []
    for file in os.listdir('.'):
        if not fnmatch.fnmatch(file, '*.py') and not fnmatch.fnmatch(file, '.DS_Store'):
            files.append(file)
    return files

def uploadtoServer():
    files = loadFilePath()
    print("User has those files: ")
    print(files)
    if (files):
        for fname in files:
            print("File found, sending request to server... ****************")
            input = 'upload '+ fname
            s.sendall(input.encode())
            
            # Receive ACK from server to make sure server caught file
            ack = s.recv(1024).decode()
            print("ACK from server: " + str(ack))
            print("This files is uploaded to server. ****************")
        print("Uploading process completes. ****************")
    else:
        print("No files available in dir.")

## Register user
def register():
    global userID
    userID = e1.get()
    if (userID == ''):
        Label(f1, text="Please input valid value to register.").pack(side = BOTTOM)
    else:
        msgToSend = "register " + userID
        s.sendall(msgToSend.encode())

    ## Get the data from server
    data = s.recv(1024).decode()
    if (data == "The userID already registered."):
        Label(f1, text=data).pack(side = BOTTOM)
    else:
        f1.grid_remove()
        f2.grid(row=0, column=0)
        Label(f2, text=data).pack(side = BOTTOM)
        raise_frame(f2)
        uploadtoServer()

# Frame 1 for register
Label(f1, text="The server is connected.").pack(side = TOP)
Label(f1, text="Please register first:").pack(side = TOP)
e1 = Entry(f1)
e1.pack()
Button(f1, text='Register', width=15, height=2, command=register).pack()


## Frame 2 #####################################################################################################
## Display file path
def displayFilePaths(data):
    for elt in data:
        Label(f2, text=elt).pack(side = BOTTOM)

## List local files
def listLocalFiles():
    files = loadFilePath()
    if files:
        displayFilePaths(files)
    else:
        displayFilePaths("No file is shared now.")

## Leave the files sharing
def leave():
    msgToSend = 'leave ' + userID
    s.sendall(msgToSend.encode())
    f2.grid_remove()
    f3.grid(row=0, column=0)
    raise_frame(f3)
    s.close()
    s2.close()
    s3.close()

## Redirect to download page
def redirectToDownloadPage():
    f2.grid_remove()
    global f4
    f4 = Frame(window)
    f4.grid(row=0, column=0)
    raise_frame(f4)
    displayFileForDownload()

# Frame 2 for list / leave input
Label(f2, text="You are registered.").pack(side = TOP)
Button(f2, text='List local files', width=15, height=2, command=listLocalFiles).pack()
Button(f2, text='Download files', width=15, height=2, command=redirectToDownloadPage).pack()
Button(f2, text='Leave', width=15, height=2, command=leave).pack()

# Frame 3 for leave page
Label(f3, text="Sorry for missing you. Please close the window.").pack(side = TOP)

## Frame 4 #####################################################################################################
## Rename the filename if exist when downloading
def filename_fix_existing(filename):
    dirname = '.'
    name, ext = filename.rsplit('.', 1)
    names = [x for x in os.listdir(dirname) if x.startswith(name)]
    names = [x.rsplit('.', 1)[0] for x in names]
    suffixes = [x.replace(name, '') for x in names]
    # filter suffixes that match ' (x)' pattern
    suffixes = [x[2:-1] for x in suffixes if x.startswith(' (') and x.endswith(')')]
    indexes  = [int(x) for x in suffixes if set(x) <= set('0123456789')]
    idx = 1
    if indexes:
        idx += sorted(indexes)[-1]
    return '%s(%d).%s' % (name, idx, ext)

##
def displayFileForDownload():
    msgToSend = 'list_remote'
    print("Current server is {}".format(s))
    s.sendall(msgToSend.encode())
    data = s.recv(1024).decode()
    words = data.split()
    print("Here are the files showing in the window: ")
    print(words)
    
    if (data == "No files are shared on server."):
        Label(f4, text=data).pack(side = TOP)
    else:
        i = 0
        while i + 1 < len(words):
            id = words[i]
            fname = words[i + 1]
            sentence = id + ': ' + fname
            Label(f4, text=sentence).pack(side = TOP)
            Button(f4, text='Download', width=15, height=2, command=lambda i=i: downloadThisFile(id = words[i], fname = words[i + 1])).pack()
            i = i + 2
    print("Display Complete. *****")

def redirectToMainPage():
    f4.destroy()
    f2.grid(row=0, column=0)
    raise_frame(f2)

## Download this file
def downloadThisFile(id, fname):
    print("File found, sending request to server... ****************")
    input = 'download '+ fname + ' ' + id
    s.sendall(input.encode())
    
    # Receive the ip which has this file
    ack = s.recv(1024).decode()
    if (ack == "This user is not registerd any more."):
        print(ack)
    else:
        print("ACK1 from server: " + ack)
        words = ack.split()

    # Connect the client who has this file with filename
    s3.sendto(fname.encode(),(words[0], TCP_PORT2))
    clientSocketACK(words, fname, machineIP)
    ack2 = s3.recv(1024).decode()
    print("ACK2 from server: " + ack2)
    fileSize = ack2
    s3.sendto(str(fileSize).encode(),(words[0], TCP_PORT2))
    transferToClient(fname, fileSize)

def clientSocketACK(words, fname, machineIP):
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s11 in readable:
        # Client server
        if s11 is s2:
            global clientSocket
            clientSocket, infoIP = s2.accept()
            print("### A client Connection is {}".format (clientSocket))
            print("### Client Address is {}".format (infoIP))
            print("### Client is asking for %s" %fname)
            fileSize = os.path.getsize(fname)
            clientSocket.sendto(str(fileSize).encode(), (machineIP, TCP_PORT2))
        else:
            print("Received:::: ")

def transferToClient(fname, fileSize):
    print("!ClientSocket info: " + clientSocket.recv(1024).decode())

    # Start to send file
    f1 = open((path + fname), "rb")
    buffRead = 0
    bytesRemaining1 = int(fileSize)
    
    # Start to receive file
    if os.path.exists(fname):
        fname = filename_fix_existing(fname)
    f = open((path + fname), "wb")
    bytesRemaining = int(fileSize)

    while bytesRemaining != 0 and bytesRemaining1 != 0:

        if(bytesRemaining1 >= 1024):
            buffRead = f1.read(1024)
        else:
            buffRead = f1.read(bytesRemaining)
        sizeofSlabRead = len(buffRead)
        print("* File read: %d bytes" % sizeofSlabRead)
        clientSocket.sendto(buffRead,(machineIP, TCP_PORT2))

        if(bytesRemaining >= 1024):
            slab = s3.recv(1024)
        else:
            slab = s3.recv(bytesRemaining)
        f.write(slab)
        sizeofSlabReceived = len(slab)
        print("** File wrote %d bytes" % len(slab))

        bytesRemaining1 = bytesRemaining - int(sizeofSlabRead)
        bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
    print("File %s is transfered to client completely. ****************" %f)
    f1.flush()
    f1.close()
    f.flush()
    f.close()
    redirectToMainPage()

f0.grid(row=0, column=0)
raise_frame(f0)
window.mainloop()





