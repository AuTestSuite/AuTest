Test.Summary = "Test the we fail when a timeout is set"

Setup.Copy("server.py", "server")

tr = Test.AddTestRun()
tr.Command = "python server --time=10"
tr.TimeOut = 1
# should never run
tr.ReturnCode = 0
