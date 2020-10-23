Test.Summary = "Test the we fail when we don't start up in the expected time"

Setup.Copy("server.py", "server")

tr = Test.AddTestRun()
s = tr.Processes.Process("server", "python server --time=1 --port 8080", returncode=None)
# set bad port so we will fail
s.Ready = When.PortOpen(8090)
# setting time explict to a smaller time value
s.StartupTimeout = 1
# should never run
tr.Command = "curl 127.0.0.1:8080"
tr.ReturnCode = 0
tr.Processes.Default.StartBefore(tr.Processes.server)
