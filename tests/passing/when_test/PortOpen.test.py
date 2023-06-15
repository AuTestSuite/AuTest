Test.Summary = "Tests When.PortOpen"

Setup.Copy("utils/testport.py", "testport")
Setup.Copy("utils/delaySocket.py", "delaySocket")

port = 8484

tr = Test.AddTestRun("Curl to server")
tr.Processes.Process("server", "python delaySocket -p {port}".format(port=port))
tr.Processes.server.Ready = When.PortOpen(port)
#tr.Processes.server.StartupTimeout = 30  # need more time in cases of dns issues.

tr.Command = "python testport -p {0}".format(port)
tr.Processes.Default.ReturnCode = 0
tr.Processes.Default.StartBefore(tr.Processes.server)
