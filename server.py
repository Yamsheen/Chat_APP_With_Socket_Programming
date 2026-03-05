'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util
import threading


FORMAT = "utf-8"
SIZE = 5000

class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''

    def __init__(self, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.connected_clients = []

    def start(self):
        self.sock.listen()
        while True:
            conn, add= self.sock.accept()
            threading.Thread(target = self.client_handler, args=(conn,)).start()


   



    def client_handler(self, conn):
        current_username = ""
        while True:
            try:
                msg=conn.recv(5000).decode("utf-8")
               
               

            

                msg_list = msg.split()
                if msg_list[0] == "join":
                    
                    if len(self.connected_clients) >= 10:
                        msg_to_send = "err_server_full".encode('utf-8')
                        conn.send(msg_to_send)
                        print("disconnected: server full")
                        conn.close()
                        break
                        

                    username = msg_list[1]
                    flag = False
                    for client in self.connected_clients:
                            if username == client[0]:
                                print("disconnected: username not available")
                                conn.send("err_username_unavailable".encode("utf-8"))
                                conn.close()
                                flag = True 
                    if flag:
                        break
                           

                    self.connected_clients.append((username,conn))
                    print(f"join: {username}")
                    current_username = username
                   

                elif msg_list[0] == "quit":
                    print("check")
                    username = msg_list[1]
                    
                    print(f"disconnected: {username}")
                    conn.close()
                    break

                
                
                elif msg_list[0] == "list":
                    l = ""
                    for n in range(len(self.connected_clients)):
                        l += self.connected_clients[n][0] + " "
                    print("request_users_list:",msg_list[1])
                    users_list_msg = "list " + l
                    conn.send(users_list_msg.encode(FORMAT))

                elif msg_list[0] == "msg":
                    print("msg:",current_username)
                    sender_username = msg_list[2]
                    recipient_count = int(msg_list[1])
                    recipients = msg_list[2:2 + recipient_count]
                    message = " ".join(msg_list[2 + recipient_count:])
                    recipients = set(recipients)
                    for recipient in recipients:
                        found = False
                        for client in self.connected_clients:
                            if recipient == client[0]: 
                                recipient_msg = f"msg {current_username}: {message}"
                                client[1].send(recipient_msg.encode("utf-8"))
                                found = True
                      
                        if not found:
                            print(f"msg: {current_username} to non-existent user {recipient}")

                elif msg_list[0] == "file":
                    print("file:",current_username)
                    sender_username = msg_list[2]
                    recipient_count = int(msg_list[1])
                    recipients = msg_list[2:2 + recipient_count]
                    message = " ".join(msg_list[2 + recipient_count:])
                    recipients = set(recipients)
                    for recipient in recipients:
                        found = False
                        for client in self.connected_clients:
                            if recipient == client[0]:  
                                recipient_msg = f"file {current_username}: {message}"
                                client[1].send(recipient_msg.encode("utf-8"))
                                found = True
                      
                        if not found:
                            print(f"file: {current_username} to non-existent user {recipient}")
                   

                elif msg_list[0] == "err_server_full":
                    print("Disconnected: Server full")
                    conn.close()

                elif msg_list[0]== "err_unknown_message":
                    print(f"disconnected: {msg_list[1]} sent an unknown command")
                    conn.close()

           
            except Exception as e:
                print(f"Exception: {e}")
                conn.close()
                break
        return



    

    
    






    

# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a", ["port=", "address="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    SERVER = Server(DEST, PORT)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
