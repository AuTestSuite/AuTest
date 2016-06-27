from autest.api import AddWhenFunction
import hosts.output as host

import socket

def PortOpen(port, address=None):

    if address is None:
        address="localhost"
    address = (address, port)
    #host.WriteVerbose(["portopen", "when"], "checking port {0}".format(port))

    try:
        s = socket.create_connection(address, timeout=.5)
        s.close()
        return True
    except socket.error:
        s = None
        return False  
    except socket.timeout:
        s = None

    return False

AddWhenFunction(PortOpen)
