
import sys
from socket import *
from threading import *



def main():

    # Server socket 
    server_sock = socket()

    # Finding listening socket using IP address and port number 
    server_addr = ("0.0.0.0", 8080)
    server_sock.bind(server_addr)

    # Determines the number of pending connection (Queued Connections)
    server_sock.listen(5)
 
    
    while True:
      
        (conn_sock, conn_addr) = server_sock.accept()

        #Creates a new thread for a new connection            
        thread_handle = Thread(target=new_thread, args=(conn_sock,))

        #Starts a thread
        thread_handle.start()
    

# This function will do the following:
#           1.) Receive (.recv())
#           2.) Read    (read())
#           3.) Send Answer 
def new_thread(client_sock):
 
    client_msg = client_sock.recv(1024).decode()
     
    assert client_msg != "", "No Request."

    # Splitting client's message
    client_msg = client_msg.split('\n')

    # Checks if 'GET' exists
    get_command = client_msg[0].split()
    
    if get_command[0] != "GET":
        client_sock.close() 
        return  
    else:
        # Desired file
        filename = get_command[1].lstrip('/')
        

    try:
    
        # Checks if the file is exist
        
        #Reads Binary files
        #Opens the Binary File
        read_msg = open(str(filename), "rb")
        sys.stdout.flush()
        #Reads through the whole file 
        whole_file = read_msg.read()
        
        #Content length
        length_file = len(whole_file)
        # Answers client request
        answer = "HTTP/1.1 200 OK\nContent-Length: " + str(length_file)
        answer += "\n\n"      

        # Sends  the answer for the client 
        client_sock.sendall(answer.encode())
        client_sock.sendall(whole_file)   
    

    except IOError:

        # File is NOT FOUND
        answer = "HTTP/1.1 404 Not Found\n\n"

        client_sock.sendall(answer.encode())
    
    
    #Server is closed 
    client_sock.close()          
           
main()
