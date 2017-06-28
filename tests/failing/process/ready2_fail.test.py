Test.Summary="Test the we fail when we don't start up in the expected time"

Setup.Copy("server.py","server")

tr=Test.AddTestRun()
tr.Processes.Process("server","python server --time=1 --port 8080",returncode=None)
# setting time explict to a smaller time value
tr.Processes.server.StartupTimeout=1
# should never run
tr.Command="curl 127.0.0.1:8080"
tr.ReturnCode=0
# set bad port to wait on
tr.Processes.Default.StartBefore(tr.Processes.server,ready=When.PortOpen(8090))