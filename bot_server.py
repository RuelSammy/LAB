import socketserver

class BotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive data from the bot
        self.data = self.request.recv(1024).strip()
        print("Bot with IP {} sent:".format(self.client_address[0]))
        print(self.data.decode())  # Decode the bytes for printing
        
        # Send a response back to the bot
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "", 8000
    tcpServer = socketserver.TCPServer((HOST, PORT), BotHandler)
    print(f"Server running on {HOST}:{PORT}")

    try:
        tcpServer.serve_forever()
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")
    except Exception as e:
        print(f"There was an error: {e}")
    finally:
        print("Shutting down the server.")
        tcpServer.server_close()
