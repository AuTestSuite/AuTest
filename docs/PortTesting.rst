Port Readiness Testing
======================

There are 4 When items that can be used to test for ports readiness: *PortOpen*, *PortReady*, *PortsOpen*, and *PortsReady*. As the name implies, *PortsOpen* and *PortsReady* are simply wrappers of *PortOpen* and *PortReady* that can take in multiple ports. 

PortOpen
--------

This function psutil to probe whether a port is open by seeing if it is in either LISTEN or NONE state. The potential issue with this is that the source of the port might not be ready to accept data, so if psutil fails to detect a port, we fallback onto the *PortReady* logic.


PortReady
---------

This function opens a port and uses Python's builtin socket functions to send some traffic to the port. If the connection is successful, then the port is considered to be ready. However, this does not guarantee the process listening the the port is necessarily ready.