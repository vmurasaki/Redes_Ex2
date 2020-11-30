# Echo multiconn server program
import selectors
import socket

HOST = '0.0.0.0' # Symbolic name meaning all available interfaces
PORT = 50007 # Arbitrary non-privileged port

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    print('Accepted', conn) 
    print('From', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    conn.sendall(b'dir')

def read(conn, mask):
    data = conn.recv(1024) # Should be ready
    if data:
        print(repr(data))
    else:
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)


