Test.Summary="Test a case of is ready logic for start different propocesses"

Test.SkipUnless(Condition.HasProgram("curl","Curl need to be installed on system for this test to work"))

Setup.Copy("server.py","server")

tr=Test.AddTestRun()
s=tr.Processes.Process("server","python server --time=1 --port 8080",returncode=None)
s.Ready=When.PortOpen(8080)
tr.Command="curl 127.0.0.1:8080"
tr.ReturnCode=0
tr.Processes.Default.StartBefore(tr.Processes.server,ready=When.PortOpen,port=8080)
