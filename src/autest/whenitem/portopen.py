from autest.api import AddWhenFunction
import hosts.output as host

import socket
reported=0
def PortOpen(port, address=None):
    global reported
    reported=0
    ret=False
    if address is None:
        address="localhost"

    address = (address, port)    

    try:
        s = socket.create_connection(address, timeout=.5)
        s.close()
        ret = True
    except socket.error:
        s = None
        ret = False  
    except socket.timeout:
        s = None
    # high volume... so we do this in debug only    
    if ret or reported%100==0:
        host.WriteDebug(["portopen", "when"], "checking port {0} = {1}".format(port,ret))
        reported+=1
    return ret

AddWhenFunction(PortOpen)
