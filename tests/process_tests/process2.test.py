
Test.Summary='''
Test Runnning of processes and shutdown of global process
'''

Setup.Copy("app.py","app")
Setup.Copy("app.py","global1")
Setup.Copy("app.py","global2")

Test.Processes.Process("g1","python global1 300")
Test.Processes.Process("g2","python global2 300")

t=Test.AddTestRun("Test Creation of many processes")
p=t.Processes.Default
p.Command="python app 1"
p.ReturnCode=0

p.StartBefore= Test.Processes.g1
p.StartAfter= Test.Processes.g2


t=Test.AddTestRun("Test Processes are running still")
t.StillRunningBefore=Test.Processes.g1
t.StillRunningBefore=Test.Processes.g2
t.StillRunningAfter=Test.Processes.g1
t.StillRunningAfter=Test.Processes.g2
p=t.Processes.Default
p.Command="python app 1"
p.ReturnCode=0

