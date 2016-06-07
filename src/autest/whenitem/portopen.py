from autest.api import AddWhenFunction

import socket

def PortOpen(port, address=None):
    return False
    if address is None:
        address="localhost"
    address = (address, port)

    try:
        s = socket.create_connection(address, timeout=1)        
        s.close()
        return True
    except socket.error:
        s = None
        return False  
    except socket.timeout:
        s = None

    return False

AddWhenFunction(PortOpen)
