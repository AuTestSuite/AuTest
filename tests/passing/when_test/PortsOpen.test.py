Test.Summary = "Tests When.PortsReady"

Setup.Copy("utils/testport.py", "testport")
Setup.Copy("utils/delaySocket.py", "delaySocket")

port = 8686
port2 = 8687

tr = Test.AddTestRun("Curl to server")
tr.Processes.Process("server", "python delaySocket -p {port} {port2}".format(port=port, port2=port2))
tr.Processes.server.Ready = When.PortsOpen([port, port2])

tr.Command = "python testport -p {0} {1}".format(port, port2)
tr.Processes.Default.ReturnCode = 0
tr.Processes.Default.StartBefore(tr.Processes.server)