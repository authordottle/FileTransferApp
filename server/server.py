#!/usr/bin/env python

import select, socket, sys
import threading
import os
import urllib.request
import time

user_name = []
socket_list = []
conn_list = []
user_connection = {}
file_list = ''
global files
files = []
path = ("./")
filesInServer =[]
TCP_PORT = 5001

## Build the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(("", TCP_PORT))
server.listen(5)
print("Server is binded.")

inputs = [server, sys.stdin]
newData = 0
conns = 0
localConn = 0
ips = {}

## Load local file path
def loadFilePath():
    global files
    files = []
    for file in os.listdir('.'):
        if not fnmatch.fnmatch(file, '*.py'):
            files.append(file)
    return files

## Main Function
while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is server:
            print("Here receives a connect request from a client. ****************")
            print
            conn, addr = s.accept()
            print("Connection is {}".format (conn))
            print("Address is {}".format (addr))
            conn.setblocking(0)
            inputs.append(conn)
            conn_list.append(conn)
            localConn = conn
        elif s is sys.stdin:
            command_string = input()
            print("Received:::: " + command_string)
        else:
            data = s.recv(1024).decode()
            if data:
                words = data.split()
                for i,word in enumerate(words):
                    
                    # Register users joining to share files for downloading
                    if word == "register":
                        userID = words[i+1]
                        if not userID in user_connection:
                            user_connection[userID] = s
                            ips[userID] = addr
                            print("New user %s is registered." % userID)
                            greetingMessage = "Ok. "+ userID +" is registered now."
                            localConn.send(greetingMessage.encode())
                        else:
                            errorMessage = "The userID already registered."
                            localConn.send(errorMessage.encode())
                
                    # Upload the file one by one passed by client side
                    elif word == "upload":
                        fname = words[i+1]
                        print('User: '+ addr[0] + ':' + str(addr[1]) + ' asked a upload request for: %s ****************' % fname)
                        # Send back the file name as ACK
                        localConn.sendall(words[i+1].encode())
                        filesInServer.append([userID, fname])
                        print("File %s is uploaded to server completely. ****************" % fname)
                            
                    elif word == "list_remote":
                        if filesInServer:
                            output = ''
                            for elt in filesInServer:
                                id = elt[0]
                                file = elt[1]
                                output = output + id + ' ' + file + ' \n'
                            localConn.send(output.encode())
                        else:
                            localConn.send("No files are shared on server.".encode())
                        
                    # Upload the file one by one passed by client side
                    elif word == "download":
                        fname = words[i+1]
                        id = words[i+2]
                        print('File %s belongs to %s.' % (fname, id))
                        print('IP is %s, %s.' %(ips[id][0], ips[id][1]))
                        if (user_connection[id]):
                            # Send back the ip which has this file
                            input = str(ips[id][0]) + ' ' + str(ips[id][1])
                            localConn.sendall(input.encode())
                        else:
                            localConn.sendall("This user is not registerd any more.".encode())


                    # Leave and no longer sharing files
                    elif word == "leave":
                        userID = words[i+1]
                        conn_list.remove(user_connection[userID])
                        del user_connection[userID]
                        temp = []
                        for elt in filesInServer:
                            if (elt[0] != userID):
                                temp.append(elt)
                                print("User %s is still registered. ****************" % elt[0])
                        filesInServer = temp
                        print("User %s left. ****************" % userID)

print("bye")

