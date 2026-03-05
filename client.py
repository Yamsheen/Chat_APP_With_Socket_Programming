'''
This module defines the behaviour of a client in your Chat Application
'''
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util

FORMAT = "utf-8"
SIZE = 5000


'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''
c = True

class Client:
    '''
    This is the main Client Class. 
    '''

    def __init__(self, username, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(None)
        self.name = username
        self.sock.connect((self.server_addr, self.server_port))
        self.sock.sendall(f"join {self.name}".encode(FORMAT))

    def read_file(self,filename):
        print("file" ,filename)
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            file.close()
            return lines

        except FileNotFoundError:
            pass
        except IOError:
            pass


    def start(self):
        while c:
            user_input = input()

            if user_input == "list":
                try:
                    user_input += " " + self.name
                    try:
                        self.sock.sendall(user_input.encode("utf-8"))
                    except:
                        pass
                except BrokenPipeError:
                    print("Server disconnected. Quitting.")
                    break
            elif user_input == "quit":
                try:
                    user_input += " " + self.name
                    print("user",user_input)
                    try:
                        self.sock.sendall(user_input.encode("utf-8"))
                    except:
                        pass
                    print("quitting")
                    break
                except BrokenPipeError:
                    print("Server disconnected. Quitting.")
                    break
            elif user_input.startswith("msg"):
                try:
                    self.sock.sendall(user_input.encode("utf-8"))
                except BrokenPipeError:
                    
                    print("Server disconnected. Quitting.")
                    pass
                    break
                    

            elif user_input.startswith("file"):
                try:
                    user_input = user_input.split()
                    file_data = self.read_file(user_input[-1])
                    user_input = ' '.join(user_input)
                    file_data = ' '.join(file_data)
                    user_input += " " + file_data
                    try:
                        self.sock.sendall(user_input.encode("utf-8"))
                    except:
                        pass
                except BrokenPipeError:
                    print("Server disconnected. Quitting.")
                    break
            elif user_input == "help":
                print("List of commands:")
                # ... (existing code)
            elif user_input.lower() == "quit":
                self.quit()
            else:
                print("incorrect userinput format")


    

    def quit(self):
            try:
                disconnect_message = f"disconnect {self.name}"
                self.sock.sendall(disconnect_message.encode("utf-8"))
            except BrokenPipeError:
                
                pass
            
            sys.exit()

    
        

    def receive_handler(self):
        try:

            while True:
            
                
                    msg = self.sock.recv(SIZE).decode(FORMAT)
                    msg_list =  msg.split()

                    if not msg:
                        print(f"no msg")
                        break

                    elif len(msg_list) == 0:
                        print(f"empty list")
                        continue
                   
                    elif msg_list[0] == "list":
                            print(msg_list)
                            usernames = msg_list[1:]
                            usernames = ' '.join(usernames)
                            print("list:",usernames)
                    elif msg_list[0] == "msg":
                            sender_username = msg_list[1]
                            message = ' '.join(msg_list[2:])
                            print(f"msg: {sender_username} {message}")
                    elif msg_list[0] == "file":
                            print("from server",msg_list)
                            sender_username = msg_list[1].rstrip(':')
                            file_name = msg_list[2]
                            print(f"file: {sender_username}: {file_name}")
                            file_name = self.name + "_" + file_name
                            with open(file_name, 'w') as file:
                                file.writelines(msg_list[-1])
                    elif msg_list[0] == "err_server_full":
                        print("disconnected: server full")
                        self.sock.close()
                        break
                    elif msg_list[0] == "err_username_unavailable":
                        print("disconnected: username not available")
                        self.sock.close()
                        break
            
        
        except Exception as e:
            print(f"An error occurred: {e}")

        return

        
                        
       


# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a", ["user=", "port=", "address="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
