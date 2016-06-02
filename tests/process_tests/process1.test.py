
Test.Summary='''
Test Runnning of processes and shutdown
'''

Setup.Copy("app.py","app")
Setup.Copy("app.py","app.p1")
Setup.Copy("app.py","app.p2")
Setup.Copy("app.py","app.1")
Setup.Copy("app.py","app.2")

t=Test.AddTestRun("Test creation of default")
t.Processes.Default.Command="python app 1"
t.Processes.Default.ReturnCode=0

t=Test.AddTestRun("Test creation default and assignment of object")
p=t.Processes.Default
p.Command="python app 1"
p.ReturnCode=0

t=Test.AddTestRun("Test Creation of many processes")
p=t.Processes.Default
p.Command="python app 1"
p.ReturnCode=0

pre1=t.Processes.Process("pre1","python app.p1 5")
pre2=t.Processes.Process("pre2","python app.p2 5")
post1=t.Processes.Process("post1","python app.1 2")
post2=t.Processes.Process("post2","python app.2 220")

pre2.StartBefore(pre1) 
post2.StartBefore(post1)
p.StartBefore(pre2)
p.StartAfter(post2)
